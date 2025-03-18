---
kind: tutorial
---


# Adding your (private) package to RAIDEX

> [ INFO ]
>
> This page is for TIFUUN collaborators.
> If you're an external user who wants to
> add your package to RAIDEX,
> you should contact the [RAIDEX maintainer](people.md) instead.

> [ INFO ]
>
> For this guide we assume that your code is hosted on a
> private github repo,
> so that only people of your choosing can view your
> source code.
> Do you have a public github repo? Then go to the guide for
> [public packages](raidex-tifuun-public.md).
>
> Are your components part of the `rai_compos_pub` or `rai_compos_priv`
> packages? Then you do not need to do anything; those repos are already
> configured for RAIDEX.
> Check the README files for more info.


So, you've
[set up your package](packaging.md)
and want to add it to RAIDEX.
Good!

## Add deploy key

If you package is hosted on a private github repo,
you need to grant RAIDEX access to that repo.
This can be done through so-called "deploy keys".

1. Navigate to the "settings" tab in the top bar of your repo page
1. Navigate to "deploy keys" under "security" in the sidebar
1. Click "add deploy key"
1. Add the RAIDEX public key

The RAIDEX public key is as follows:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEd6Zx1h9EnoLZDJDSiU78kMbzMxCRZwOoBiHdIndHjs
```

## Add your package to the requirements file

Next, clone the
[RAIDEX repository](https://github.com/tifuun/raidex).
Then, open the file `deploy/raidex-packages.txt`
and add a line for your package
in the following format format:

```
git+ssh://git@github.com/<user-or-org>/<repository-name>.git
```

So, for example, if the HTTP url to your package is
<https://github.com/tifuun/rai_smiley>,
then you would add
`git+ssh://git@github.com/tifuun/rai_smiley.git`

Once you are done, commit your changes and push.

> [ DANGER ]
> Since you have write access to the RAIDEX repository,
> it is easy for you to exfiltrate the RAIDEX private key,
> which you can use to read other people's private repositories.
>
> We trust that you do not do this.
>
> We also trust that you follow good cybersecurity practices
> and keep your github account safe.

## Debugging your package deployment

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

