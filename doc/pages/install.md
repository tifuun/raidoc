---
kind: tutorial
---

# Installing RAIMAD

RAIMAD is a Python package that supports Python 3.12, 3.11, and 3.10.
You can install it with `pip`:

```shell
pip install raimad
```

## Check the installation worked

RAIMAD ships with a sample Snowman component.
You can try exporting the snowman to a CIF file to check that
RAIMAD is installed correctly:


```python exec
import raimad as rai
snowman = rai.Snowman()
rai.show(snowman)
```

The `rai.show()` command should open KLayout and display the snowman.
[KLayout](https://www.klayout.de/) is highly recommended.
is a CIF viewer recommended for use with RAIMAD.
If you don't want to install KLayout,
you can directly export the snowman
to a file of your choosing:

```python
import raimad as rai

rai.export_cif(rai.Snowman(), '/path/to/output/file.cif')
```

## Dependencies

RAIMAD depends only on the `typing-extensions` module,
which `pip` will install automatically.

## RAIMAD in Jupyter

It is discouraged but possible to use RAIMAD
in Jupyter.
The [documentation page](jupyter.md) provides
some relevant information.

## Windows paths

This tutorial assumes a unix-like operating system.
If you are using RAIMAD in windows, please
take note of the following difference:

Windows uses the backslash `\` as a Path separator.
To prevent Python from interpreting backslashes in path strings
as escape sequences, either double them or put an `r` before
the opening quote:

```python
mypath1 = "C:\\Path\\To\\File.cif"
mypath2 = r"C:\Path\To\File.cif"
```

If you're writing code that you intend to share with others,
consider using Python's built-in
[pathlib](https://docs.python.org/3/library/pathlib.html)
module for cross-platform compatibility.


<!--
### A note on this tutorial: screencasts

Throughout this tutorial, you will encounter
pre-recorded screencasts that demonstrate certain
actions.

In these screencasts, we use a POSIX-like terminal
environment
for tasks like cloning repositories,
editing files,
and invoking RAIMAD.

We do this because it's more concise, universal,
and accessible
than screen recordings of graphical interfaces.

If you're coming from Windows and aren't familiar
with POSIX,
don't fret,
it's rather simple!
The screencast below gives a demonstration.

And keep in mind, these screencasts are for
demonstration purposes.
You can use whatever tools you like to achieve the same
goals.

![An example screencast](../asciinema/asciinema-demo.cast )
-->

