"""builder.py: home to Builder class"""

from typing import Any
from dataclasses import dataclass, field
from pathlib import Path
import shutil
import os
from collections import defaultdict
import json
import importlib
import ast
import subprocess

import sass
import frontmatter
import marko
import jinja2
from addict import Dict
from reflink import reflink
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer
from pygments import highlight
import ansi2html

import raimad as rai

from raidoc.raimark_ext import RaimarkExt
from raidoc.raimark_ext import RaimarkPrepassExt
from raidoc.raimark_ext import TitleMixin
from raidoc.raimark_ext import IndexerMixin
from raidoc.raimark_ext import LinkMixin
from raidoc.raimark_ext import JupyterExporterMixin
#from raidoc.autogen import FilesystemScanner
#from raidoc.autogen import ast_unparse_function_signature
from raidoc.autogen import scan_public

#class PageKind(StrEnum):
#    NONE = 'none'
#    TUTORIAL = 'tutorial'
#    HOWTO = 'howto'
#    DEEPDIVE = 'deepdive'
#    REFERENCE = 'reference'

from typing import cast

def _pygmentize(code):
    return highlight(code, PythonLexer(), HtmlFormatter(nowrap=True))

def _goat(code):
    goat = subprocess.Popen(
        ['goat', ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        # FIXME check status code
        )
    stdout, stderr = goat.communicate(code.encode('utf-8'))
    assert not stderr
    return stdout.decode('utf-8')

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
            loader=jinja2.FileSystemLoader(source / 'templ')
            )
        self.j2_templ = self.j2_env.from_string((source / 'templ/root.html').read_text())

        self.j2_function_reference = self.j2_env.from_string((source / 'templ/function-reference.html').read_text())
        self.j2_class_reference = self.j2_env.from_string((source / 'templ/class-reference.html').read_text())

        self.marko = marko.Markdown(extensions=['gfm', 'codehilite', RaimarkExt])
        self.marko_prepass = marko.Markdown(extensions=[RaimarkPrepassExt])

        try:
            self.raidoc_version = importlib.metadata.version('raidoc')
        except:
            self.raidoc_version = '???'

    def page(self, path):
        # FIXME path vs name!?
        for page in self.pages:
            if page.path is None:
                # FIXME hack for autogen
                continue
            if page.path.name == Path(path).name:
                return page
        raise Exception(path)

    def render_autogen(self, dest):
        #functions, classes = scan_public(rai)

        # TODO so that self.pages entries exist already
        # this just kind of ignores them.
        # Refactor so that these pages are generated from self.pages

        for fn in self.autogen_functions:
            html_content = (
                self.j2_function_reference.render({
                    'fndef': fn,
                    '_pygmentize': _pygmentize,
                    '_goat': _goat,
                    })
                )

            html_full = self.j2_templ.render({
                'page': {
                    'html_content': html_content,
                    'path_md': None,  # FIXME this is a hack
                    'journey_links': None,
                    },
                'pages': self.pages,
                'webroot': '../../',
                'body_classes': 'autogen',
                #'all_pages': self.marko(self.get_pages_by_kind_str()),  #FIXME
                'raidoc_version': f"v{self.raidoc_version}",
                })

            path_html = dest / f'pages/autogen/fn_{fn.name}.html'
            path_html.write_text(html_full)

        for cls in self.autogen_classes:
            html_content = (
                self.j2_class_reference.render({
                    'clsdef': cls,
                    '_pygmentize': _pygmentize,
                    '_goat': _goat,
                    })
                )

            # FIXME get rid of this entire function and have
            # the standard page render logic handle this to
            # avoid copypasta
            html_full = self.j2_templ.render({
                'page': {
                    'html_content': html_content,
                    'path_md': None,  # FIXME this is a hack
                    'journey_links': None,
                    },
                'pages': self.pages,
                'webroot': '../../',
                'body_classes': 'autogen',
                #'all_pages': self.marko(self.get_pages_by_kind_str()),  #FIXME
                'raidoc_version': f"v{self.raidoc_version}",
                })

            path_html = dest / f'pages/autogen/cls_{cls.name}.html'
            path_html.write_text(html_full)

        #scanner = FilesystemScanner()
        #scanner.use_module(rai)
        #scanner.scan()

        #for file_scanner in scanner.file_scanners:
        #    for cls in file_scanner.classes:
        #        pass
        #    for fn in file_scanner.functions:
        #        html_content = (
        #            self.j2_function_reference.render({
        #                'reference': {
        #                    'name': fn.name,
        #                    'signature': ast_unparse_function_signature(fn),
        #                    'docstring': ast.get_docstring(fn),
        #                    }
        #                })
        #            )

        #        html_full = self.j2_templ.render({
        #            'page': {
        #                'html_content': html_content,
        #                'path_md': None,  # FIXME this is a hack
        #                'journey_links': None,
        #                },
        #            'webroot': '../../',
        #            'raidoc_version': f"v{self.raidoc_version}",
        #            })

        #        (dest / f'pages/autogen/fn_{fn.name}.html').write_text(html_full)

    
    def render(self, dest: Path):

        Path(dest / 'pages').mkdir(parents=True, exist_ok=True)
        Path(dest / 'pages/autogen').mkdir(parents=True, exist_ok=True)
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
            if page.path is None:
                #FIXME hack for autogen
                continue
            (dest / page.path_html).write_text(page.html_full)
            (dest / page.path_md).write_text(page.md)
            json.dump(page.jupyter_json, (dest / page.path_jupyter).open('w'))

        self.render_autogen(dest)


    def _prepass(self) -> None:
        for path in (self.source).rglob('*.md'):
            self._load_page(path)

        for page in self.pages:
            try:
                self._parse_journey(page)
            except Exception as e:
                raise Exception(f"While parsing {page}") from e

        # autogen
        self.autogen_functions, self.autogen_classes = scan_public(rai)
        for fn in self.autogen_functions:

            #FIXME copypasta from render_autogen
            path_html = f'pages/autogen/fn_{fn.name}.html'

            self.pages.append(
                Page(
                    path=None,
                    path_html=path_html,
                    path_md=None,
                    path_jupyter=None,
                    title=f"Function: {fn.name}",
                    fm={'kind': 'reference'},  # TODO separate field?
                    md=None,
                    )
                )

        for cls in self.autogen_classes:

            #FIXME copypasta from render_autogen
            path_html = f'pages/autogen/cls_{cls.name}.html'

            self.pages.append(
                Page(
                    path=None,
                    path_html=path_html,
                    path_md=None,
                    path_jupyter=None,
                    title=f"Class: {cls.name}",
                    fm={'kind': 'reference'},  # TODO separate field?
                    md=None,
                    )
                )


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

    #def get_pages_by_kind(self):
    #    by_kind = defaultdict(list)
    #    by_kind['tutorial']
    #    by_kind['other']
    #    for page in self.pages:
    #        by_kind[str(page.fm.get('kind', 'other')).lower()].append(page)
    #    return by_kind

    #def _get_pages_by_kind_str(self):
    #    #FIXME just add full jinja templating to the md files
    #    #aswell as html
    #    for kind, pages in self.get_pages_by_kind().items():
    #        yield f'### {kind}\n'
    #        for page in pages:
    #            if page.path is None:  # TODO hack for autogen
    #                yield f'- [{page.title}]({str(page.path_html)}) \n'
    #                continue

    #            if page.path.name == 'index.md':
    #                continue

    #            yield f'- [[{str(page.path)}]] \n'

    #def get_pages_by_kind_str(self):
    #    return ''.join(self._get_pages_by_kind_str())

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
                '{{webroot}}', 
                webroot
            )#.replace(
            #    '{{all_pages}}', 
            #    self.get_pages_by_kind_str()
            #    )

        self.monkeypatch_current_page = page
        page.html_content = self.marko(page.md_filled)

        page.html_full = self.j2_templ.render({
            'page': page,
            'pages': self.pages,
            'webroot': webroot,
            'body_classes': '',
            #'all_pages': self.marko(self.get_pages_by_kind_str()),  #FIXME
            'raidoc_version': f"v{self.raidoc_version}",
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



