"""
autogen.py: generate RAIDOC pages from RAIMAD docstrings.

What follows is a brief list of ast.FunctionDef and ast.ClassDef
attributes,
which will hopefully be useful for normal people who don't
spend their days writing custom documentation systems
and consequently don't have these memorized.



"""

from types import ModuleType
import ast
from pathlib import Path
from dataclasses import dataclass
import inspect

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

def ast_unparse_function_signature(func_def):
    """
    Reconstruct function signature from ast.FunctionDef object.
    Tortured out of ChatGPT.
    Pretty sure it has some issues with functions that have positional-only
    or keyword-only args.
    """
    # Get function name
    func_name = func_def.name
    
    # Get arguments and their default values
    args = func_def.args
    arg_strings = []
    
    # Handle positional-only arguments (arguments before '/')
    for posonly_arg in args.posonlyargs:
        if posonly_arg.annotation:
            annotation = ast.unparse(posonly_arg.annotation)  # Get readable annotation
            arg_strings.append(f"{posonly_arg.arg}: {annotation}")
        else:
            arg_strings.append(posonly_arg.arg)

    # Insert '/' if there are positional-only arguments
    if args.posonlyargs:
        arg_strings.append("/")

    # Handle regular positional or keyword arguments (arguments before '*')
    for arg in args.args:
        if arg.annotation:
            annotation = ast.unparse(arg.annotation)  # Get readable annotation
            arg_strings.append(f"{arg.arg}: {annotation}")
        else:
            arg_strings.append(arg.arg)

    # Handle *args (variable positional arguments)
    if args.vararg:
        arg_strings.append(f"*{args.vararg.arg}")

    # Insert '*' if there are keyword-only arguments
    if args.kwonlyargs:
        if args.vararg:
            arg_strings.append("*")  # Insert '*' for keyword-only args after *args

    # Handle keyword-only arguments (arguments after '*')
    for kwonly_arg in args.kwonlyargs:
        if kwonly_arg.annotation:
            annotation = ast.unparse(kwonly_arg.annotation)  # Get readable annotation
            arg_strings.append(f"{kwonly_arg.arg}: {annotation}")
        else:
            arg_strings.append(kwonly_arg.arg)

    # Handle **kwargs (variable keyword arguments)
    if args.kwarg:
        arg_strings.append(f"**{args.kwarg.arg}")
    
    # Handle default values (if any)
    default_start_index = len(args.posonlyargs) + len(args.args) - len(args.defaults)
    for i, default in enumerate(args.defaults):
        # Use ast.unparse to get the default value in a human-readable form
        default_value = ast.unparse(default)
        arg_strings[default_start_index + i] += f" = {default_value}"
    
    # Combine function name and arguments
    signature = f"{func_name}({', '.join(arg_strings)})"
    
    # Add return type annotation (if present)
    if func_def.returns:
        return_annotation = ast.unparse(func_def.returns)
        signature += f" -> {return_annotation}"
    
    return signature

@dataclass
class FunctionDef:
    signature: str
    name: str

    def __init__(self, node):
        signature = ast_unparse_function_signature(node)
        name = node.name

class FileScanner():
    def __init__(self, filesystem_scanner, abspath):
        self.filesystem_scanner = filesystem_scanner
        self.abspath = abspath
        self.md_fragments = []

        self.classes = []
        self.functions = []

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
        self.functions.append(node)

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
        self.classes.append(node)

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

    def print_classes_and_functions(self):
        for scanner in self.file_scanners:
            for cls in scanner.classes:
                print(cls)
            for fn in scanner.functions:
                print(fuck(fn))

@dataclass
class FnDef:
    name: str
    sig: str
    docstring: str
    #module: str

@dataclass
class ClsDef:
    name: str
    docstring: str
    methods: tuple[FnDef]
    #module: str

def scan_public(module):
    functions = []
    classes = []

    for name in module.__all__:
        obj = vars(module)[name]
        if inspect.isclass(obj):
            classes.append(ClsDef(
                name=name,
                docstring=inspect.getdoc(obj),
                methods=tuple(
                    FnDef(
                        name=methname,
                        sig=str(inspect.signature(method)),
                        docstring=inspect.getdoc(method),
                        )
                    for methname, method in vars(obj).items()
                    if
                        not methname.startswith('_')
                        and inspect.isfunction(method)
                    # TODO static/classmethod?
                    )
                ))
        elif inspect.isfunction(obj):
            functions.append(FnDef(
                name=name,
                sig=str(inspect.signature(obj)),
                docstring=inspect.getdoc(obj)
                ))

    return functions, classes

if __name__ == '__main__':
    scan_public()
    #scanner = FilesystemScanner()
    #scanner.use_module(raimad)
    #scanner.scan()
    ##print(scanner.get_md())
    #scanner.print_classes_and_functions()

