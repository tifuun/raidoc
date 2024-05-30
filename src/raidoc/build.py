from pathlib import Path
import shutil

import sass
import jinja2
import marko
from pygments.formatters import HtmlFormatter

from raidoc.raimark_ext import RaimarkExt


def build(source='./doc', dest='./build'):
    source = Path(source)
    dest = Path(dest)

    md = marko.Markdown(extensions=['gfm', 'codehilite', RaimarkExt])

    env = jinja2.Environment(
        autoescape=False,
        undefined=jinja2.StrictUndefined,
        )
    template = env.from_string((source / 'templ/root.html').read_text())

    if dest.exists():
        shutil.rmtree(dest)

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

    for path in (source / 'pages').rglob('*'):
        if path.suffix != '.md':
            continue

        markdown = path.read_text()

        try:
            content = md(markdown)
        except Exception as e:
            raise Exception(
                f'Error rendering markdown file {str(path)}'
                ) from e

        html = template.render({
            'content': content
            })

        destparent = dest / path.parent.relative_to(source)
        destparent.mkdir(parents=True, exist_ok=True)
        destpath = destparent / f"{path.stem}.html"
        destpath.write_text(html)

