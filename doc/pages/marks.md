---
kind: tutorial
---

# Marks

Marks allow the author of a component to
define special points of interest.
For example, the author of an MKID component
can define a mark that specifies where the readout line should
connect.
Marks can be created using the `.marks` property
of a compo,
and they can be accessed through the `.marks` property of
any proxy pointing to that compo.

Similar to `.bbox`,
which you've learned about in
[[subcompos.md]],
the `.marks` property creates boundpoint objects.
Unlike `.bbox`,
which has a set of nine points that are calculated from
the component's geometry,
`.marks` allows the component's author to assign
any number of arbitrarily chosen points:

```python exec hide-output
import raimad as rai

class Filter(rai.Compo):
    def _make(self):
        coupler_top = rai.RectLW(10, 2).proxy()
        coupler_bot = rai.RectLW(12, 2).proxy()
        resonator = rai.RectLW(2, 10).proxy()

        coupler_top.snap_above(resonator)
        coupler_bot.snap_below(resonator)

        # Define the `thz_line_coup` mark
        # as a point 10 units above the top coupler
        self.marks.thz_line_coup = (
            rai.add(
                coupler_top.bbox.top_mid,
                (0, 2)
                )
            )

        # Define the `mkid_coup` mark
        # as a point w units below the bottom coupler
        self.marks.mkid_coup = (
            rai.add(
                coupler_bot.bbox.bot_mid,
                (0, 2)
                )
            )

        self.subcompos.coupler_top = coupler_top
        self.subcompos.coupler_bot = coupler_bot
        self.subcompos.resonator = resonator
```

Users of your component can then access the marks that
you have defined:

```python exec
class MyCompo(rai.Compo):
    def _make(self):
        thz_line = rai.RectLW(100, 2).proxy()
        filter1 = Filter().proxy()
        filter2 = Filter().proxy()

        filter1.marks.thz_line_coup.to(
            thz_line.bbox.bot_left
            )
        filter1.move(20, 0)

        filter2.marks.thz_line_coup.to(
            thz_line.bbox.bot_left
            )
        filter2.move(40, 0)

        self.subcompos.thz_line = thz_line
        self.subcompos.filter1 = filter1
        self.subcompos.filter2 = filter2

mycompo = MyCompo()
rai.show(mycompo)
```

## Annotating marks

It is a good idea to list all of the marks that your
component defines in a special `Marks`
nested class.
Similar to Python's type annotations,
this will have no effect on the functionality of
your component,
but it will help other humans and programs
that might use it:

```python exec hide-output
import raimad as rai

class Filter(rai.Compo):
    class Marks:
        thz_line_coup = rai.Mark("THZ Line goes here")
        mkid_coup = rai.Mark("MKID coupler goes here")

    def _make(self):
        ...
```
