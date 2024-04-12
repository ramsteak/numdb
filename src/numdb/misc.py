from typing import TypeVar, Mapping, Any, Iterable

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


def flatten_dict(
    nested_dict: dict[str, Any | dict[str, Any]], *, join_char: str = "."
) -> dict[str, Any]:
    """Flattens a nested dictionary.
    The function takes a nested dict[str, Any] (where the keys are strings) and
    flattens it to a dict where the keys are composed by joining the keys of the
    nested dicts with `join_char`. Values that are not of type dict are preserved.

    Args:
        `nested_dict`: the dictionaty to flatten. Keys of all nested dicts should be str.
        `join_char`: optional, the character used to join the keys when flattening.
            default: "."

    Returns:
        `dict`: The flattened dictionary

    Example:
        >>> nested_dict = {'a': 1, 'b': {'c': 2, 'd': {'e': 3}}}
        >>> flatten_dict(nested_dict)
        {'a': 1, 'b.c': 2, 'b.d.e': 3}
    """

    def walk(_d: dict, prev: tuple[str, ...]) -> Iterable[tuple[tuple[str, ...], Any]]:
        for k, v in _d.items():
            if isinstance(v, dict):
                yield from walk(v, (*prev, k))
            else:
                yield ((*prev, k), v)

    return {join_char.join(ks): v for ks, v in walk(nested_dict, ())}
