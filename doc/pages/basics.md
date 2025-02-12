# The Basics of RAIMAD

Creating components in RAIMAD is as simple as...

```python exec
import raimad as rai

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

coup1 = IShapedFilter()
rai.show(coup1)
```

Once you've made your basic components
(or, as we call them, "compos"),
you can put them together into larger compos:

```python exec
class Filterbank(rai.Compo):
    def _make(self):
        
        for index, length in enumerate((10.5, 11.7, 12.8)):
            filt = IShapedFilter(beam_length = length).proxy()
            filt.bbox.bot_mid.to((17 * index, 0))
            self.subcompos[f"filt_{index}"] = filt

        thz_line = rai.RectWire(
            self.subcompos.filt_0.bbox.bot_left,
            self.subcompos.filt_2.bbox.bot_right,
            width=2
            ).proxy()

        thz_line.move(0, -4)

        self.subcompos.thz_line = thz_line

bank = Filterbank()
rai.show(bank)
```

## Exporting components

There are two ways to export components:
though Python code,
or from the command line using the `raimad` command.

To export a component from within Python,
pass it to `raimad.export_cif()` method:

```python
import raimad as rai

class MyCompo(rai.Compo):
    ...

# Create instance
mycompo = MyCompo()

# Export to `mycompo.cif`
rai.export_cif(mycompo)
```

To use the `raimad` command, invoke it as
`raimad export <module>:<compo>`,
as demonstrated in the screencast below:

![screencast demonstrating the raimad export command](../asciinema/raimad-cli-export.enhance.cast)

More extensive use of `raimad export` is covered in
[[collaboration.md]].



