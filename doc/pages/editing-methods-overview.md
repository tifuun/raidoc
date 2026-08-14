---
kind: reference
---

# Editing methods overview

This page aims to offer a complete overview of all editing operations
in RAIMAD.

Editing operations are methods of
[Transform](cls_Transform), [Proxy](cls_Proxy),
and [Boundpoint](cls_BoundPoint).
Complete documentation generated from Python docstrings and method
signatures is available in the pages linked above.

These two automatic test files in the RAIMAD repo
may provide additional insight:

- [`test_new_editing.py`](https://github.com/tifuun/raimad/blob/editing-extratest/tests/test_new_editing.py)
- [`test_new_editing_table.py`](https://github.com/tifuun/raimad/blob/editing-extratest/tests/test_new_editing_table.py)

<!-- TODO point to main branch once editing-extratest is merged-->

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

The reference point can be given as two separate `x` and `y` coordinates
with the `crotate` method,
or as a 2-tuple holding both coordinates in one object using the `protate`
method:

```python exec
import raimad as rai

# annular sector 1/8 of a circle wide facing towards positive y
ansec = rai.AnSec.from_auto(
    r1=40, r2=50,
    thetamid=rai.quartercircle, 
    dtheta=rai.eigthcircle,
    )

# original
show(ansec)

# rotate around origin with
# coords given as two separate arguments
r1 = ansec.proxy().crotate(rai.quartercircle, 0, 0)
show(r1)

# rotate around ansec's middle with
# coords given as a tuple
r2 = ansec.proxy().protate(rai.quartercircle, (0, 45))
show(r2)

# The difference between these two invocations
# won't be visible in the preview because of autocrop,
# but it does change where they end up:
print(f"{r1.bbox.mid = }")
print(f"{r2.bbox.mid = }")

```

`rotate` takes either:

```python exec
# original
show(ansec)

# tuple
r1 = ansec.proxy().rotate(rai.quartercircle, (0, 0))
show(r1)

# or separate coords
r2 = ansec.proxy().rotate(rai.quartercircle, 10, 10)
show(r2)

print(f"{r1.bbox.mid = }")
print(f"{r2.bbox.mid = }")

```

Or none at all (in which case,
the origin of the proxy's coordinate grid
is used as the reference point):

```python exec
# explicitly specify origin
r1 = ansec.proxy().rotate(rai.quartercircle, 0, 0)
show(r1)

# don't specify a reference point
r2 = ansec.proxy().rotate(rai.quartercircle)
show(r2)

# The two transformations are identical
print(f"{r1.bbox.mid = }")
print(f"{r2.bbox.mid = }")
```

The `orotate` method allows rotating
by a multiple of 90 degrees
around the origin.
This is useful for avoiding floating point noise -- see
[[coords-transforms.md]].

```python exec
rect = rai.RectLW(20, 10)
rect_orot = rect.proxy().orotate(1)
show(rect)
show(rect_orot)
print(f"{rect.bbox.as_list() = }")
print(f"{rect_orot.bbox.as_list() = }")
```

Rotating around a `BoundPoint` can be done with the `rotate` method.
Since the `BoundPoint` itself is the reference point,
`protate`, `crotate`, and `orotate` methods are not defined for it.

```python exec
# original
show(ansec)

# rotate around ansec's middle (explicit coordinates)
r1 = ansec.proxy().rotate(rai.quartercircle, 0, 45)
show(r1)

# Same thing but using bbox.mid
r2 = ansec.proxy().bbox.mid.rotate(rai.quartercircle)
show(r2)

print(f"{r1.bbox.mid = }")
print(f"{r2.bbox.mid = }")

```


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

`hflip` flips horizontally (mirrors along the vertical axis).
`vflip` flips vertically (mirrors along the horizontal axis).
A custom vertical or horizontal line can be specified.
`cflip` and `pflip` can mirror along two axes at once,
with the former taking the x and y coordinates separately,
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

```python exec
sn = rai.Snowman()
show(sn)
show(sn.proxy().acscale(0.2, 0, 0))
show(sn.proxy().apscale(0.1, (0, 0)))
show(sn.proxy().ppscale((0.1, 0.2), (0, 0)))
show(sn.proxy().ccscale(0.2, 0.1, 0, 0))
```

`BoundPoint`'s scaling methods take only the factors,
and use the `BoundPoint` itself as the reference point.
Again, the factors can be given as two separate numbers,
a tuple, or a single number for both the X and Y scale.

| Method  |  Reference point |
|---------|------------------|
|  ascale |  single number   |
|  pscale |  tuple           |
|  cscale |  two args        |

```python exec
show(sn)
s1 = sn.proxy().bbox.top_right.pscale((0.2, 0.1))
s2 = sn.proxy().bbox.bot_left.cscale(0.2, 0.1)

# Same scale factors...
show(s1)
show(s2)

# But different locations due to different
# reference point
print(f"{s1.bbox.mid = }")
print(f"{s2.bbox.mid = }")
```

Finally, `scale` just works with whatever you throw at it:

```python exec

# All of these scale by a factor of 0.2
# on X and Y around the origin

show(sn.proxy().scale(0.2))
show(sn.proxy().scale(0.2, 0, 0))
show(sn.proxy().scale(0.2, (0, 0)))
show(sn.proxy().scale(0.2, 0.2, 0, 0))
show(sn.proxy().scale((0.2, 0.2), (0, 0)))
```


## Aligning Points

`BoindPoint`s have special a special `to` method
exclusive to them,
which transforms the underlying Proxy such that
the `BoundPoint` ends up at specific coordinates.
This is basically a more ergonomic version of `move`,
useful in operations that have a sense of "connecting"
or "overlapping"
things together.
`pto` and `cto` variants are available.

| Method  | Transform | Proxy    | Boundpoint |
|---------|-----------|----------|------------|
| to      |           |          | ✔          |
| pto     |           |          | ✔          |
| cto     |           |          | ✔          |

```python exec
class Foo(rai.Compo):
    def _make(self):
        center = rai.RectLW(40, 40).proxy()
        left = rai.RectLW(20, 20).proxy()
        right = left.proxy()

        left.bbox.mid.to(center.bbox.bot_left)
        right.bbox.mid.to(center.bbox.bot_right)

        self.subcompos.append(center)
        self.subcompos.append(left)
        self.subcompos.append(right)

show(Foo())
```


## Snapping

| Method      | Transform | Proxy    | Boundpoint |
|-------------|-----------|----------|------------|
| snap\_left  |           |  ✔       |            |
| snap\_right |           |  ✔       |            |
| snap\_above |           |  ✔       |            |
| snap\_below |           |  ✔       |            |

Proxies have snapping methods that let you connect them to other
proxies as if they had magnets.
You can snap things above, below, to the left, and to the right of each other.
See [[coords-transforms.md]] and [[cls_Proxy]] for more info.

```python exec
class Foo(rai.Compo):
    def _make(self):
        center = rai.RectLW(40, 40).proxy()
        left = rai.RectLW(20, 20).proxy()
        right = left.proxy()

        left.snap_left(center)
        right.snap_right(center)

        self.subcompos.append(center)
        self.subcompos.append(left)
        self.subcompos.append(right)

show(Foo())
```

