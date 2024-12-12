"""builder.py: home to Builder class"""

from typing import Any
from dataclasses import dataclass, field
from pathlib import Path
import shutil
import os

import sass
import frontmatter
import marko
import jinja2
from addict import Dict
from reflink import reflink
from pygments.formatters import HtmlFormatter

import raimad as rai

from raidoc.raimark_ext import TitleMixin
from raidoc.raimark_ext import IndexerMixin
from raidoc.raimark_ext import RaimarkExt
from raidoc.raimark_ext import LinkMixin

@dataclass
class JourneyLink:
    journey_page: 'Page'
    prev: 'Page | None' = None
    next: 'Page | None' = None

@dataclass
class Page:
    path: Path
    path_html: Path
    title: str
    fm: Any  # FIXME
    md: str
    html_content: str

    journey_links: list[JourneyLink] = field(default_factory=list)

    html_full: str = ''

def custom_copy(source, dest):
    if os.path.exists(dest):
        if os.stat(source).st_mtime <= os.stat(dest).st_mtime:
            return reflink(source, dest)
    else:
        return reflink(source, dest)

class Builder:
    pages: list[Page]

    def __init__(self, source: Path) -> None:
        self.source = source

        self.pages = []

        self.j2_env = jinja2.Environment(
            autoescape=False,
            undefined=jinja2.StrictUndefined,
            )
        self.j2_templ = self.j2_env.from_string((source / 'templ/root.html').read_text())

        self.marko = marko.Markdown(extensions=['gfm', 'codehilite', RaimarkExt])

    def page(self, path):
        for page in self.pages:
            # The `str` here converts Path to str so that the equality works
            if str(page.path) == path:
                return page
        raise Exception(path)
    
    def render(self, dest: Path):
        shutil.copytree(
            self.source / 'fontawesome',
            dest / 'fontawesome',
            copy_function=custom_copy,
            dirs_exist_ok=True
            )
        shutil.copytree(
            self.source / 'img',
            dest / 'img',
            copy_function=custom_copy,
            dirs_exist_ok=True
            )
        shutil.copytree(
            self.source / 'js',
            dest / 'js',
            copy_function=custom_copy,
            dirs_exist_ok=True
            )

        Path(dest / 'pages').mkdir(parents=True, exist_ok=True)

        for path in (self.source / 'scss').rglob('*'):
            if path.suffix != '.scss':
                continue

            scss = path.read_text()
            css = sass.compile(string=scss)
            destparent = dest / 'css' / path.parent.relative_to(self.source / 'scss')
            destparent.mkdir(parents=True, exist_ok=True)
            destpath = destparent / f"{path.stem}.css"
            destpath.write_text(css)

        pyg_style = HtmlFormatter(style='default').get_style_defs()
        (dest / 'pyg.css').write_text(pyg_style)

        for page in self.pages:
            (dest / 'pages' / page.path_html).write_text(page.html_full)

    def _prepass(self) -> None:
        for path in (self.source / 'pages').rglob('*.md'):
            self._load_page(path)

        for page in self.pages:
            self._parse_journey(page)

    def _load_page(self, path: Path) -> Page:
        fm = frontmatter.load(path)
        md = fm.content


        TitleMixin.clear()
        IndexerMixin.clear()
        LinkMixin.builder = self
        html_content = self.marko(md)
        title = TitleMixin.page_title

        path = path.relative_to(self.source / 'pages')
        path_html = path.with_suffix('.html')

        self.pages.append(
            Page(
                path=path,
                path_html=path_html,
                title=title,
                fm=Dict(fm.to_dict()),
                md=md,
                html_content=html_content
                )
            )

        return self.pages[-1]

    def _parse_journey(self, page: Page) -> None:
        journey = page.fm.journey
        if not journey:
            return

        # FIXME one and two item journeys

        for prev, this, next in rai.triplets(journey.pages):
            self.page(this).journey_links.append(
                JourneyLink(
                    journey_page=page,
                    prev=self.page(prev),
                    next=self.page(next)
                )
            )

        self.page(journey.pages[0]).journey_links.append(
            JourneyLink(
                journey_page=page,
                next=self.page(journey.pages[1])
            )
        )

        self.page(journey.pages[-1]).journey_links.append(
            JourneyLink(
                journey_page=page,
                prev=self.page(journey.pages[-2])
            )
        )

    def _render_page(self, page: Page):
        page.html_full = self.j2_templ.render({
            'page': page,
            'webroot': '../' * (len(page.path.parts) + 1),  # FIXME magic number
            })



