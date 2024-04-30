# CIF Export Deepdive

The CIF export mechanism is complicated,
so we will go through it step-by-step.

## Basic CIF export with `export_cif`

The easies way to produce a CIF file is with the
`export_cif` function.
You can use it during development and for small components.
Gere is a very simple component called `Towers`.
It consists of two tall boxes.
One box is upright, and the other box is rotated by 10 degrees
around its bottom middle point.

```python exec
import pycif as pc

class Towers(pc.Compo):
    def _make(self):
        upright = pc.RectWH(40, 100).proxy()
        leaning = pc.RectWH(40, 100).proxy()

        upright.move(-50, 0)
        leaning.move(50, 0)

        leaning.bbox.bot_mid.rotate(pc.deg2rad(10))

        self.subcompos.upright = upright
        self.subcompos.leaning = leaning

towers = Towers()
towers_cif = pc.export_cif(towers)

print('`Towers` component:')
show(towers)
print('CIF file produced by `export_cif`:')
print(towers_cif)
```

## A closer look with `CIFExporter`

`export_cif` is just a shorthand for the `CIFExporter`
class.
If we use `CIFExporter` directly,
we can take advantage of the `.as_dot()` method to
make a visual representation of routine calls within the CIF file.

Note that we use `multiplier=1` simply to make the numbers
more readable.

```python exec
exporter_towers = pc.CIFExporter(
    towers,
    multiplier=1
    )
show(exporter_towers.as_dot())
```

By default,
`CIFexporter` applies no optimizations to the CIF export process,
so there are quite a lot of unnecessary subroutines.
However,
this lets us see clearly how CIF subroutines map
to RAIMAD Compos and Proxies.

In the diagram,
rectangle nodes represent subroutines that correspond
to compos,
and nodes with a folded corner represent subroutines that
correspond to proxies.

All following examples will use the tree representation of CIF files.
If you want the raw CIF code,
please consult the appendix at the bottom.

## Copied proxies correspond to re-used subroutines

Now consider a component `LinkedTowers`.
The only difference from `towers` is that
only one `RectWH` object is instantiated.
The `upright` and `leaning` subcomponents
are two proxies that point to the same `RectWH` component.
As a result,
the CIF file also uses only one subroutine to define the rectangle.

```python exec
class LinkedTowers(pc.Compo):
    def _make(self):
        upright = pc.RectWH(40, 100).proxy()

        # leaning = pc.RectWH(40, 100).proxy()
        # don't make a new one, just copy!
        leaning = upright.copy()

        upright.move(-50, 0)
        leaning.move(50, 0)

        leaning.bbox.bot_mid.rotate(pc.deg2rad(10))

        self.subcompos.upright = upright
        self.subcompos.leaning = leaning

linked_towers = LinkedTowers()
show(linked_towers)

exporter_linked_towers = \
    pc.CIFExporter(linked_towers, multiplier=1)
show(exporter_linked_towers.as_dot())
```

## `flatten_proxies` cuts down on the number of subroutines

The default settings of CIFExporter may be good for debugging,
but they produce too many unnecessary subroutines
that bloat the CIF file.
One optimization that can be enabled is called
`flatten_proxies`,
which tells `CIFExporter` to flatten the proxies:

```python exec
exporter_linked_towers_flatten = (
    pc.CIFExporter(
        linked_towers,
        multiplier=1,
        flatten_proxies=True
        )
    )
show(
    exporter_linked_towers_flatten
    .as_dot()
    )
```

Instead of being broken out into separate subroutines,
the transformations are now done directly inside the
root subroutine.

## Save a few bytes with `cif_native`

RAIMAD thinks of polygons as arrays of points.
Some types of polygons can be represented in a more succinct way.
For example, in CIF,
rectangles can be uniquely defined by just two point,
instead of the full four,
using the `B` command.

The `cif_native` option instructs the CIF exporter
to make these types of optimizations whenever possible.

```python exec
print('without `cif_native`:')
show(
    pc.CIFExporter(
        pc.RectWH(10, 50),
        multiplier=1,
        cif_native=False
        ).as_dot()
    )

print('with `cif_native`:')
show(
    pc.CIFExporter(
        pc.RectWH(10, 50),
        multiplier=1,
        cif_native=True
        ).as_dot()
    )
```

Currently, only `RectWH` supports this;
all other compos will still be exported with `P` commands.

## Take it further with `native_inline`

`native_inline` allows you to take advantage of CIF's
ability to define boxes with a custom rotation and position,
eradicating the need for subroutines in some cases:

```python exec
print('The component:')
show(linked_towers)

print('Without `native_inline`:')

exporter = pc.CIFExporter(
    linked_towers,
    multiplier=1,
    flatten_proxies=True,
    cif_native=True,
    native_inline=False,
    )
show(exporter.as_dot())

print('With `native_inline`:')

exporter = pc.CIFExporter(
    linked_towers,
    multiplier=1,
    flatten_proxies=True,
    cif_native=True,
    native_inline=True
    )
show(exporter.as_dot())
```

