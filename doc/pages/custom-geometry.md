---
kind: tutorial
---

# Custom Geometry

There are two ways to create components with arbitrary polygons.
The first way is by using `raimad.CustomPoly`:

```python exec
import raimad as rai

mypoly = rai.CustomPoly((
    (0, 0),
    (50, 20),
    (10, -20)
    ))
rai.show(mypoly)
```

A little bit of a hidden feature of `CustomPoly` is that
it's possible to define in-place marks:

```python exec
class MyCompo(rai.Compo):
    def _make(self):
        carrot1 = rai.CustomPoly((
                (0, 20),
                ("tip", (50, 0)),
                (0, -20)
            )).proxy()

        carrot2 = rai.CustomPoly((
                (0, 10),
                ("tip", (-50, 0)),
                (0, -10)
            )).proxy()

        carrot2.marks.tip.to(carrot1.marks.tip)

        self.subcompos.append(carrot1)
        self.subcompos.append(carrot2)

rai.show(MyCompo())
```

## Raw geometry

Another way to make custom geomtry
is by accessing your compo's `self.geoms` dict directly.
This works on a lower level than `rai.CustomPoly` and allows for more
flexibility.
In fact, it's how all of the built-in RAIMAD components are constructed.

`self.geoms` is a dict mapping layer names to layer contents.
The layer contents are a list of polygons,
and every polygon is itself a list of coordinate pairs.


```python exec
class RobotFace(rai.Compo):
    def _make(self):
        self.geoms = {
            'eyes': [
                [ # Left eye
                    (0, 0),
                    (10, 0),
                    (10, 10),
                    (0, 10),
                    ],
                [ # right eye
                    (20, 00),
                    (30, 00),
                    (30, 10),
                    (20, 10),
                    ],
                ],
            'mouth': [
                [
                    (-10, -20),
                    (40, -20),
                    (40, -30),
                    (-10, -30),
                    ],
                ]
            }

rai.show(RobotFace())
```

If you're making a geometrically complex component
with few clear hierarchical boundaries,
it might be easier to implement it by using `self.geoms` directly
rather through subcompos.

As a final note, you might wonder whether it's possible
to combine both styles of making components -- i.e.
to have a component that both defines geometry manually with `self.geoms`
*and* adds subcomponents with `self.subcompos`.

The answer is that it's possible, but discouraged.

