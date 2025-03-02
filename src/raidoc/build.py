from pathlib import Path
import shutil
import subprocess
import json

import sass
import jinja2
import marko
from pygments.formatters import HtmlFormatter
import frontmatter
from addict import Dict

from raidoc.raimark_ext import RaimarkExt, LinkMixin, IndexerMixin
from raidoc.autogen import FilesystemScanner

import raimad

dot_sanitizer = str.maketrans({
    '-': '_',
    '.': '_',
    })


def build(source='./doc', dest='./build'):
    source = Path(source)
    dest = Path(dest)

    #scanner = FilesystemScanner()
    #scanner.use_module(raimad)
    #scanner.scan()
    #for file_scanner in scanner.file_scanners:
    #    md_path = (
    #        source / 'pages' / 'autogen' / file_scanner.relpath
    #        .with_suffix('.md')
    #        )
    #    (md_path.parent).mkdir(parents = True, exist_ok = True)
    #    md_path.write_text(file_scanner.get_md())

    graph = [
        'digraph D {',
        '\tlayout=neato;',
        '\toverlap=false;',
        '\tsplines=true;',
        '\tnodesep=0.8;',
        '\tranksep=1.0;',
        ]

    md = marko.Markdown(extensions=['gfm', 'codehilite', RaimarkExt])

    search_index = []

    env = jinja2.Environment(
        autoescape=False,
        undefined=jinja2.StrictUndefined,
        )
    template = env.from_string((source / 'templ/root.html').read_text())

    if dest.exists():
        shutil.rmtree(dest)

    shutil.copytree(source / 'fontawesome', dest / 'fontawesome')
    shutil.copytree(source / 'img', dest / 'img')
    shutil.copytree(source / 'js', dest / 'js')
    for path in (source / 'scss').rglob('*'):
        if path.suffix != '.scss':
            continue

        scss = path.read_text()
        css = sass.compile(string=scss)
        destparent = dest / 'css' / path.parent.relative_to(source / 'scss')
        destparent.mkdir(parents=True, exist_ok=True)
        destpath = destparent / f"{path.stem}.css"
        destpath.write_text(css)

    pyg_style = HtmlFormatter(style='default').get_style_defs()
    (dest / 'pyg.css').write_text(pyg_style)

    for path in (source).rglob('*'):
        if path.suffix != '.md':
            continue

        fm = frontmatter.load(path)

        prevnext = Dict()
        prevnext.prev = fm.get('prev', '').replace('.md', '.html')
        prevnext.next = fm.get('next', '').replace('.md', '.html')
        # TODO ugly replace hack. Again,
        # we need a prepass to map filename -> title
        # but also filename.md -> filename.html

        # Strip frontmatter before passing to marko
        markdown = fm.content

        LinkMixin.links_to = []
        IndexerMixin.init()

        try:
            content = md(markdown)
        except Exception as e:
            raise Exception(
                f'Error rendering markdown file {str(path)}'
                ) from e

        for link_dest in LinkMixin.links_to:
            dest_stem = Path(link_dest).stem
            graph.append(
                f"\t{path.stem.translate(dot_sanitizer)} -> "
                f"{dest_stem.translate(dot_sanitizer)};"
                )

        graph.append(
            f'''\t{path.stem.translate(dot_sanitizer)} '''
            f'''[URL="{path.relative_to(source).with_suffix('.html')}"];'''
            )

        html = template.render({
            'content': content,
            'webroot': '../' * len(path.relative_to(source).parent.parts),
            'prevnext': prevnext
            })

        destparent = dest / path.parent.relative_to(source)
        destparent.mkdir(parents=True, exist_ok=True)
        destpath = destparent / f"{path.stem}.html"
        destpath.write_text(html)

        search_index.append((
            str(path.relative_to(source).with_suffix('.html')),
            IndexerMixin.get_index_entry()
            ))

    graph.append('}')

    map_gv = Path(dest / 'map.gv')
    map_svg = Path(dest / 'map.svg')
    map_cmap = Path(dest / 'map-cmap.html')
    map_gv.write_text('\n'.join(graph))

    # TODO copypasta
    subprocess.Popen(
        [
            'dot',  # Call the DOT compiler...
            '-Tsvg',  # tell it to produce an SVG file...
            '-Gbgcolor=none',  # ...with a transparent background
            '-Nfontsize=10',  # ... with a smaller than usual font size
            '-Nfontname=Courier New',  # ... with a smaller than usual font size
            f'-o{str(map_svg)}',
            f'{str(map_gv)}',
            ],
        ).wait()
    subprocess.Popen(
        [
            'dot',  # Call the DOT compiler...
            '-Tcmapx',  # tell it to produce an SVG file...
            '-Gbgcolor=none',  # ...with a transparent background
            '-Nfontsize=10',  # ... with a smaller than usual font size
            '-Nfontname=Courier New',  # ... with a smaller than usual font size
            f'-o{str(map_cmap)}',
            f'{str(map_gv)}',
            ],
        ).wait()


    template = env.from_string((source / 'templ/map.html').read_text())
    html = template.render({
        'webroot': '',
        'map_cmap': map_cmap.read_text()
        })
    (dest / 'map.html').write_text(html)

    with (dest / 'search_index.js').open('w') as file:
        file.write('var search_index = ')
        json.dump(search_index, file)
        file.write(';\n')

    template = env.from_string((source / 'templ/search.html').read_text())
    html = template.render({
        'webroot': '',
        })
    (dest / 'search.html').write_text(html)


