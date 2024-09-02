"""autogen.py: generate RAIDOC pages from RAIMAD docstrings."""

from types import ModuleType
import ast
from pathlib import Path
from dataclasses import dataclass

import raimad

def docstring_to_md(docstring):
    if docstring is None:
        return '*Missing docstring*\n\n'
    return ''.join((
        *(
            f"> {line.lstrip()}\n> \n" if line.strip('-') else ''
            for line in docstring.split('\n')
            ),
        '\n\n'
        ))

class FileScanner():
    def __init__(self, filesystem_scanner, abspath):
        self.filesystem_scanner = filesystem_scanner
        self.abspath = abspath
        self.md_fragments = []

    @property
    def relpath(self):
        return self.abspath.relative_to(
            self.filesystem_scanner.root_path
            )

    def scan(self):
        tree = ast.parse(self.abspath.read_text())

        self.md_fragments.append(
            f"# File `{self.relpath}`\n\n"
            )
        self.md_fragments.append(
            docstring_to_md(ast.get_docstring(tree))
            )

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                self.scan_function_def(node)

            elif isinstance(node, ast.ClassDef):
                if node.name in {'Options', 'Layers', 'Marks'}:
                    # Do not generate docs for
                    # the options/layers/marks annotation classes.
                    #
                    # TODO check if this is actually
                    # a nested class?
                    continue
                self.scan_class_def(node)

    def scan_function_def(self, node):
        self.md_fragments.append(
            f"## Function `{node.name}`\n\n"
            )

        self.md_fragments.append("```python\n")
        self.md_fragments.append(
            ast.unparse(node).split('\n', 1)[0]
            .replace(', ', ',\n\t')
            )
        self.md_fragments.append("\n```\n\n")
        # TODO this breaks on decorators, etc.
        # Better reconstruct it by hands
        # from node.args, node.name, node.decorator_list,
        # etc.

        self.md_fragments.append(
            docstring_to_md(ast.get_docstring(node))
            )

    def scan_class_def(self, node):
        self.md_fragments.append(
            f"## Class `{node.name}`\n\n"
            )
        self.md_fragments.append(
            docstring_to_md(ast.get_docstring(node))
            )
        # TODO methods

    def get_md(self):
        return ''.join(self.md_fragments)

class FilesystemScanner():
    def __init__(self):
        #self.visited = set()
        self.root_path = None
        self.md_fragments = []
        self.file_scanners = []

    def use_module(self, module):
        self.root_path = Path(module.__path__[0])

    def scan_file(self, abspath):
        file_scanner = FileScanner(self, abspath)
        self.file_scanners.append(file_scanner)
        file_scanner.scan()

    def scan(self):
        for path, dirnames, filenames in self.root_path.walk():
            if not '__init__.py' in filenames:
                continue

            for filename in filenames:
                self.scan_file(path / filename)

    def get_md(self):
        return ''.join((
            *self.md_fragments,
            *(scanner.get_md() for scanner in self.file_scanners)
            ))


if __name__ == '__main__':
    scanner = FilesystemScanner()
    scanner.use_module(raimad)
    scanner.scan()
    print(scanner.get_md())

