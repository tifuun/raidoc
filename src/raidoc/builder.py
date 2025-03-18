"""builder.py: home to Builder class"""

from typing import Any
from dataclasses import dataclass, field
from pathlib import Path
import shutil
import os
from collections import defaultdict

import sass
import frontmatter
import marko
import jinja2
from addict import Dict
from reflink import reflink
from pygments.formatters import HtmlFormatter
import ansi2html

import raimad as rai

from raidoc.raimark_ext import RaimarkExt
from raidoc.raimark_ext import RaimarkPrepassExt
from raidoc.raimark_ext import TitleMixin
from raidoc.raimark_ext import IndexerMixin
from raidoc.raimark_ext import LinkMixin

#class PageKind(StrEnum):
#    NONE = 'none'
#    TUTORIAL = 'tutorial'
#    HOWTO = 'howto'
#    DEEPDIVE = 'deepdive'
#    REFERENCE = 'reference'

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

    journey_links: list[JourneyLink] = field(default_factory=list)

    md_filled: str = ''
    html_content: str = ''
    html_full: str = ''

def custom_copy(source, dest):
    print(dest)
    #if os.path.exists(dest):
    #    if os.stat(source).st_mtime <= os.stat(dest).st_mtime:
    #        print('a')
    #        return reflink(source, dest)
    #else:
    #    print('b')
    #return reflink(source, dest)
    raise Exception()

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
        self.marko_prepass = marko.Markdown(extensions=[RaimarkPrepassExt])

    def page(self, path):
        # FIXME path vs name!?
        for page in self.pages:
            if page.path.name == Path(path).name:
                return page
        raise Exception(path)
    
    def render(self, dest: Path):
        for subfolder in (
                'img',
                'js',
                'asciinema'
                ):
            shutil.copytree(
                self.source / subfolder,
                dest / subfolder,
                #copy_function=custom_copy,
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

        ansi_style = '\n'.join(
                str_style
                for style in ansi2html.style.get_styles()
                if (str_style := str(style)).startswith('.ansi')
                )
        # FIXME .inv styles not covered
        (dest / 'ansi.css').write_text(ansi_style)

        for page in self.pages:
            (dest / page.path_html).write_text(page.html_full)

    def _prepass(self) -> None:
        for path in (self.source).rglob('*.md'):
            self._load_page(path)

        for page in self.pages:
            self._parse_journey(page)

    def _load_page(self, path: Path) -> Page:
        fm = frontmatter.load(path)
        md = fm.content

        TitleMixin.clear()
        IndexerMixin.clear()
        LinkMixin.builder = self
        self.marko_prepass(md)
        title = TitleMixin.page_title

        path = path.relative_to(self.source)
        path_html = path.with_suffix('.html')

        self.pages.append(
            Page(
                path=path,
                path_html=path_html,
                title=title,
                fm=Dict(fm.to_dict()),
                md=md,
                )
            )

        return self.pages[-1]

    def _parse_journey(self, page: Page) -> None:
        journey = page.fm.journey
        if not journey:
            return

        # FIXME one and two item journeys

        journey_pages = (
            page.path,
            *journey.pages
            )

        for prev, this, next in rai.triplets(journey_pages):
            self.page(this).journey_links.append(
                JourneyLink(
                    journey_page=page,
                    prev=self.page(prev),
                    next=self.page(next)
                )
            )

        self.page(journey.pages[-1]).journey_links.append(
            JourneyLink(
                journey_page=page,
                prev=self.page(journey.pages[-2])
            )
        )

        page.journey_links.append(
            JourneyLink(
                journey_page=page,
                next=self.page(journey.pages[0])
            )
        )

    def get_pages_by_kind(self):
        by_kind = defaultdict(list)
        by_kind['tutorial']
        by_kind['other']
        for page in self.pages:
            by_kind[str(page.fm.get('kind', 'other')).lower()].append(page)
        return by_kind

    def _get_pages_by_kind_str(self):
        #FIXME just add full jinja templating to the md files
        #aswell as html
        for kind, pages in self.get_pages_by_kind().items():
            yield f'### {kind}\n'
            for page in pages:
                if page.path.name == 'index.md':
                    continue
                yield f'- [[{str(page.path)}]] \n'

    def get_pages_by_kind_str(self):
        return ''.join(self._get_pages_by_kind_str())

    def _render_page(self, page: Page):

        webroot = '../' * (len(page.path.parts) - 1)

        # TODO full jinja
        page.md_filled = page.md.replace(
            '{{journey_toc}}', 
            '\n'.join((
                f'1. [[{link}]]'
                for link in page.fm.journey.pages
                ))
            ).replace(
                '{{all_pages}}', 
                self.get_pages_by_kind_str()
                )

        page.html_content = self.marko(page.md_filled)

        page.html_full = self.j2_templ.render({
            'page': page,
            'webroot': webroot,
            })



