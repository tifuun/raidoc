---
kind: howto
---

# KLayout layer properties

RAIMAD has support for creating
[KLayout's `lyp` (layer properties) files](https://www.klayout.de/lyp_format.html).

This page provides a brief overview of these capabilities.
For exhaustive documentation
(different layer properties and their values;
builtin dither pattern names;
builtin line pattern names),
please read the KLayout docs,
or consult
[`src/raimad/cif/lyp.py`](https://github.com/tifuun/raimad/blob/main/src/raimad/cif/lyp.py).

Layer properties can be assigned to an object using
the `_experimental_lyp` dict, mapping
CIF layer names
(not RAIMAD layer names -- see [[cif-layer-names.md]])
to `rai.lyp.Properties` objects:

<!--
```python exec
import os
#os.mkdir('/play/raidoc/tmp')
lastdir = os.getcwd()
os.chdir('/play/raidoc/tmp')
```
-->

```python
import raimad as rai

class Foo(rai.Compo):
    _experimental_lyp = {
        'RED': rai.lyp.Properties(
            fill_color='#ff0000',
            frame_color='#00ffff',
            width=2,
            ),
        'BLUE': rai.lyp.Properties(
            fill_color='#0000ff',
            frame_color='#ffaa00',
            width=5,
            ),
        }

    def _make(self):
        self.subcompos.append(rai.RectLW(10, 10).proxy().map('red'))
        self.subcompos.append(rai.RectLW(10, 10)
            .proxy().movex(20).map('blue'))
```

The `.lyp` file needs to be exported separately from the `.cif` file:

```python
compo = Foo()

rai.export_cif(compo, 'foo.cif')
rai.export_lyp(compo, 'foo.lyp')
```

In KLayout, the `.lyp` file can be loaded using
File > Load Layer Properties:

![]({{webroot}}img/doc/lyp/lyp-basic.png)

Dither patterns and line stipples are supported too.
`rai.lyp.dithers` and `rai.lyp.lines` are DictLists
(see [[dictlist.md]]), so you may use `.attribute`
syntax.
Some dither and lines names, however,
contain spaces and dashes,
so you need to use `['index']` syntax to access these. 

```python
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
<!--

```python exec
compo = Foo()

rai.export_cif(Foo(), 'foo.cif')
rai.export_lyp(Foo(), 'foo.lyp')
```
-->

![]({{webroot}}img/doc/lyp/lyp-dither.png)

RAIMAD also ships with some custom dither patterns not available
in standard KLayout:

```python exec
for idx, name in enumerate(rai.cif.lyp.raidithers.keys()):
    print(f"{idx}: {name}")
```

```python
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

<!--
```python exec
rai.export_cif(Demo(), 'foo.cif')
rai.export_lyp(Demo(), 'foo.lyp')
```
-->

![]({{webroot}}img/doc/lyp/lyp-raidithers.png)
 

User-defined dither patterns and lines are possible too:

```python
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

class Custom(rai.Compo):
    _experimental_lyp = {
        'FOO': rai.lyp.Properties(
            line_style=rai.lyp.CustomLineStyle(
                name='ascii',
                pattern='*.*..*.*.....**..*..**..**.**...',
                ),
            width=5,
            dither_pattern=bowtie,
            ),
        }
    def _make(self):
        self.subcompos.r1 = rai.RectLW(4, 4).proxy().map('foo')

#rai.export_cif(Foo())
#rai.export_lyp(Foo())
```


<!--
```python exec
rai.export_cif(Custom(), 'cust.cif')
rai.export_lyp(Custom(), 'cust.lyp')
```
-->

![]({{webroot}}img/doc/lyp/lyp-custom.png)

<!--
```python exec
os.chdir(lastdir)
```
-->

