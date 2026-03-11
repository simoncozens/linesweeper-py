from .linesweeper import _binary_op, LinesweeperError
from kurbopy import BezPath
from typing import List
from ufoLib2.objects import Contour
from fontTools.pens.basePen import AbstractPen


def combine_paths(bezpaths: List[BezPath]) -> BezPath:
    """Combines multiple BezPaths into a single one by concatenating their elements."""
    combined = BezPath()
    for path in bezpaths:
        for element in path.elements():
            combined.push(element)
    return combined


def binary_op(
    set_a: BezPath, set_b: BezPath, fill_rule: str, operation: str
) -> List[BezPath]:
    """Performs a boolean operation on two sets of paths.

    Arguments:
        set_a: The first set of paths.
        set_b: The second set of paths.
        fill_rule: The fill rule to use ("nonzero" or "evenodd").
        operation: The boolean operation to perform ("union", "intersection", "difference", or "xor").
    """
    svgs = _binary_op(set_a, set_b, fill_rule, operation)
    bezpaths = [BezPath.from_svg(svg) for svg in svgs]
    return bezpaths


def simplify(bezpaths: List[BezPath]) -> List[BezPath]:
    """Simplifies a list of BezPaths by performing a union operation on them."""
    combined = combine_paths(bezpaths)
    return binary_op(combined, BezPath(), "nonzero", "union")


def remove_overlaps(contours: List[Contour], pen: AbstractPen):
    """Removes overlaps from a list of contours by performing a union operation on them."""
    bezpaths = []
    for contour in contours:
        bezpaths.extend(BezPath.from_drawable(contour))
    simplified_paths = simplify(bezpaths)
    for path in simplified_paths:
        path.draw(pen)
