# Contributor's guide

> [INFO]
>
> This page is about contributing to RAIMAD.
> The overview for collaborating on RAIMAD packages
> is here: [[collaboration.md]]

If you would like to contribute to RAIMAD,
you are welcome to do so.
We use the
[fork-and-branch](https://blog.scottlowe.org/2015/01/27/using-fork-branch-git-workflow/)
workflow approach.
In short:

1. Create a fork of the
    RAIMAD [repo](https://github.com/tifuun/raimad)
    in GitHub
1. Clone your fork locally with
    `git clone <URL-to-forked-repo>`
1. Add the upstream repository as a remote with
    `git remote add upstream https://github.com/tifuun/raimad`
1. Make a new branch with
    `git checkout -b <new-branch-name>`
1. Make your changes
1. Push your changes to your forked repo with
    `git push origin <new-branch-name>`
    - This should trigger a message from github asking if you
        want to make a pull request.
        Open the pull request, and your contribution
        will be reviewed.
1. After your changes have been merged, do not forget to
    synchronise your `main` branch on the local and remote:
    ```
    git chekout main
    git pull upstream main
    git push origin main
    ```
1. After that, the feature branch can be deleted:
   ```
   git branch -d <new-branch-name>
   git push --delete origin <new-branch-name>
   ```

## Issues, Feature Requests & Bugs 

Feel free to report bugs, request features,
and ask question in the
[github issue tracker](https://github.com/tifuun/raimad/issues)

## Developer Guide

When editing RAIMAD,
you would want to install it in development mode.
From the root of the cloned git repo, run
```
pip install -e .
```

The `-e` flag tells pip to install the code
in the repository directly, without making a copy.
This means that any changes you make to RAIMAD
will be immediately reflected in the `raimad` module
imported with Python.

## Automatic tests

There are automatic tests under the `tests`
directory in the repo.
The tests depend on
[cift](https://github.com/maybeetree/cift),
which is used to validate the CIF files produced
by RAIMAD.
You can install it like so:

```shell
pip install cift
```

After cift is installed,
you can run the unit tests
with Python's standard `unittest` library.
From the root of the repo, execute:

```shell
python -m unittest
```

We also recommend
[pytest](https://docs.pytest.org/en/stable/),
a drop-in replacement for unittest with prettier output
and better integration with Python's
debugger `pdb`.
Pytest, however, should not be a requirement,
and any unit tests that you contribute must work without it.

## Python Versions

RAIMAD supports Python 3.10, 3.11, and 3.12.
Your contributions must work in all of these versions.
To ensure compatibility,
simply run the unit tests in all three versions.

Installing all three versions of Python
locally might prove tedious.
Therefore, we provide a docker container
that you can use to test RAIMAD
in all supported versions.
See the *Docker* section below for more info.

## Tooling

We use some additional tooling to control
RAIMAD's code quality.

### MyPy

[MyPy](https://www.mypy-lang.org/)
is a static type checker for Python.
All code you contribute must be compliant with
MyPy's strict mode.
To check this, install MyPy with pip and tell it to check
the package's source code:

```
pip install mypy
mypy --strict src/raimad
```

Note that we currently do not require the unit tests
to comply with MyPy at all, just the main code.
This might change in the future.

### Ruff

[Ruff](https://docs.astral.sh/ruff/)
is a style checker for Python.
It is *recommended* that code that you contribute
complies with the Ruff style,
but not required.
Contributions that add no features but improve
the style of existing code to comply with Ruff
are also encouraged!

To run Ruff, install it with pip and launch it
from the root of the repo:
```shell
pip install ruff
ruff check
```

### Coverage

[Coverage](https://coverage.readthedocs.io/en/7.6.12/)
is a good tool for making sure that your unit tests
actually cover the code that you write.
It is highly encouraged to have as much as
practical of your contributed code to be covered
by your unit tests.

To use coverage, install it with pip and run it from
the root of the repo:

```
pip install coverage
coverage run -m unittest
```

This will create a `.coverage` file that contains
information about coverage.
You can then use it to generate a short report
right in your terminal:

```
coverage report -i
```

The `-i` flag is needed to ignore errors that result
from unit tests that create temporary Python modules.
We hope to resolve this issue soon.

## Docker

We provide a docker container that can be used to easily
test RAIMAD in all supported Python versions
and run all the tooling.

You can use it by pulling the docker image from github
and running it from the root of the repo
like this:

```
docker pull ghcr.io/maybeetree/raimad-tooling:latest
docker run -v "./:/pwd" raimad-tooling
```

Sample output:
```shell
TOOLING_UNITTEST_3.13=true  # Did unittests pass?
TOOLING_UNITTEST_3.12=true  # Did unittests pass?
TOOLING_UNITTEST_3.11=true  # Did unittests pass?
TOOLING_UNITTEST_3.10=true  # Did unittests pass?
TOOLING_MYPY=true  # Were there NO mypy issues?
TOOLING_COVERAGE=89  # Percentage of codebase covered by tests
TOOLING_TODOS=67  # How many TODOs and FIXMEs are in the code?
TOOLING_RUFF=107  # How many issues reported by ruff?
```

For more information,
please visit the
[raimad-tooling github repo](https://github.com/maybeetree/raimad-tooling.git).

<!--
Another way to use Coverage is by creating a HTML
report that offers line-by-line coverage information:

```
coverage html -i
```

This will create a `htmlcov` directory which you can then
open in a web browser.

> [INFO]
>
> For Linux users:
> 
> If your web browser is installed through Flatpak,
> opening local HTML directories might not be
> straightforward.
> You might need to add sandbox exception for the
> `htmlcov` directory using `flatpak override`
> or a GUI tool like Flatseal.
> Alternatively,
> run `python -m http.server` from within the `htmlcov` directory
> and point your web browser to `http://localhost:8000`.
> Users of Snap might run into similar issues.

## Github Workflows

We use github workflows to generate the badges
on RAIMAD's github page.
You can also use these workflows as a way to run
unit tests and other tools without installing
the dependencies on your local system.

Edit the `on` key at the top of
`.github/workflows/test-lint-check.yml`
to include your feature branch.
Then, when you push to your fork of the repository,
github
should automatically launch unit tests and tooling.
You can check the result in the "Actions" tab.
Make sure to undo your changes to the workflow file
before opening a pull request.

-->

