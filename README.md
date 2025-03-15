# RAIDOC

Notebook-based markdown-powered documentation pages for RAIMAD.

This repository contains the source code for RAIDOC.
If you just want to read the docs,
please visit <https://tifuun.github.io/raidoc/>.

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

If you're on a non-glibc system (e.g. Alpine Linux),
you will also need to install gcc, g++ and some headers
so that pip can compile the dependencies of this project:

```sh
apk add gcc g++ python3-dev musl-dev linux-headers
```

See also the discussion on
[libsass-python](https://github.com/sass/libsass-python/issues/391#issuecomment-2555670485)
about musl wheels

You can then build the documentation like this.
The command MUST be run from the root of the repo.

```sh
python -m raidoc build
```

The output is written to the `build` directory.
Currently, there is no incremental compilation;
the above command rebuilds EVERYTHING.

## Building with podman

You can also build raidoc inside a podman container.

We use podman in a bit of an unusual way:
the container image only has python, pip,
and necessary build tools to compile python
extensions.
Then we just bind-mount raidoc source code,
the python venv, and the output directory into the container.
The advantage of this approach is that you don't have to
re-build your iamge every time you want to re-build raidoc.
More details ara available inthe comments inside the
scripts under the `podman` directory.

Build the image like this:
```shell
podman/build-podman-image.sh
```

And use it to build raidoc like this:
```shell
podman/run-container.sh
```

The first run will take a long time and use a lot of CPU because python
extensions need to be compiled.
Subsequent runs will use the compiled binaries from inside `venv`
and will therefore be much faster.

If there are weird errors, try removing the `venv`
directory in the root of the repo.

You can launch a shell into the container and poke around in it like this:
```shell
podman/run-container.sh sh
```

For example, if you want to uninstall raimad from inside container
(so that the next invocation downloads a newer version),
you can do it like this:
```shell
podman/run-container.sh venv/bin/pip uninstall raimad
```

## Viewing the built website

Once you've built raidoc,
all you need to do to view your local copy
is a http static file server to serve the contents
of the `build` directory.
The easiest way to do this is with python's
built-in `http.server`
module.
Simply run

```
python -m http.server -d build
```

in the root of th repo and then navigate to
`localhost:8000` in your web browser.

This will work regardless of whether you built raidoc natively
or in docker,
since we're just using python as a static file server.



## TODO

- [ ] Capabilities of RAIMARK
    - [ ] Lint references
    - [ ] incremental compilation
    - [ ] references to specific labels or headings
    - [ ] Frontmatter parsing
        - [x] "next" link through frontmatter
        - [x] "previous" link automatic
        - [ ] display journey TOC
    - [ ] API reference generation
- [ ] RAIDOC Content
    - [ ] Deepdive on proxies
    - [ ] Demos of various raimad designs
    - [ ] ...potentially others?
    - [ ] Documentation for maintaining raimad
    - [ ] Documentation for maintaining radoc/raidoc/raimark

## License

Copyright 2024 maybetree

### Documentation

The documentation files in this repository
(i.e. files ending with `.md` under the `doc/pages` directory)
are licensed under the
[GNU Free Documentation License (FDL)](./LICENSE-FDL.txt).

### Code

The code files in this repository,
including all Python code,
CSS and HTML templates, are licensed under the
[GNU General Public License (GPL)](./LICENSE-GPL.txt).

### Code snippets

The code snippets presented in the documentation pages
are licensed under the [CC0 License](./LICENSE-CC0.txt),
allowing you to freely use them in your own projects.


