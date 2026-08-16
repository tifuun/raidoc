---
kind: howto
---

# KLayout layer properties

RAIMAD has support for creating
[KLayout's `lyp` (layer properties) files](https://www.klayout.de/lyp_format.html).
Layer properties can be assigned to an object using
the `_experimental_lyp` dict, mapping
CIF layer names
(not RAIMAD layer names -- see [[cif-layer-names.md]])
to `rai.lyp.Properties` objects:

```python exec
import raimad as rai

class Foo(rai.Compo):
    _experimental_lyp = {
        'RED': rai.lyp.Properties(
            fill_color='#ff0000',
            frame_color='#00ffff',
            ),
        'BLUE': rai.lyp.Properties(
            fill_color='#0000ff',
            frame_color='#ffaa00',
            xfill=True,
            ),
        }

    def _make(self):
        self.subcompos.append(rai.RectLW(10, 10).proxy().map('red'))
        self.subcompos.append(rai.RectLW(10, 10)
            .proxy().movex(20).map('blue'))
```

Dither patterns and line stipples are supported too.
`rai.lyp.dithers` and `rai.lyp.lines` are DictLists
(see [[dictlist.md]]), so you may use `.attribute`
syntax.
Some dither and lines names, however,
contain spaces and dashes,
so you need to use `['index']` syntax to access these. 

```python exec
class Foo(rai.Compo):
    _experimental_lyp = {
        'ROOT': rai.lyp.Properties(
            fill_color='#ff0000',
            frame_color='#00ffff',
            dither_pattern=rai.lyp.dithers.pyramids,
            line_style=rai.lyp.lines['short dash-dotted'],
            width=5,
            ),
        }

    def _make(self):
        self.subcompos.append(rai.RectLW(10, 10).proxy())
```

RAIMAD also ships with some custom dither patterns not available
in standard KLayout:

```python exec
class Demo(rai.Compo):

    _experimental_lyp = {
        f'A{i}': rai.cif.lyp.Properties(dither_pattern=pattern)
        for i, pattern
        in enumerate(rai.cif.lyp.raidithers.values())
        }

    def _make(self) -> None:
        for i, name in enumerate(rai.cif.lyp.raidithers.keys()):

            x = i % 4 * 70
            y = i // 4 * 70

            print(f"{x}, {y}: {name}")

            self.subcompos.append(
                rai.RectLW(64, 64)
                .proxy()
                .move(x, y)
                .map(f'A{i}')
                )
```
 

User-defined dither patterns and lines are possible too:

```
bowtie = rai.cif.lyp.CustomDitherPattern(
    name='bowtie',
    lines=(
        '****....',
        '****....',
        '**..**..',
        '**..**..',
        '..**..**',
        '..**..**',
        '....****',
        '....****',
    )
)

class Foo(raimad.Compo):
    _experimental_lyp = {
        'FOO': raimad.lyp.Properties(
            line_style=raimad.lyp.CustomLineStyle(
                name='ascii',
                pattern='*.*..*.*.....**..*..**..**.**...',
                ),
            width=5,
            dither_pattern=bowtie,
            ),
        }
    def _make(self):
        self.subcompos.r1 = raimad.RectLW(4, 4).proxy().map('foo')

#rai.export_cif(Foo())
#rai.export_lyp(Foo())
```


