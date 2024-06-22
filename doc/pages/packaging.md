# Packaging

Packaging your components allows others to easily use them.

> [ INFO ]
>
> Are you a TIFUUN collaborator?
> Instead of creating your own package,
> we recommend contributing to one of the two
> existing packages instead.
> Read more on the [TIFUUN collaborator welcome page](tifuun.md).
>
> If you're not a TIFUUN collaborator or if you have a good reason
> to make your own package, read on.

RAIMAD packages are just Python packages,
so if you already know how to make Python packages,
you have a good headstart.
If you don't,
I'll do my best to explain.

## Choosing a name for your package

You should choose a short and informative name for your package.
In addition to the
[PEP8 requirement](https://peps.python.org/pep-0008/#package-and-module-names)
of using only lowercase letters,
we also require all RAIMAD packages to start with `rai_`
in order to make it clear that the package contains RAIMAD components.

## Set up your package

You can use
[`rai_smiley`](https://github.com/tifuun/rai_smiley)
as an example of how to set up a package.
If you've never made a Python package before,
you can read through the README file,
which hopefully explains everything.

## Add to RAIDEX

[RAIDEX](https://tifuun.github.io/raidex/)
is RAIMAD's package index.
It allows users to easily discover existing components.
It is highly encouraged to add your package to RAIDEX.

### Add RAIDEX metadata

> [ WORKINPROGRESS ]
>
> I'm still writing this section.

Once you've added the relevant metadata,
read the README on
[RAIDEX's gitub](https://github.com/tifuun/raidex)
for setting up RAIDEX locally.
This will allow you to see how your components will look like
on the publc RAIDEX instance,
and help you catch any errors.

Once you're satisfied with how you package looks in RAIDEX,
you can contact the [RAIDEX maintainer](people.md) to publish it.

> [ INFO ]
>
> Are you a TIFUUN collaborator?
> If so, you can add your package to RAIDEX directly,
> without going through the RAIDEX mainteiner.
> [Learn how](raidex-tifuun-public.md)

