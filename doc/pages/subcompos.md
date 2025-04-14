---
kind: tutorial
---


# Subcompos

You can create complex components which themselves consist of other components.
To do this, you simple define a class that inherits from `rai.Compo`
and defines a `_make()` method that builds your component:

```python exec
import raimad as rai

class Antenna(rai.Compo):
    def _make(self):

        # Create a reflector
        reflector = rai.Circle(20).proxy()

        # Create the active element
        active_element = rai.CustomPoly((
            (0, 5),
            (10, -5),
            (10, 5),
            (0, -5),
            )).proxy()

        # register the reflector and driven element
        # as subcompos

        self.subcompos.reflector = reflector
        self.subcompos.active_element = active_element

antenna = Antenna()
rai.show(antenna)
```

Note that you cannot register compos as subcompos directly.
You must create proxies.

## Legible transformations with BoundPoints

<!-- TODO dont-autocrop method -->

Notice how the antenna's active element in the example above
is not quite aligned to the circle?
As you've learned in [[coords-transforms.md]],
you can use `Proxy().move()` method to adjust its position.

However, RAIMAD offers a better way to do transformations
called BoundPoints.

A boundpoint is simply an XY coordinate pair
with a few special methods that allow the user to perform
transformations *in reference to* that point.

One way to get a boundpoint to a proxy is by using its
bounding box.
The bounding box, or `bbox`,
is simply an upright rectangle that fits the entirety of a
component within itself.
It can be accessed using the `.bbox` property:


```python exec

rect = rai.RectLW(10, 20).proxy()

rai.show(rect)
print("The center is at:\n", rect.bbox.mid)
print("The bottom left corner is at:\n", rect.bbox.bot_left)
print("The middle of the right edge is at:\n", rect.bbox.mid_right)
```

As you can see, the objects returned by the `.bbox` property
are not regular tuples,
but BoundPoints that hold a reference back to the proxy
that was used to create them.

BoundPoints support all of the transformations that you learned about in
[[coords-transforms.md]].
While transforming a proxy directly causes the transformation to be
applied in reference to the origin of the proxy's coordinate system,
applying a transformation through a boundpoint causes
it to be applied in relation to that point:

```python exec
from math import radians

rect = rai.RectLW(10, 20).proxy()

rai.show(rect)

rect1 = rect.proxy().bbox.bot_right.rotate(radians(15))
rai.show(rect1)

rect2 = rect.proxy().bbox.top_left.rotate(radians(15))
rai.show(rect2)
```

BoundPoints also have a special `.to(point)` method,
which translates the proxy such that the boundpoint
is in the same place as `point`:

```python exec
from math import radians

rect = rai.RectLW(10, 20).proxy()

rai.show(rect)

rect1 = rect.proxy().bbox.bot_right.to((5, 5))
rai.show(rect1)
```

Using bounding box boundpoints, we can fix
out `Antenna` component and line up the reflector
and active element:


```python exec
import raimad as rai

class Antenna(rai.Compo):
    def _make(self):

        # Create a reflector
        reflector = rai.Circle(20).proxy()

        # Create the active element
        active_element = rai.CustomPoly((
            (0, 5),
            (10, -5),
            (10, 5),
            (0, -5),
            )).proxy()

        print(
            "The middle of the reflector is at:",
            tuple(reflector.bbox.mid)
            )

        print(
            "The middle of the active element is at:",
            tuple(active_element.bbox.mid)
            )

        # Now lets align them!!
        reflector.bbox.mid.to(
            active_element.bbox.mid
            )

        # Now they're at the same point!
        assert rai.eq(
            reflector.bbox.mid,
            active_element.bbox.mid
            )

        # register the reflector and driven element
        # as subcompos
        self.subcompos.reflector = reflector
        self.subcompos.active_element = active_element

antenna = Antenna()
rai.show(antenna)
```

## Snapping

You can also snap components together based on their
bounding boxes.
This allows for rapidly building components
out of smaller building blocks without
any magic numbers or tedious coordinate calculations:

```python exec
class IShapedFilter(rai.Compo):
    def _make(self):
        coupler_top = rai.RectLW(10, 2).proxy()
        coupler_bot = rai.RectLW(12, 2).proxy()
        resonator = rai.RectLW(2, 10).proxy()

        coupler_top.snap_above(resonator)
        coupler_bot.snap_below(resonator)

        self.subcompos.coupler_top = coupler_top
        self.subcompos.coupler_bot = coupler_bot
        self.subcompos.resonator = resonator

class FilterReadout(rai.Compo):
    def _make(self):
        coupler = rai.RectLW(12, 2).proxy()
        short = rai.RectLW(2, 5).proxy()
        line = rai.RectLW(2, 10).proxy()

        bend = rai.CustomPoly(((0, 0), (2, 0), (0, 2)))
        bend_right = bend.proxy()
        bend_left = bend.proxy().vflip()

        bend_left.snap_left(coupler)
        bend_right.snap_right(coupler)
        short.snap_below(bend_left)
        line.snap_below(bend_right)

        self.subcompos.coupler = coupler
        self.subcompos.short = short
        self.subcompos.line = line
        self.subcompos.bend_left = bend_left
        self.subcompos.bend_right = bend_right

class FilterWithReadout(rai.Compo):
    def _make(self):
        filter = IShapedFilter().proxy()
        readout = FilterReadout().proxy()

        readout.snap_below(filter)
        readout.move(0, -4)  # Add a small gap

        self.subcompos.readout = readout
        self.subcompos.filter = filter

filter_with_readout = FilterWithReadout()
rai.show(filter_with_readout)
```

<!-- TODO emptybboxerror ask if you forgot to register subcompos? -->

<!-- TODO rotating and scaling around points -->

