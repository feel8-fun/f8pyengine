from __future__ import annotations

from types import CodeType
from typing import Any
from f8pysdk.expressions import ExpressionValidator, compile_expression


PYEXPR_ALLOWED_GLOBAL_FNS: dict[str, Any] = {
    "abs": abs,
    "float": float,
    "int": int,
    "min": min,
    "max": max,
    "round": round,
}

PYEXPR_ALLOWED_MATH_FNS: frozenset[str] = frozenset(
    {
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "atan2",
        "sqrt",
        "log",
        "log10",
        "exp",
        "floor",
        "ceil",
    }
)


class PyExprValidator(ExpressionValidator):
    def __init__(self, *, allow_numpy: bool) -> None:
        super().__init__(functions=PYEXPR_ALLOWED_GLOBAL_FNS.keys(),
                         math_functions=PYEXPR_ALLOWED_MATH_FNS, allow_numpy=allow_numpy)


def compile_pyexpr(expr: str, *, allow_numpy: bool) -> tuple[CodeType | None, str | None]:
    return compile_expression(expr, functions=PYEXPR_ALLOWED_GLOBAL_FNS.keys(),
                              math_functions=PYEXPR_ALLOWED_MATH_FNS, allow_numpy=allow_numpy)


__all__ = ["PYEXPR_ALLOWED_GLOBAL_FNS", "PYEXPR_ALLOWED_MATH_FNS", "PyExprValidator", "compile_pyexpr"]
