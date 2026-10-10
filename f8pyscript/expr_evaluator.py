from __future__ import annotations

from dataclasses import dataclass
from types import CodeType
from typing import Any

from f8pysdk.expressions import evaluate_expression, unwrap_value
from .expr_validator import PYEXPR_ALLOWED_GLOBAL_FNS

try:
    import numpy as np  # type: ignore
except ModuleNotFoundError:
    np = None  # type: ignore[assignment]


_PYEXPR_EVAL_ERRORS = (Exception,)
def _safe_eval_compiled(code: CodeType, *, names: dict[str, Any], allow_numpy: bool) -> Any:
    if allow_numpy and np is None:
        raise RuntimeError("numpy is not available")
    return evaluate_expression(code, names=names, functions=PYEXPR_ALLOWED_GLOBAL_FNS,
                               numpy_module=np if allow_numpy else None)


@dataclass(frozen=True, slots=True)
class PyExprEvalResult:
    value: Any = None
    error: BaseException | None = None


class PyExprEvaluator:
    def evaluate(self, code: CodeType, *, names: dict[str, Any], allow_numpy: bool) -> PyExprEvalResult:
        try:
            value = _safe_eval_compiled(code, names=names, allow_numpy=allow_numpy)
            value = unwrap_value(value)
            return PyExprEvalResult(value=value)
        except _PYEXPR_EVAL_ERRORS as exc:
            return PyExprEvalResult(error=exc)


__all__ = ["PyExprEvalResult", "PyExprEvaluator", "np"]
