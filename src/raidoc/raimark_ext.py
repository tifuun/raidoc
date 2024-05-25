import subprocess
import re

import marko


class CodeCTX:
    def __init__(self):
        self.globs = {}
        self.locs = {}


class LinkMixin(object):
    """
    Change markdown links that point to `.md` files
    into ones that point to `.html` files
    TODO don't touch non-local links, also validate links
    """

    def render_link(self, element):
        return '<a href="{}">{}</a>'.format(
            self.escape_url(element.dest.replace('.md', '.html')),
            self.render_children(element)
            )


re_callout_class = re.compile(r'\s*\[\s*(\w+)\s*\]\s*')


class CalloutMixin(object):
    """
    """

    def render_quote(self, element):
        callout_tag = element.children[0].children[0].children

        # Remove the tag from rendered outout
        element.children[0].children[0].children = ''

        print(callout_tag)
        match = re_callout_class.match(callout_tag)
        print(match)
        if not match:
            return super().render_quote(element)

        callout_class = match.groups()[0].lower()

        rendered_children = []
        for i, child in enumerate(element.children):
            rendered_children.append(super().render(child))

        return ''.join((
            f'<blockquote class="{callout_class}">',
            *rendered_children,
            '</blockquote>',
            ))


codeblock_preamble = """
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
                    self.escape_html(block_string),
                    '</pre>',
                    )))

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
    renderer_mixins=[LinkMixin, CodeBlockMixin, CalloutMixin]
)

