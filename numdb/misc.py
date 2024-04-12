from typing import Any, Iterable, Mapping, TypeVar

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")


def merge_dict(*ds: dict[_K, _V]) -> dict[_K, _V]:
    """The function merges the given dicts into a single dict. In case of key
    collisions the function keeps the value in the first dict where the key is found.

    Args:
        dict[_K, _V]: The dicts to merge

    Returns:
        dict[_K, _V]: The merged dict

    Notes:
        If no dict is passed returns an empty dict.

    Example:
        >>> a = {"one":1, "two":2}
        >>> b = {"two":3, "tre":3}
        >>> merge_dict(a, b)
        {'two': 2, 'tre': 3, 'one': 1}
    """
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
        `nested_dict`: the dict to flatten. Keys of all nested dicts should be str.
        `join_char`: optional, the character used to join the keys when flattening.
            default: "."

    Returns:
        `dict`: The flattened dict

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
