from typing import TypeVar
from typing import Mapping
from typing import Any

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")

def dict_merge(*ds: dict[_K, _V]) -> dict[_K, _V]:
    """Merges the dicts into a single dict, keeping the priority in the order
    they are specified"""
    merged = {}
    for d in reversed(ds):
        merged.update(d)
    return merged

def get_first(
    property: str,
    *vs: _T | None | dict[str, _T | Any | None],
    default: _T | None = ...,
) -> _T | None:
    for item in vs:
        if item is None:
            continue

        if isinstance(item, Mapping):
            if property not in item:
                continue
            v = item[property]
            if v is None:
                continue
            return v

        return item
    else:
        if default is ...:
            raise ValueError(f"Property {property} not defined")
        return default
