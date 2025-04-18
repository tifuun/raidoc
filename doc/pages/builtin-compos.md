---
kind: tutorial
---

# Builtin Compos

You've already seen `RectLW` in [The Basics of RAIMAD](basics.md),
a compo that represents a rectangle defined by length and width.
RAIMAD offers four more built-in compos for you to use in your
designs:

```python exec
import raimad as rai

from math import radians

RectLW = rai.RectLW(100, 50)

circle = rai.Circle(radius=40)

ansec = rai.AnSec(
    theta1=radians(45),
    theta2=radians(180),
    r1=50,
    r2=80,
    )

rectwire = rai.RectWire(
    (0, 0),              # start point
    (80, 80),            # end point
    10                   # width
    )

triangle = rai.CustomPoly([
    (0, 0),
    (80, 0),
    (40, 80)
    ])

rai.show(RectLW)
rai.show(circle)
rai.show(ansec)
rai.show(rectwire)
rai.show(triangle)
```

## AnSec

`AnSec` is short for "Annular Sector"
which is how mathematicians say "pizza crust".
There are many different ways to define an `AnSec`:

```python exec
# Explicitly define inner radius, outter radius,
# angle one, and angle two

ansec = rai.AnSec.from_auto(
    theta1=radians(45),
    theta2=radians(180),
    r1=50,
    r2=80,
    )
rai.show(ansec)
```

```python exec
# Make it go the other way

ansec = rai.AnSec.from_auto(
    theta1=radians(45),
    theta2=radians(180),
    r1=50,
    r2=80,
    )
rai.show(ansec)
```

```python exec
# Instead of giving an explicit outter radius and second angle,
# define radius delta and angle delta

for x in (10, 40, 60):
    ansec = rai.AnSec.from_auto(
        theta1=radians(0),
        dtheta=radians(x * 3),
        r1=50,
        dr=x,
        )
    rai.show(ansec)
```

For more information about AnSec,
check the [API reference](autogen/cls_AnSec.md).

## RectWire

Similar to AnSec, there are multiple possible ways to define a
RectWire: point-point-width, and point-angle-length-width.


```python exec
rw = rai.RectWire.from_points(
    (0, 0),              # start point
    (100, 80),           # end point
    10                   # width
    )
rai.show(rw)
```

```python exec
from math import radians
rw = rai.RectWire.from_polar(
    (0, 0),              # start point
    radians(-45),        # angle
    80,                  # length
    10                   # width
    )
rai.show(rw)
```

Instantiation `RectWire` directly is the same as using
`RectWire.from_points`.
For more information, see the [API reference](autogen/cls_RectWire.md).

<!-- FIXME wikilinks don't need fullpath but mdlinks do!?!?! -->

