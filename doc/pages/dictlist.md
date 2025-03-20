---
kind: deepdive
---

# DictList

A Dictlist is a RAIMAD-special container type
that acts like both a Python dict, list and object all at the same time:

```python exec
import raimad as rai

mydictlist = rai.DictList()

# works like a list
mydictlist.append('foo')
mydictlist.append('bar')
mydictlist.extend(['ayy', 'lmao'])

print(f"{len(mydictlist)=}")
print(f"{mydictlist[0]=}")
print(f"{mydictlist[2]=}")
```

```python exec
# But also like a dict
mydictlist['free'] = 'luigi'
mydictlist['marco'] = 'polo'

print(f"{len(mydictlist)=}")
print(f"{mydictlist[4]=}")
print(f"{mydictlist['free']=}")
print(f"{mydictlist[5] is mydictlist['marco']=}")

for i, item in enumerate(mydictlist.items()):
    print(f"Item {i} = {item}")
```

```python exec
# And also like an object

mydictlist.someattr = 'somevalue'
print(f"{mydictlist.someattr=}")
print(f"{mydictlist.free=}")
print(f"{mydictlist.marco=}")
```

The reason that it's good to know about dictlist is that
it shares a common ancestry with the `.subcompos` and `.marks`
attributes of compos.
The exact inheritance diagram looks like this:

```python exec hide-code

#TODO make this a helper method in raimad or in raidoc

class InheritancePrinter:
    def __init__(self):
        self.allcls = set(self.recurse((
            rai.DictList,
            rai.compo.SubcompoContainer,
            rai.compo.MarksContainer,
            )))

    def recurse(self, cls):
        if isinstance(cls, list | tuple | set):
            for x in cls:
                yield from self.recurse(x)
            return
        if not cls.__module__.startswith('raimad'):
            return
        yield cls
        for x in cls.__bases__:
            yield from self.recurse(x)

    def yield_edges(self):
        for parent in self.allcls:
            for child in self.allcls:
                if child in parent.__bases__:
                    yield f'{child.__name__} -> {parent.__name__}'

    def yield_nodes(self):
        for node in self.allcls:
            yield f'{node.__name__} [label="{str(node)}"]'

    def yield_dot(self):
        yield 'digraph D {'
        #yield 'node [shape=box]'
        yield from self.yield_nodes()
        yield from self.yield_edges()
        yield '}'

    def _repr_dot_(self):
        return '\n'.join(self.yield_dot())

rai.show(InheritancePrinter())

```

```python exec
snowman = rai.Snowman()
print(type(snowman.subcompos))
print(type(snowman.marks))
```

What this means in practice is that there are essentially
two ways to assign a subcompo:
with a name, or without a name.
Using `subcompos.append` and `subcompos.extend`
will assign only an index to the subcompo,
while using `self.subcompos.foo = bar`
or `self.subcompos['foo'] = bar`
will make it accessible with both an index and a name.
The second approach makes it easier for
users of your component to do [[subcompo-introspection.md]].

## Layers/Marks/Options annotations

#TODO no page on annotations yet!

Even though you assign the `Layers`,
`Marks`, and `Options` annotations
as nested classes when you create a component,
when the class gets actually created,
they also become dictlists:

```python exec
print(type(rai.Snowman.Layers))
print(type(rai.Snowman.Options))
print(type(rai.Snowman.Marks))

print(rai.Snowman.Layers[0])
print(rai.Snowman.Layers[0].name)
print(rai.Snowman.Layers['pebble'].name)
print(rai.Snowman.Layers['pebble'].desc)
```

Anyway, hopefully this page clears up some non-trivial
lines you might find in example code,
such as calling `self.subcompos.extend`,
or addressing `self.marks` with both `[index_notation]`
and `.attribute_notation`.

