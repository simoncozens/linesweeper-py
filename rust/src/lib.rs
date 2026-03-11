use kurbo::BezPath;
use linesweeper::binary_op as linesweeper_binary_op;
use pyo3::exceptions::PyException;
use pyo3::prelude::*;

/// Performs a boolean operation on two sets of paths.
#[pymodule(name = "linesweeper")]
mod linesweeper_py {
    use super::*;

    #[pyclass(extends=PyException)]
    pub struct LinesweeperError {
        #[pyo3(get, set)]
        pub data: String,
    }

    #[pymethods]
    impl LinesweeperError {
        #[new]
        fn new(data: &str) -> Self {
            LinesweeperError {
                data: data.to_string(),
            }
        }
    }
    impl LinesweeperError {
        fn new_py(data: &str) -> PyErr {
            PyErr::new::<LinesweeperError, _>(data.to_string())
        }
    }

    fn to_bezpath(b: &Bound<'_, PyAny>) -> Result<BezPath, PyErr> {
        let svg_path = b.call_method0("to_svg")?;
        BezPath::from_svg(&svg_path.extract::<String>()?)
            .map_err(|e| LinesweeperError::new_py(&format!("Invalid SVG path: {}", e)))
    }

    fn op_from_string(s: &str) -> Result<linesweeper::BinaryOp, PyErr> {
        match s {
            "union" => Ok(linesweeper::BinaryOp::Union),
            "intersection" => Ok(linesweeper::BinaryOp::Intersection),
            "difference" => Ok(linesweeper::BinaryOp::Difference),
            "xor" => Ok(linesweeper::BinaryOp::Xor),
            _ => Err(LinesweeperError::new_py(&format!(
                "Invalid operation: {}",
                s
            ))),
        }
    }

    fn fill_rule_from_string(s: &str) -> Result<linesweeper::FillRule, PyErr> {
        match s {
            "nonzero" => Ok(linesweeper::FillRule::NonZero),
            "evenodd" => Ok(linesweeper::FillRule::EvenOdd),
            _ => Err(LinesweeperError::new_py(&format!(
                "Invalid fill rule: {}",
                s
            ))),
        }
    }

    #[pyfunction]
    fn _binary_op(
        set_a: Bound<PyAny>,
        set_b: Bound<PyAny>,
        fill_rule: String,
        op: String,
    ) -> PyResult<Vec<String>> {
        let paths_a = to_bezpath(&set_a)?;
        let paths_b = to_bezpath(&set_b)?;
        let fill_rule = fill_rule_from_string(&fill_rule)?;
        let op = op_from_string(&op)?;

        Ok(linesweeper_binary_op(&paths_a, &paths_b, fill_rule, op)
            .map_err(|e| {
                LinesweeperError::new_py(&format!("Error performing boolean operation: {}", e))
            })?
            .contours()
            .map(|c| c.path.to_svg())
            .collect())
    }
}
