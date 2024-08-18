# Helpers

RAIMAD defines some helper functions.
These are used internally in RAIMAD,
but you can also use them for your own benefit.

## Geometric helpers

```python exec
import raimad as rai
import numpy as np

print( rai.midpoint( np.array((-10, -10)), np.array((12, 12)) ))
print( rai.polar( np.deg2rad(90), 5 ))
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

## Other helpers

```python exec
print( rai.custom_base(10, ['O', 'I']), bin(10) )

```

