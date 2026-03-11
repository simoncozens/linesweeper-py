import pytest
from kurbopy import BezPath
from linesweeper import binary_op, simplify, combine_paths


def test_union():
    path_a = BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z")
    path_b = BezPath.from_svg("M 50,50 L 150,50 L 150,150 L 50,150 Z")
    result = binary_op(path_a, path_b, "nonzero", "union")
    assert len(result) > 0


def test_intersection():
    path_a = BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z")
    path_b = BezPath.from_svg("M 50,50 L 150,50 L 150,150 L 50,150 Z")
    result = binary_op(path_a, path_b, "nonzero", "intersection")
    assert len(result) > 0


def test_difference():
    path_a = BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z")
    path_b = BezPath.from_svg("M 50,50 L 150,50 L 150,150 L 50,150 Z")
    result = binary_op(path_a, path_b, "nonzero", "difference")
    assert len(result) > 0


def test_xor():
    path_a = BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z")
    path_b = BezPath.from_svg("M 50,50 L 150,50 L 150,150 L 50,150 Z")
    result = binary_op(path_a, path_b, "nonzero", "xor")
    assert len(result) > 0


def test_simplify():
    paths = [
        BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z"),
        BezPath.from_svg("M 50,50 L 150,50 L 150,150 L 50,150 Z"),
    ]
    result = simplify(paths)
    assert len(result) > 0


def test_combine_paths():
    paths = [
        BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z"),
        BezPath.from_svg("M 200,200 L 300,200 L 300,300 L 200,300 Z"),
    ]
    combined = combine_paths(paths)
    assert len(combined.elements()) == sum(len(p.elements()) for p in paths)


def test_invalid_operation():
    path_a = BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z")
    path_b = BezPath.from_svg("M 50,50 L 150,50 L 150,150 L 50,150 Z")
    with pytest.raises(Exception):
        binary_op(path_a, path_b, "nonzero", "invalid")


def test_invalid_fill_rule():
    path_a = BezPath.from_svg("M 0,0 L 100,0 L 100,100 L 0,100 Z")
    path_b = BezPath.from_svg("M 50,50 L 150,50 L 150,150 L 50,150 Z")
    with pytest.raises(Exception):
        binary_op(path_a, path_b, "invalid", "union")
