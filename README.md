# RAIDOC

Notebook-based markdown-powered documentation pages for RAIMAD.

This repository contains the source code for RAIDOC.
If you just want to read the docs,
please visit
[github pages](http://example.com).

## Building

First, you need to go and install [graphviz](https://graphviz.org/).
You can check that it works by running the `dot` command:

```sh
$ dot --version
dot - graphviz version 10.0.1 (0)
```

After you have `dot` working, install RAIDOC like any other Python package
by cloning this repository:

```sh
git clone https://github.com/maybeetree/raidoc.git
cd raidoc
python -m pip install -e .
```

You can then build the documentation like this:

```sh
python -m raidoc build
```

The output is written to the `build` directory.
Currently, there is no incremental compilation;
the above command rebuilds EVERYTHING.

## TODO

- [ ] Lint references
- [ ] incremental compilation
- [ ] references to specific labels or headings
- [ ] Frontmatter parsing
    - [ ] "next" link through frontmatter
    - [ ] "previous" link automatic

