---
kind: reference
---

# Editing methods overview

This page aims to offer a complete overview of all editing operations
in RAIMAD.

Editing operations are methods of
[Transform](cls_Transform), [Proxy](cls_Proxy),
and [Boundpoint](cls_Boundpoint).
Complete documentation generated from Python docstrings and method
signatures is available in the pages linked above.
Briefly:

- `Transform` objects represent a transformation,
    not tied to any specific Compo.
- `Proxy` objects tie together a Compo and a Transform.
    While the underlying Compo remains immutable,
    a Proxy offers a transformed view into that Compo.
    Proxies can stack on top of each other,
    combining their transformations.
- `BoundPoint` objects represent a point tied to a specific Proxy.
    A BoundPoint provides an ergonomic way to change the origin
    of an applied transformation.
    Rotating around a specifc corner
    or mirroring along a specific vertical line
    are two examples of operations that are easy to do with `BoundPoint`.

## Rotation

| Method  | Transform | Proxy    | Boundpoint |
|---------|-----------|----------|------------|
| protate | ✔         | ✔        |            |
| crotate | ✔         | ✔        |            |
| orotate | ✔         | ✔        |            |
| rotate  | ✔         | ✔        | ✔          |

Rotation takes two inputs: the angle, and the reference point
(the point "around" -- or, in British English, "about" -- which
the rotation is happening).

The angle is given in radians in the counterclockwise
orientation (mathematicians call this "positive orientation").
Python's `math.radians` method can be used to convert from degrees,
and RAIMAD itself provides some aliases TODO not documented!

The reference point can be given as two separate `x` and `y` coordinates
with the `crotate` method,
or as a 2-tuple holding both coordinates in one object using the `protate`
method:

TODO

`rotate` takes either:

TODO

Or none at all (in which case,
the origin of the proxy's coordinate grid
is used as the reference point):

TODO

The `orotate` method allows rotating
by a multiple of 90 degrees
around the origin.
This is useful for avoiding floating point noise -- see
[[coords-transforms.md]].

TODO

Rotating around a `BoundPoint` can be done with the `rotate` method.
Since the `BoundPoint` itself is the reference point,
`protate`, `crotate`, and `orotate` methods are not defined for it.

TODO


## Translation (movement)

| Method  | Transform | Proxy    | Boundpoint |
|---------|-----------|----------|------------|
| pmove   | ✔         | ✔        | ✔          |
| cmove   | ✔         | ✔        | ✔          |
| movex   | ✔         | ✔        | ✔          |
| movey   | ✔         | ✔        | ✔          |
| move    | ✔         | ✔        | ✔          |

Translation takes two arguments:
x and y offset.
As with rotation, we have `cmove` and `pmove` that take
two numbers and one tuple respectively,
and `move`, which takes either.
We also define `movex` and `movey` methods
that take only one coordinate.

All movement methods are defined for all
editing classes.
Since there is no "reference point" for translation,
moving a BoundPoint is the same as moving its Proxy.


## Reflection (flipping)

| Method  | Transform | Proxy    | Boundpoint |
|---------|-----------|----------|------------|
| pflip   | ✔         | ✔        |            |
| cflip   | ✔         | ✔        |            |
| hflip   | ✔         | ✔        | ✔          |
| vflip   | ✔         | ✔        | ✔          |
| flip    | ✔         | ✔        | ✔          |

`hflip` and `vflip` mirror along the horizontal
and vertical axes, respectively TODO check.
A custom vertical or horizontal line can be specified.
`pflip` and `cflip` can mirror along two axes at once,
with the former taking the x and y coordinates separately TODO check,
and the latter taking them as a 2-tuple.
`flip` can take either, defaulting to mirroring along
the X and Y axes.

Mirroring can be done in reference to a `BoundPoint`,
in which case the position of the boundpoint are used as the
axes of mirroring -- either separately using `hflip` and `vflip`,
or both at once with `flip`.
`pflip` and `cflip` are not defined for `BoundPoint`,
since the `BoundPoint` itself is the reference.


## Scaling

| Method  | Transform | Proxy    | Boundpoint |
|---------|-----------|----------|------------|
| apscale | ✔         | ✔        |            |
| acscale | ✔         | ✔        |            |
| ppscale | ✔         | ✔        |            |
| ccscale | ✔         | ✔        |            |
| cpscale | ✔         | ✔        |            |
| pcscale | ✔         | ✔        |            |
| ascale  |           |          | ✔          |
| pscale  |           |          | ✔          |
| cscale  |           |          | ✔          |
| scale   | ✔         | ✔        | ✔          |

Scaling is the most complicated.
It takes an X scale factor, a Y scale factor, and a reference point.
Either can be given as separate coords or a tuple.
Also, a single number can be used as both the X and Y factor.
There are methods for each combination:

| Method  | Scale factor  | Reference point |
|---------|---------------|-----------------|
| apscale | single number | tuple           |
| acscale | single number | two args        |
| ppscale | tuple         | tuple           |
| ccscale | two args      | two args        |
| cpscale | two args      | tuple           |
| pcscale | tuple         | two args        |

`BoundPoint`'s scaling methods take only the factors,
and use the `BoundPoint` itself as the reference point.
Again, the factors can be given as two separate numbers,
a tuple, or a single number for both the X and Y scale.

| Method  |  Reference point |
|---------|------------------|
|  ascale |  single number   |
|  pscale |  tuple           |
|  cscale |  two args        |

Finally, `scale` just works with whatever you throw at it:

TODO


## Aligning Points

`BoindPoint`s have special a special `to` method
exclusive to them,
which transforms the underlying Proxy such that
the `BoundPoint` ends up at specific coordinates.
This is basically a more ergonomic version of `move`,
useful in operations such as connecting "ports" or
couplers of different components
togethers TODO phrasing.
`pto` and `cto` variants are available.

| Method  | Transform | Proxy    | Boundpoint |
|---------|-----------|----------|------------|
| to      |           |          | ✔          |
| pto     |           |          | ✔          |
| cto     |           |          | ✔          |

## Snapping

TODO


