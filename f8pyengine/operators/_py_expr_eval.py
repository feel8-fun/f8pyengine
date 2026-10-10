from __future__ import annotations

from types import CodeType
from typing import Any, cast
from f8pysdk.expressions import (
    GLOBAL_FUNCTIONS, MATH_FUNCTIONS, JsonRef as JsonRef,
    compile_expression, evaluate_expression, is_identifier as is_identifier,
    normalize_expr_code as normalize_expr_code, sigmoid as scalar_sigmoid,
    unwrap_value, wrap_value as wrap_value,
)

try:
    import numpy as np
except ModuleNotFoundError:
    np = None


def sigmoid(x: Any) -> Any:
    if np is not None and isinstance(x, (np.ndarray, np.generic)):
        return 1.0 / (1.0 + np.exp(-cast(Any, x)))
    return scalar_sigmoid(x)


ALLOWED_GLOBAL_FNS: dict[str, Any] = {**GLOBAL_FUNCTIONS, "sigmoid": sigmoid}
ALLOWED_MATH_FNS = MATH_FUNCTIONS


def unwrap_wrapped_value(value: Any) -> Any:
    return unwrap_value(value)


def compile_expr(expr: str, *, allow_numpy: bool) -> tuple[CodeType | None, str | None]:
    return compile_expression(expr, functions=ALLOWED_GLOBAL_FNS.keys(), allow_numpy=allow_numpy)


def safe_eval_compiled(code: CodeType, *, names: dict[str, Any], allow_numpy: bool) -> Any:
    if allow_numpy and np is None:
        raise RuntimeError("numpy is not available")
    return evaluate_expression(code, names=names, functions=ALLOWED_GLOBAL_FNS,
                               numpy_module=np if allow_numpy else None)
