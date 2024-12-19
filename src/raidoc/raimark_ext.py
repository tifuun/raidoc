import subprocess
import re
import copy

import marko
from ansi2html import Ansi2HTMLConverter

ansi2html = Ansi2HTMLConverter().convert

class CodeCTX:
    def __init__(self):
        self.globs = {}
        self.locs = {}

class WikiLink(marko.inline.InlineElement):
    pattern = r'\[\[(.+?)\]\]'
    parse_children = True

    def __init__(self, match):
        self.target = match.group(1)

class LinkMixin(object):
    """
    Change markdown links that point to `.md` files
    into ones that point to `.html` files
    TODO don't touch non-local links, also validate links
    """

    links_to = []

    def render_link(self, element):
        # TODO reject xx:// type links
        if not element.dest.endswith('.md'):
            return super().render_link(element)

        self.links_to.append(element.dest)
        return '<a href="{}">{}</a>'.format(
            self.escape_url(element.dest.rstrip('.md') + '.html'),
            self.render_children(element)
            )

    def render_wiki_link(self, element):
        page = LinkMixin.builder.page(element.target)
        href = page.path_html
        title = page.title
        return f'<a href="{href}" class="wikilink">{title}</a>'


re_callout_class = re.compile(r'\s*\[\s*(\w+)\s*\]\s*')


class CalloutMixin(object):
    """
    """

    def render_quote(self, element):
        try:
            callout_tag = element.children[0].children[0].children
        except IndexError:
            # TODO huh?
            return super().render_quote(element)

        if not isinstance(callout_tag, str):
            # TODO huh?
            return super().render_quote(element)

        match = re_callout_class.match(callout_tag)
        if not match:
            return super().render_quote(element)

        # Remove the tag from rendered outout
        element.children[0].children[0].children = ''

        callout_class = match.groups()[0].lower()

        rendered_children = []
        for i, child in enumerate(element.children):
            rendered_children.append(super().render(child))

        return ''.join((
            f'<div class="blockquote-wrap {callout_class}">'
            '<div class="blockquote-before"></div>'
            '<blockquote>',
            *rendered_children,
            '</blockquote></div>',
            ))

    def render_paragraph(self, element):

        # TODO fix this monstrosity
        # this was added to prevent empty paragraph
        # when you do a callout label,
        # then line skip with a single `>`
        # then the callout body

        rendered = super().render_paragraph(element)
        if rendered.strip() == '<p></p>':
            return ''
        return rendered


class EmphasisMixin(object):

    def render_emphasis(self, element):

        rendered_children = []
        for i, child in enumerate(element.children):
            rendered_children.append(super().render(child))

        return ''.join((
            '<span class="deemphasis">',
            *rendered_children,
            '</span>',
            ))


class IndexerMixin(object):

    index_entry = None

    @classmethod
    def clear(cls):
        cls.index_entry = tuple([] for _ in range(10))

    def render_heading(self, element):

        html_text = super().render_heading(element)
        plain_text = re.sub('<[^>]*>', '', html_text).strip()
        # TODO horrible inefficient

        self.index_entry[element.level - 1].append(plain_text)

        return html_text

    @classmethod
    def get_index_entry(cls):
        return copy.deepcopy(cls.index_entry)

class TitleMixin(object):
    """Collect the title of the page"""

    page_title = ''

    @classmethod
    def clear(cls):
        cls.page_title = ''

    def render_heading(self, element):
        if not TitleMixin.page_title and element.level == 1:
            TitleMixin.page_title = element.children[0].children
            # FIXME this will break eventually
        return super().render_heading(element)


codeblock_preamble = """
import raimad as rai

__raimark_output__ = []

if '_og_print' not in dir():
    _og_print = print
def print(*args, **kwargs):
    global __raimark_output__
    from io import StringIO
    io = StringIO()
    if 'file' not in kwargs.keys():
        kwargs['file'] = io
    _og_print(*args, **kwargs)
    __raimark_output__.append(('str', io.getvalue()))

def show(obj):
    global __raimark_output__
    if hasattr(obj, '_repr_dot_'):
        __raimark_output__.append(('dot', obj._repr_dot_()))
    elif hasattr(obj, '_repr_svg_'):
        __raimark_output__.append(('svg', obj._repr_svg_()))
    else:
        __raimark_output__.append(('str', repr(obj)))

rai.show = show
"""


class CodeBlockMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = CodeCTX()

    def render_fenced_code(self, element):
        rendered_code = super().render_fenced_code(element)

        template = (
            '''<div class="raimark-rendered-code">\n'''
            '''<div class="raimark-code{hide_code}">\n'''
            '''{0}'''
            '''</div>'''
            '''<div class="raimark-output{hide_output}">'''
            '''{1}'''
            '''</div>'''
            '''</div>'''
            )

        code = element.children[0].children

        # TODO regex
        if element.lang == 'python' and 'exec' in element.extra:
            return template.format(
                rendered_code,
                self._exec_python(code),
                hide_code=' hidden' * ('hide-code' in element.extra),
                hide_output=' hidden' * ('hide-output' in element.extra),
                )

        elif element.lang == 'dot' and 'exec' in element.extra:
            return template.format(
                rendered_code,
                self._exec_dot(code),
                hide_code=' hidden' * ('hide-code' in element.extra),
                hide_output=' hidden' * ('hide-output' in element.extra),
                )
        else:
            return rendered_code

    def _exec_python(self, code):

        full_code = '\n'.join((codeblock_preamble, code))
        exec(full_code, self.ctx.globs, self.ctx.globs)
        output = self.ctx.globs['__raimark_output__']

        template = (
            '''<div class="raimark-output-block">'''
            '''{0}'''
            '''</div>'''
            )

        blocks = []
        for block_type, block_string in output:
            if block_type == 'svg':
                blocks.append(block_string)

            elif block_type == 'dot':
                blocks.append(self._exec_dot(block_string))

            else:
                blocks.append(''.join((
                    '<pre>',
                    ansi2html(
                        #self.escape_html(
                            block_string,
                            #    ),
                        full=False
                        ),
                    '</pre>',
                    )))
                # self.escape_html not needed here;
                # ansi2html takes care of that

        return '\n'.join(map(template.format, blocks))

    def _exec_dot(self, code):
        dot = subprocess.Popen(
            [
                'dot',  # Call the DOT compiler...
                '-Tsvg',  # tell it to produce an SVG file...
                '-Gbgcolor=none',  # ...with a transparent background
                '-Nfontsize=10',  # ... with a smaller than usual font size
                '-Nfontname="Courier New"',  # ... with a smaller than usual font size
                ],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            )
        stdout, stderr = dot.communicate(code.encode('utf-8'))
        assert not stderr
        return stdout.decode('utf-8')



RaimarkExt = marko.helpers.MarkoExtension(
    elements=[WikiLink],
    renderer_mixins=[
        LinkMixin,
        CodeBlockMixin,
        CalloutMixin,
        EmphasisMixin,
        IndexerMixin,
        TitleMixin,
        ]
)

RaimarkPrepassExt = marko.helpers.MarkoExtension(
    renderer_mixins=[
        TitleMixin,
        ]
)
