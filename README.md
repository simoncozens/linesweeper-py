# linesweeper

Python bindings for the [linesweeper](https://github.com/simoncozens/linesweeper) Rust crate, performing boolean operations on paths (intersection, union, difference, xor). Useful for font development and other vector graphics workflows.

## Install

```
pip install linesweeper
```

## Usage

### Boolean operations on BezPaths

Use `binary_op` to perform boolean operations (union, intersection, difference, xor) on two sets of paths:

```python
from kurbopy import BezPath
from linesweeper import binary_op

# Create two overlapping rectangles as BezPaths
path_a = BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z")
path_b = BezPath.from_svg("M 50,50 L 150,50 L 150,150 L 50,150 Z")

# Union: combine both shapes
result = binary_op(path_a, path_b, "nonzero", "union")

# Intersection: keep only the overlapping region
result = binary_op(path_a, path_b, "nonzero", "intersection")

# Difference: subtract path_b from path_a
result = binary_op(path_a, path_b, "nonzero", "difference")

# Xor: keep non-overlapping regions
result = binary_op(path_a, path_b, "nonzero", "xor")
```

The `fill_rule` parameter can be `"nonzero"` or `"evenodd"`.

### Simplifying paths / removing overlaps

Use `simplify` to merge a list of overlapping BezPaths into a simplified result:

```python
from kurbopy import BezPath
from linesweeper import simplify

paths = [
    BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z"),
    BezPath.from_svg("M 50,50 L 150,50 L 150,150 L 50,150 Z"),
]
simplified = simplify(paths)
```

### Removing overlaps from UFO contours

Use `remove_overlaps` to remove overlapping contours from a UFO glyph, using [ufoLib2](https://github.com/fonttools/ufoLib2):

```python
from ufoLib2 import Font
from linesweeper import remove_overlaps

font = Font.open("MyFont.ufo")

glyph = font["A"]
contours = list(glyph)
glyph.clearContours()
remove_overlaps(contours, glyph.getPen())
```

## API Reference

### `binary_op(set_a, set_b, fill_rule, operation)`

Performs a boolean operation on two `BezPath` objects.

- **set_a** / **set_b**: `kurbopy.BezPath` objects.
- **fill_rule**: `"nonzero"` or `"evenodd"`.
- **operation**: `"union"`, `"intersection"`, `"difference"`, or `"xor"`.
- **Returns**: A list of `BezPath` objects.

### `simplify(bezpaths)`

Simplifies a list of `BezPath` objects by performing a union operation.

- **bezpaths**: A list of `kurbopy.BezPath` objects.
- **Returns**: A list of simplified `BezPath` objects.

### `remove_overlaps(contours, pen)`

Removes overlaps from a list of UFO `Contour` objects and draws the result to a pen.

- **contours**: A list of `ufoLib2.objects.Contour` objects.
- **pen**: A `fontTools.pens.basePen.AbstractPen` to draw the result to.

### `combine_paths(bezpaths)`

Concatenates multiple `BezPath` objects into a single `BezPath`.

- **bezpaths**: A list of `kurbopy.BezPath` objects.
- **Returns**: A single `BezPath`.

## Build from source

This package is built using [maturin](https://www.maturin.rs/), which compiles the Rust code and creates a Python wheel:

```
pip install maturin
maturin develop --release
```

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE.txt](LICENSE.txt) file for details.