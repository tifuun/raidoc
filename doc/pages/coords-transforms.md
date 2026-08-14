---
kind: tutorial
---

# Coordinates and Transformations

RAIMAD's coordinate system works like this:

- the X axis goes from left to right.
- the Y axis goes from bottom to top.
- Angles are measured in radians.
- Increasing the angle goes counterclockwise.
- Decreasing the angle goes clockwise.
- Angle 0 is in the positive X direction.
- When talking about rectangles:
    - "length" is the measure on the X axis.
    - "width" is the measure on the Y axis.

If you are a mathematician,
this should feel familiar.
If you come from a computer graphics background,
we sincerely apologize.

## Transformations are done with Proxies

RAIMAD compos are immutable.
You cannot transform them.
However, what you can do,
is create a Proxy.
Proxies are like lenses that apply transformations to compos.
The compo itself remains unchanged,
but looking at it through a proxy changes how it looks to you.

```python exec
from math import radians
import raimad as rai

square = rai.RectLW(10, 10)

square_translated = square.proxy().move(15, 0)
square_stretched = square.proxy().scale(1.5, 0.5)
square_rotated = square.proxy().rotate(radians(15))

rai.show(square)
rai.show(square_translated)  # won't be visible because of autocrop
rai.show(square_stretched)
rai.show(square_rotated)
```

## Multiple transformations

There are three ways to combine transformations.
First of all, you can simply chain the different
transformation methods on top of each other:


```python exec
square_multiple = (
    square.proxy()
    .move(15, 0)
    .scale(1.5, 1)
    )

rai.show(square_multiple)
```

This method is preferred, 
because it is easiest to type.


Unlike compos, proxies are mutable,
so you can perform the various methods on separate lines:
```python exec
square_multiple.rotate(radians(-15))
rai.show(square_multiple)
```

Finally, you can create proxies of proxies:
```python exec
square_big = square_multiple.proxy().scale(2)
rai.show(square_big)
```

Applying a transformation to a proxy of a proxy only
affects the topmost proxy.
So the `square_multiple` proxy is unaffected
by the `.scale(2)` call above:

```python exec
rai.show(square_multiple)
```

## Angle aliases

As you've seen before, `.rotate` takes an angle in radians.
Python's `math.radians` can be used to convert degrees to radians.
RAIMAD also defines some aliases for common angles:

```python exec
from math import degrees

print(degrees( rai.fullcircle ))
print(degrees( rai.halfcircle ))
print(degrees( rai.quartercircle ))
print(degrees( rai.eigthcircle ))
```

British English variants are available too:

```python exec
print(degrees( rai.fullcircle ))
print(degrees( rai.semicircle ))
print(degrees( rai.demisemicircle ))
print(degrees( rai.hemidemisemicircle ))
```

## Orthogonal rotations

The `.orotate` method rotates the Proxy by an integer multiple
of 90 degrees in the counterclockwise direction,
*without* invoking trigonometric functions.
This can be used to avoid floating-point noise.

```python exec
rect = rai.RectLW(20, 10)
rect_orot = rect.proxy().orotate(1)
show(rect)
show(rect_orot)
print(f"{rect.bbox.as_list() = }")
print(f"{rect_orot.bbox.as_list() = }")
```

The `.bbox` method returns a bounding box
(this is explained later in [[subcompos.md]]).
As you can see, the values are exact,
both in the original Compo and its rotated Proxy.
Compare with using regular `.rotate`:

```python exec
rect_rot = rect.proxy().rotate(rai.quartercircle)
show(rect)
show(rect_rot)
print(f"{rect.bbox.as_list() = }")
print(f"{rect_rot.bbox.as_list() = }")
```


## Adding and subtracting points

<!-- TODO boundpoint page -->

RAIMAD uses Python tuples
(and sometimes its own BoundPoint class,
which you will learn about later)
to store coordinate points.
You cannot add and subtract tuples using the familiar
`+` and `-` operators.
Instead, you can use `rai.add` and `rai.sub` helpers:

```python exec
my_point = (5, 5)
left = rai.add(my_point, (-2, 0))
below = rai.sub(my_point, (0, 2))

print("My point: ", my_point)
print("To the left: ", left)
print("Above: ", below)
```

There is also `rai.midpoint`, which calculates
the midpoint by averaging the X and Y values:

```python exec
print("Midpoint: ",
    rai.midpoint(
        (0, 6),
        (6, 0)
        )
    )
```

If you really want to use infix notation,
you can. But please don't.

```python exec
sum = (5, 5) |rai.add| (1, 3)
midpoint = (5, 5) |rai.midpoint| (1, 3)

print("Sum: ", sum)
print("Midpoint: ", midpoint)
```

## More editing methods

[[editing-methods-overview.md]] gives a complete overview
of editing methods.
It's recommended to consult that page after completing the tutorial.



