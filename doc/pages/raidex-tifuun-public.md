# Adding your (public) package to RAIDEX

> [ INFO ]
>
> This page is for TIFUUN collaborators.
> If you're an external user who wants to
> add your package to RAIDEX,
> you should contact the [RAIDEX maintainer](people.md) instead.

> [ INFO ]
>
> For this guide we assume that your code is hosted on a
> public github repo, so that your code is available for the world
> to read.
> Do you have a private github repo? Then go to the guide for
> [private packages](raidex-tifuun-private.md)

So, you've
[set up your package](packaging.md)
and want to add it to RAIDEX.
Good!

## Add your package to the requirements file

Clone the
[RAIDEX repository](https://github.com/tifuun/raidex).
Then, open the file `deploy/raidex-packages.txt`
and add a line for your package
in the following format format:

```
git+https://github.com/<user-or-org>/<repo-name>.git
```

So, for example, if the HTTP url to your package is
<https://github.com/tifuun/rai_smiley>,
then you would add
`git+https://github.com/tifuun/rai-smiley.git`

Once you are done, commit your changes and push.

> [ DANGER ]
>
> Since you have write access to the RAIDEX repository,
> it is easy for you to exfiltrate the RAIDEX private key,
> which you can use to read other people's private repositories.
>
> We trust that you do not do this.
>
> We also trust that you follow good cybersecurity practices
> and keep your github account safe.

## Debugging your package deployment
<!-- TODO this section is copy-pasted.
We need snippets!! -->

Once you've pushed your changes to raidex,
a runner should pick up the updated workflow file
and rebuild raidex.
You can check on how it is going in the
"Actions" tab of the raidex repository on github.
If something goes wrong, you can also read the error log there.

> [ INFO ]
>
> If your commit results in a failed build,
> do not panic.
> The last good version of raidex will still be available
> to everyone else.
> Read the error message,
> fix it,
> and push again.

## Optional: publish to PyPI

If you want to make it easier for others to install
your package,
you should publish it to PyPI.
[Python's official documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
goes in-depth on how to do this.
But generally,
it boils down to the following steps:

1. Create a PyPI account
1. Create an API token for your account
1. Install [twine](https://pypi.org/project/twine/)
1. Inside of your package:
    1. `python -m build`
    1. `python -m twine upload dist/rai_yourpackage-x.x.x*`
1. Verify that it worked: `pip install rai_yourpackage`

Once you have your package on pypi,
you can replace your line in the
`raidex-packages.txt` file
with the name of your package.