## Full example

Hear is an example of a toy filterbank with two rows of filters.
Each filter consists of two resonator elements.
In each filter, the right resonator is a copy of the left one
(or, more accurately, they are two proxies pointing to the same
resonator compo).
Similarly, the bottom row is a rotated copy of the top row.

```python exec
import pycif as pc
class CShapedResonator(pc.Compo):
    def _make(
            self,
            beam_length,
            top_coup_length: float = 10,
            bot_coup_length: float = 8,
            thickness: float = 2
            ):

        beam = pc.RectWH(2, beam_length).proxy()
        top_coup = pc.RectWH(top_coup_length, thickness).proxy()
        bot_coup = pc.RectWH(top_coup_length, thickness).proxy()

        top_coup.bbox.mid_left.to(
            beam.bbox.top_right
            - (0, thickness / 2)
            )

        bot_coup.bbox.mid_left.to(
            beam.bbox.bot_right
            + (0, thickness / 2)
            )

        self.auto_subcompos()

class Filter(pc.Compo):
    def _make(
            self,
            compo_resonator,
            separation: float = 10
            ):

        res1 = compo_resonator().proxy()
        res2 = res1.copy()

        res2.snap_right(res1)
        res2.move(separation, 0)

        self.auto_subcompos()

class Filters(pc.Compo):
    def _make(
            self,
            beam_lengths: list[int],
            filt_spacing=80,
            ):

        for i, beam_length in enumerate(beam_lengths):

            resonator_partial = CShapedResonator.partial(
                beam_length=beam_length
                )

            filt = Filter(resonator_partial).proxy()
            # make them aligned on the bottom
            filt.bbox.bot_mid.to((0, 0))
            filt.move(filt_spacing * i, 0)

            self.subcompos[f"filt_{i}"] = filt

class FilterBank(pc.Compo):
    def _make(
            self,
            compo_filters,
            ms_spacing: float = 10
            ):

        filts1 = compo_filters().proxy()
        filts2 = filts1.copy()
        filts2.rotate(pc.semicircle)
        filts2.snap_below(filts1)
        filts2.move(0, -ms_spacing * 2)

        ms_start = pc.midpoint(
            filts1.bbox.bot_left,
            filts2.bbox.top_left,
            )

        ms_end = pc.midpoint(
            filts1.bbox.bot_right,
            filts2.bbox.top_right,
            )

        ms = pc.RectWire(ms_start, ms_end, 2).proxy()

        self.auto_subcompos()

bank = FilterBank(
    compo_filters=(
        Filters.partial(
            beam_lengths=range(10, 50, 10)
            )
        )
    )

print('the component:')
show(bank)

print('CIF file (all optimizations):')
exporter_filterbank = pc.CIFExporter(
    bank,
    multiplier=1,
    flatten_proxies=True,
    cif_native=True,
    native_inline=True
    )
show(exporter_filterbank.as_dot())
```

## Esoteric edgecases

You don't have to read this.
It shouldn't be useful.

### Stacked proxies

It is possible to have components that
contain proxies of proxies (of proxies of proxies....).

Normally, stacked proxies are only created internally by RAIMAD
to allow `BoundPoint`s to work properly.
I don't know why you would want to make stacked proxies
manually in your design, but you can.

Stacked proxies are handled correctly by CIFExporter.

```python exec
class ProxyStack(pc.Compo):
    def _make(self):
        first = pc.RectWH(50, 50).proxy()
        second = first.proxy().move(100, 0)
        third = second.proxy().move(100, 0)

        self.auto_subcompos(locals())

print('The component:')
proxy_stack = ProxyStack()
show(proxy_stack)

print('The CIF file:')
exporter = pc.CIFExporter(proxy_stack, multiplier=1)
show(exporter.as_dot())
```

`flatten_proxies`
is also able to flatten stacked proxies:

```python exec
exporter = pc.CIFExporter(
    proxy_stack,
    multiplier=1,
    flatten_proxies=True
    )
show(exporter.as_dot())
```

### `native_inline` without `flatten_proxies`

It's possible to enable `native_inline` without enabling
`flatten_proxies`.
You end up with a weird middleground where the CIF file
doesn't quite mirror the RAIMAD component structure,
but also isn't very optimized.
I don't know why you would want to do this,
but you can.

```python exec
exporter = pc.CIFExporter(
    proxy_stack,
    multiplier=1,
    cif_native=True,
    flatten_proxies=False,
    native_inline=True,
    )
show(exporter.as_dot())
```

## Appendix: full CIF files

### Towers (`exporter_towers`)
```python exec hide-code
print(exporter_towers.cif_string)
```

### Linked Towers (`exporter_linked_towers`)
```python exec hide-code
print(exporter_linked_towers.cif_string)
```

### Link Towers with `flatten_proxies` (`exporter_linked_towers_flatten`)
```python exec hide-code
print(exporter_linked_towers_flatten.cif_string)
```

### Filterbank (`exporter_filterbank`)
```python exec hide-code
print(exporter_filterbank.cif_string)
```

