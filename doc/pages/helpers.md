# Helpers

RAIMAD defines some helper functions.
These are used internally in RAIMAD,
but you can also use them for your own benefit.

## Geometric helpers

```python exec
import raimad as rai
import numpy as np

print( rai.midpoint( np.array((-10, -10)), np.array((12, 12)) ))
print( rai.polar( np.deg2rad(90), 5 ).round())
print( np.rad2deg(
    rai.angle_between( np.array((0, 10)), np.array((2, 2)) )
    ))

```

<!-- TODO angspace, others -->

## Iteration helpers

> [ SEEALSO ]
> Python's [itertools](https://docs.python.org/3/library/itertools.html)
> module also contains some useful iteration helpers.

### Overlapping

```python exec
print(list( rai.iters.duplets( range(10) )))
print(list( rai.iters.triplets( range(10) )))
print(list( rai.iters.quadlets( range(10) )))
print(list( rai.iters.quintlets( range(10) )))

# Custom number
print(list( rai.iters.overlap( 3, range(10) )))
```

### Non-overlapping

```python exec
print(list( rai.iters.couples( range(10) )))
print(list( rai.iters.triples( range(10) )))
print(list( rai.iters.quadles( range(10) )))
print(list( rai.iters.quintles( range(10) )))

# Custom number
print(list( rai.iters.nonoverlap( 3, range(10) )))
```

### Flatten and Braid

```python exec
print( list( rai.flatten( [[[1, 2, 3], [4, 5], [6], 7], 8, 9, 10] )))

print( list( rai.braid( 'abc', [1,2,3], 'あえい' )))

```

### Testers

```python exec
print( rai.iters.is_rotated( [1, 2, 3], [1, 2, 3] ))
print( rai.iters.is_rotated( [1, 2, 3], [2, 3, 1] ))
print( rai.iters.is_rotated( [1, 2, 3], [3, 2, 1] ))
print( rai.iters.is_rotated( [1, 2, '3'], ['3', 1, 2] ))
print( rai.iters.is_rotated( [1, 2, '3'], [3, 1, 2] ))
print( rai.iters.is_rotated(
    [1, 2, '3'],
    [3, '1', 2],
    comparison=lambda a, b: list(map(str, a)) == list(map(str, b))
    ))
```

## Generator decorators
Sometimes you don't care about the lazy-loading aspect of generators
and you just want to use them for the nice `yield` syntax.
In these cases,
`preload_generator` and `join_generator`
come in handy.

```python exec
@rai.preload_generator()
def mygen():
    yield 1
    yield 2
    yield 4

print(mygen()[2])

@rai.join_generator('\n and ')
def mygen():
    yield 'hello'
    yield 'world'
    for x in range(3):
        yield 'foo'
        yield 'bar'

print(mygen())
```

## Other helpers

```python exec
print( rai.custom_base(10, ['O', 'I']), bin(10) )

```

