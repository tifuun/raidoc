# Layers

Components can have multiple layers.
Layers are identified by their name, which is a string.
All layer names should consist of lowercase letters, digits, and underscores.
You use the `.map()` method to map different subcomponents
to different layers.

<!-- TODO enfore layer naming in RAIMAD -->

```python exec
import raimad as rai

class Antenna(rai.Compo):
    def _make(self):
        reflector = rai.Circle(20).proxy().map('gnd')
        active = rai.CustomPoly((
            (0, 5),
            (10, -5),
            (10, 5),
            (0, -5),
            )).proxy().map('conductor')

        active.bbox.mid.to(
            reflector.bbox.mid)

        self.subcompos.reflector = reflector
        self.subcompos.active = active

antenna = Antenna()
show(antenna)
```

> [WORKINPROGRESS]
>
> Work in progress:
> The RAIDOC component preview currently draws all layers in the same color,
> so you can't really tell which polygon is on which layer.
> We will fix this Soon (TM).
> For now, you can export the component as CIF to verify that layers
> do indeed work.

## Layer maps

All of the [builtin components](builtin-compos.md)
have only one layer, `root`.
If your component has multiple layers,
you can pass a dict to `.map()` in order to assign each of the child
component layers to parent component layers.
For example, a component like `Antenna` may define abstract layer names
such as `gnd` and `conductor`,
while your toplevel design might define them as concrete materials,
like `al` and `nbtin`.
The keys of the dict are the child layer names,
and the values are the parent layer names.

```python exec
class MySpectrometer(rai.Compo):
    def _make(self):
        antenna = Antenna().proxy().map({
            'conductor': 'nbtin',
            'gnd': 'al',
            })

        # Add other subcomponents...

        self.subcompos.antenna = antenna

spec = MySpectrometer()
show(spec)
```

> [INFO]
>
> Passing a single string to `.map()` when the child component has multiple
> layers will flatten them.
> Passing `None` to `.map()` (or simply not calling `.map()`) will propagate
> all of the child layers to the parent.
>
> Does your component only have one layer, and you can't think of
> a good name for it?
> If that's the case, then just call it `root`.

## Annotating layers

You should declare which layers your component will have
by creating a nested class called `Layers` within your component class.
Please include the layer's name and a brief description of what it is.
You will learn later why this is important to include.

```exec python hide-output
class Antenna(rai.Compo):

    class Layers:
        gnd = rai.Layer('Ground plane')
        conductor = rai.Layer('Conductor layer for antenna's active element')

    def _make(self):
        reflector = rai.Circle(20).proxy().map('gnd')
        active = rai.CustomPoly((
            (0, 5),
            (10, -5),
            (10, 5),
            (0, -5),
            )).proxy().map('conductor')

        active.bbox.mid.to(
            reflector.bbox.mid)

        self.subcompos.reflector = reflector
        self.subcompos.active = active

class MySpectrometer(rai.Compo):

    class Layers:
        al = rai.Layer('Aluminium ground plane')
        nbtin = rai.Layer(
            'Niobium-titanium-nitride layer deposited by electrobeam'
            )

    def _make(self):
        antenna = Antenna().proxy().map({
            'conductor': 'nbtin',
            'gnd': 'al',
            })

        # Add other subcomponents...

        self.subcompos.antenna = antenna
```

The tutorial ends here for now.

