# Coordinates and Transformations

RAIMAD's coordinate system works like this:

- the X axis goes from left to right
- the Y axis goes from bottom to top
- Positive angles go counterclockwise
- Negative angles go clockwise
- When talking about rectangles:
    - "length" is the measure on the X axis
    - "width" is the measure on the Y axis

If you are a mathematician,
this should make sense.
If you come from a computer graphics environment,
we sincerely apologize.

## Transformations

You can move, rotate, and scale any RAIMAD compo:

```python exec
import raimad as rai
import numpy as np

class IShapedFilter(rai.Compo):
    def _make(self, beam_length: float = 10.5):
        beam = rai.RectLW(2, beam_length).proxy()
        coup_top = rai.RectLW(10, 2).proxy()
        coup_bot = rai.RectLW(12, 2).proxy()

        coup_top.snap_above(beam)
        coup_bot.snap_below(beam)

        self.subcompos.beam = beam
        self.subcompos.coup_top = coup_top
        self.subcompos.coup_bot = coup_bot

class TransformExample(rai.Compo):
    def _make(self):
        filter = IShapedFilter().proxy()

        moved = filter.copy().move(50, 20)
        scaled = filter.copy().scale(5)
        rotated = filter.copy().rotate(np.deg2rad(90)).scale(4)

        self.subcompos.filter = filter
        self.subcompos.moved = moved
        self.subcompos.scaled = scaled
        self.subcompos.rotated = rotated

show(TransformExample())
        
```

## Snapping and bbox

Each compo has a bounding box (bbox).
It's an imaginary rectangle that encloses the entire geometry of the compo.
One application of bbox are the `snap_above` and `snap_below` functions you've
seen earlier (`snap_left` and `snap_right` also exist).
You can also access the bbox directly with the `.bbox` attribute:

```exec python
# TODO example
```

The tutorial ends here for now.


