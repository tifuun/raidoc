---
kind: tutorial
---

# Collaboration

In order to make it easier for different people to use your
RAIMAD designs,
you can organize them into a *package*.
RAIMAD packages are nothing more the standard Python
packages.
That means you can install them with tools like `pip`.

## Using a RAIMAD package

If you would just like to make use of a RAIMAD package
within your designs,
you can install it using pip.
For example, if you wanted to install
the sample
[`rai_smiley` package](https://github.com/tifuun/rai_smiley),
you could do it like so

```shell
pip install git+https://github.com/tifuun/rai_smiley
```

## Working on other people's repos

If you want to not only use a package,
but also change its code
(for example, if you want to contribute new components to an existing package),
you should first *clone*
the repository using git,
and then install it using pip editable mode,
like so:

```shell
git clone https://github.com/tifuun/rai_smiley
pip install -e ./rai_smiley
```

Installing a package in editable mode means that any changes
that you make in your local copy of the package
will be reflected from within Python when you import it.

The screencast below demonstrates these steps by making a simple
change in the sample
[`rai_smiley`](https://github.com/tifuun/rai_smiley) package.

![screencast demonstrating working on a raimad package](../asciinema/collaboration-smiley.cast)

### Adding new components to an existing package

Python is very permissive in regards to where you put
your code within a package.
Indeed, some <sup>
[1](https://github.com/benjaminp/six/blob/main/six.py),
[2](https://github.com/python/typing_extensions/blob/main/src/typing_extensions.py),
[3](https://github.com/benjaminp/six/blob/main/six.py)
</sup>
prolific packages put all or almost all of their
code within one file.

In RAIMAD, however, to keep things manageable,
we follow the following rule of thumb:

- Any classes (e.g. components) that are useful on their own
    deserve their own separate file.
- Any supporting functions and classes (e.g. subcomponents)
    should share the file with the class that they support.

We also use 
[src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
for RAIMAD packages,
which means that Python source code files go into
`src/package_name/`.

With regards to naming classes and files, we also adhere to
[PEP8](https://peps.python.org/pep-0008/#package-and-module-names).
In short, files should be in `snake_case`,
while classes should be in `UpperCamelCase`.

So, if a package called `rai_filters` contains a component
called `IShapedFilter`,
you should expect to find its source code under
`src/rai_filters/i_shaped_filter.py`,
which might also contain supporting classes/components like
`IShapedFilterCoupler`.

Finally, we use the `__init__.py` files
(which are required to be present in every package directory
by Python)
to perform *namespace flattening*.
Continuing with the `rai_filters` example above,
`src/rai_filters/__init__.py` might include lines like
`from rai_filters.i_shaped_filder import IShapedFilter`
so that users of the package can access the component
as `rai_filters.IShapedFilter`, as opposed to the needlessly
verbose `rai_filters.i_shaped_filter.IShapedFilter`.

The screencast below demonstrates how you can add
a sample `IShapedFilter` component to the `rai_smiley`
package
and update the `__init__.py` file to include the newly
added component.

![screencast that demonstrates adding a new component to a package](../asciinema/collaboration-smiley-new-component.cast)

### A note on `raimad export` syntax

In Python, you use the `.` operator to access child modules
of a module as well as objects within a module.
The `raimad export` command, however,
uses the `.` to access child modules,
and the `:` to access a component class
within a module.

In other words, the last separator is always a ':'
and not a '.'.

So, while you may access the IShapedFilter class
as `rai_smiley.i_shaped_filter.IShapedFilter`
or `rai_smiley.IShapedFilter`
from Python,
when using the `raimad export` command
you would write
`rai_smiley.i_shaped_filter:IShapedFilter`
or `rai_smiley:IShapedFilter`.

## Making your own package

You can also make your own package from scratch.
Make sure to choose a short and informative name
that
[complies with PEP8](https://peps.python.org/pep-0008/#package-and-module-names),
and starts with `rai_`.

After that, by using the sample
[`rai_smiley`](https://github.com/tifuun/rai_smiley)
as a reference,
set up the file structure of your package and upload it to
a git repository.

> [ INFO ]
>
> Are you a TIFUUN collaborator?
> Instead of creating your own package,
> we recommend contributing to one of the two
> existing packages instead.
> Read more on the [TIFUUN collaborator welcome page](tifuun.md).

<!--
## Namespace woes: src layout, classes vs files, \_\_init\_\_.py

This section is meant to clarify some painful confusions
that result
from Python's... *permissive* approach to structuring packages.

### src layout

We prefer that everyone use
[src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)
as opposed to flat layout for RAIMAD packages.

In practice, that means that the root of a repository
will only contain metadata files,
while the actual code will be under
`src/package_name`.

### Classes: one in each file or...?

Unlike, for example, Java, which mandates that each file
only have one (public) class,
Python lets you put your classes wherever you want.
The general rule of thumb that we prefer everyone
uses for RAIMAD is:

- Each independently useful component gets its own file
- Subcomponents that are only useful in the context
    of a larger component can share a file with the component

### File and class naming conventions

Please adhere to
[PEP8](https://peps.python.org/pep-0008/#package-and-module-names)
when naming classes and files.
In short, files should be in `snake_case`,
while classes should be in `UpperCamelCase`.

So, a hypothetical I-Shaped filter component would
be called `IShapedFilter`
and live inside `src/package_name/i_shaped_filter.py`.

### `__init__.py`

The `__init__.py` is a file that must be present
in every directory inside the package,
even if it is empty.

A curious effect of the `__init__.py` file is that
any objects defined in it are available directly
in the module which corresponds to the directory containing
the file.

Example:
- A function called `foo` defined inside `src/mypackage/bar.py`
    is available in the Python interpreter
    as `mypackage.bar.foo`
- A function called `baz` defined inside `src/mypackage/__init__.py`
    is available in the Python interpreter
    as `mypackage.baz`

As explained two sections above,
we prefer to have a separate file for each class.
So if you have a class called `MyCompo`
inside `src/mypackage/mycompo.py`,
it will be available as
`mypackage.mycompo.MyCompo`
in the Python interpreter.

This is suboptimal, because
it requires users of `MyCompo`
to do a lot of unnecessary typing.
We deal with this by doing *namespace flattening*
inside of the `__init__.py` file.

In essence, we put a single import line
`from mypackage.mycompo import MyCompo`
into the top level `__init__.py` file,
which makes `MyCompo` available
from the top level module of the package.
Users of the package are now able to
access the component class
as simply `mypackage.MyCompo`.

Thus, barring special circumstances,
`__init__.py` files inside RAIMAD packages
(and, as a matter of fact,
inside RAIMAD itself)
should only contain import lines used for namespace
flattening,
or be completely empty.
-->



