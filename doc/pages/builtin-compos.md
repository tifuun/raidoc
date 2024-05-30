# Builtin Compos

You've already seen `RectWH` in [The Basics of RAIMAD](basics.md),
a compo that represents a rectangle defined by width and height.
RAIMAD offers four more built-in compos for you to use in your
designs:

```python exec
import raimad as rai
import numpy as np

rectwh = rai.RectWH(100, 50)

circle = rai.Circle(radius=40)

ansec = rai.AnSec(
    theta1=np.deg2rad(45),
    theta2=np.deg2rad(180),
    r1=50,
    r2=80,
    orientation=rai.Orientation.POS,
    )

rectwire = rai.RectWire(
    (0, 0),              # start point
    (80, 80),            # end point
    10                   # thickness
    )

triangle = rai.CustomPoly([
    (0, 0),
    (80, 0),
    (40, 80)
    ])

show(rectwh)
show(circle)
show(ansec)
show(rectwire)
show(triangle)
```

## AnSec

`AnSec` is short for "Annular Sector"
which is how mathematicians say "pizza crust".
There are many different ways to define an `AnSec`:

```python exec
# Explicitly define inner radius, outter radius,
# angle one, and angle two

ansec = rai.AnSec(
    theta1=np.deg2rad(45),
    theta2=np.deg2rad(180),
    r1=50,
    r2=80,
    orientation=rai.Orientation.POS,
    )
show(ansec)
```

```python exec
# Make it go the other way

ansec = rai.AnSec(
    theta1=np.deg2rad(45),
    theta2=np.deg2rad(180),
    r1=50,
    r2=80,
    orientation=rai.Orientation.NEG,
    )
show(ansec)
```

```python exec
# Instead of giving an explicit outter radius and second angle,
# define radius delta and angle delta

for x in (10, 40, 60):
    ansec = rai.AnSec(
        theta1=np.deg2rad(0),
        dtheta=np.deg2rad(x * 3),
        r1=50,
        dr=x,
        orientation=rai.Orientation.POS,
        )
    show(ansec)
```

For all the options that AnSec takes,
go read it's source code.

> [ WORKINPROGRESS ]
> We will soon have documentation pages for all RAIMAD classes and functions.
> But for now, if you want to learn more about a class or function,
> you should go read its docstring.

Next up: [Coordinates and Transformations](coords-transforms.md)

