"""builder.py: home to Builder class"""

from typing import Any
from dataclasses import dataclass, field
from pathlib import Path
import shutil
import os
from collections import defaultdict
import json

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
from raidoc.raimark_ext import JupyterExporterMixin

#class PageKind(StrEnum):
#    NONE = 'none'
#    TUTORIAL = 'tutorial'
#    HOWTO = 'howto'
#    DEEPDIVE = 'deepdive'
#    REFERENCE = 'reference'

from typing import cast

#FIXME horrible monkeypatch
def wtf(self, text):
    source = marko.source.Source(text)
    source.parser = self
    doc = cast(marko.block.Document, self.block_elements["Document"]())
    with source.under_state(doc):
        doc.children = self.parse_source(source)
        self.parse_inline(doc, source)

    self.monkeypatch_source = source

    return doc


marko.Parser.parse = wtf

def wtf2(source):
    cls = marko.block.FencedCode

    m = source.expect_re(cls.pattern)
    if not m:
        return None
    prefix, leading, info = m.groups()
    if leading[0] == "`" and "`" in info:
        return None
    lang, _, extra = marko.helpers.partition_by_spaces(info)
    source.context.code_info = cls.ParseInfo(prefix, leading, lang, extra)
    return m

import re
def wtf3(source) -> tuple[str, str, str]:
    cls = marko.block.FencedCode

    source.next_line()
    source.consume()
    lines = []
    parse_info: marko.block.FencedCode.ParseInfo = source.context.code_info
    while not source.exhausted:
        line = source.next_line()
        if line is None:
            break
        source.consume()
        m = re.match(r" {,3}(~+|`+)[^\n\S]*$", line, flags=re.M)
        if m and parse_info.leading in m.group(1):
            break

        prefix_len = source.match_prefix(parse_info.prefix, line)
        if prefix_len >= 0:
            line = line[prefix_len:]
        else:
            line = line.lstrip()
        lines.append(line)

    return parse_info.lang, parse_info.extra, "".join(lines)

def wtf4(self, source):
    """Parse the source into a list of block elements."""
    element_list = self._build_block_element_list()
    ast: list[block.BlockElement] = []
    while not source.exhausted:
        for ele_type in element_list:
            if ele_type.match(source):
                result = ele_type.parse(source)
                if not hasattr(result, "priority"):
                    # In some cases ``parse()`` won't return the element, but
                    # instead some information to create one, which will be passed
                    # to ``__init__()``.
                    result = ele_type(result)  # type: ignore

                if not hasattr(result, 'monkeypatch_source'):
                    result.monkeypatch_source = ''.join(
                        match.string[match.span()[0]:match.span()[1]]
                        for match in
                        source.monkeypatch_lines
                        )
                    source.monkeypatch_lines.clear()

                ast.append(result)
                break
        else:
            # Quit the current parsing and go back to the last level.
            break
    return ast

marko.parser.Parser.parse_source = wtf4

class MySource(marko.source.Source):
    def __init__(self, *args, **kwargs):
        self.monkeypatch_lines = []
        super().__init__(*args, **kwargs)

    def push_state(self, *args, **kwargs):
        self.monkeypatch_lines.clear()
        return super().push_state(*args, **kwargs)

    def pop_state(self, *args, **kwargs):
        #self.monkeypatch_lines.clear()
        return super().pop_state(*args, **kwargs)

    def consume(self, *args, **kwargs):
        #FIXME WHAT is going on here + prefix is lost
        self.monkeypatch_lines.append(self.match)
        self.state.monkeypatch_source = ''.join(
            match.string[match.span()[0]:match.span()[1]]
            for match in
            self.monkeypatch_lines
            )
        return super().consume(*args, **kwargs)

marko.source.Source = MySource

@dataclass
class JourneyLink:
    journey_page: 'Page'
    prev: 'Page | None' = None
    next: 'Page | None' = None

@dataclass
class Page:
    path: Path  # <- in source directory
    path_html: Path
    path_jupyter: Path
    path_md: Path  # <- in build directory, to allow users to download
    title: str
    fm: Any  # FIXME
    md: str

    jupyter_json: dict | None = None

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

        Path(dest / 'pages').mkdir(parents=True, exist_ok=True)
        Path(dest / 'downloads/jupyter/pages').mkdir(parents=True, exist_ok=True)
        Path(dest / 'downloads/md/pages').mkdir(parents=True, exist_ok=True)

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
            (dest / page.path_md).write_text(page.md)
            json.dump(page.jupyter_json, (dest / page.path_jupyter).open('w'))


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
        path_jupyter = Path('downloads/jupyter') / path.with_suffix('.ipynb')
        path_md = Path('downloads/md') / path

        self.pages.append(
            Page(
                path=path,
                path_html=path_html,
                path_md=path_md,
                path_jupyter=path_jupyter,
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

        # jupyter notebook stuff

        cells = []
        for element, source in JupyterExporterMixin.toplevel_elements:
            if isinstance(element, marko.block.FencedCode):
                cells.append({
                    'cell_type': 'code',
                    'execution_count': None,
                    'metadata': {},
                    'source': element.children[0].children
                    })
            elif isinstance(element, marko.block.BlankLine):
                continue
            else:
                cells.append({
                    'cell_type': 'markdown',
                    'metadata': {},
                    'source': element.monkeypatch_source
                    })

        page.jupyter_json = {
                'nbformat': 4,
                'nbformat_minor': 0,
                'metadata': {},
                'cells': cells
            }



