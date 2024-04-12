from __future__ import annotations

from pathlib import Path
from typing import Callable, TypeAlias

from pandas import Series

from .enums import Spectrum

_registered_filetypes: dict[str, FileType] = {}
_filetypes_priority: dict[str, int] = {}

ReadMethod: TypeAlias = Callable[[Path, str, Spectrum], Series | None]
MetaMethod: TypeAlias = Callable[[Path, str, Spectrum], Series | None]


class FileType:
    def __init__(
        self,
        type_name: str,
        allowed_extensions: list[str] | None,
        read_method: ReadMethod,
        meta_method: MetaMethod,
        accept_extension_rule: Callable[[str], bool] | None = None,
    ) -> None:
        self.name = type_name

        self.allowed_extensions = allowed_extensions

        self.read_method = read_method
        self.meta_method = meta_method

        if accept_extension_rule is None:

            def _aer(e: str, /) -> bool:
                if self.allowed_extensions is None:
                    return False
                return e in self.allowed_extensions

            self.accept_extension_rule = _aer

        elif callable(accept_extension_rule):
            self.accept_extension_rule = accept_extension_rule
        else:
            raise ValueError("Invalid accept extension rule")


class KeyCollisionError(Exception):
    ...


def register_filetype(
    ftype: FileType, *, priority: int = 10, overwrite: bool = False
) -> None:
    """The function adds a filetype to the `_registered_filetypes` dict

    Args:
        ftype (FileType): The FileType object to be added
        priority (int, optional): The priority of the object. FileTypes to be used as
        fallbacks should have a priority equal to 0. Defaults to 10.
        overwrite (bool, optional): If set, overwrites a FileType with the same name.
        Defaults to False.

    Raises:
        KeyCollisionError: If overwrite is set to False (default) and a FileType
        with the same name already exists.
    """
    if not overwrite:
        if ftype.name in _registered_filetypes:
            raise KeyCollisionError(f'Key "{ftype.name}" already exists')

    _registered_filetypes[ftype.name] = ftype
    _filetypes_priority[ftype.name] = priority


def get_filetypes() -> list[FileType]:
    ftypes = list(_registered_filetypes.values())
    ftypes.sort(key=lambda f: _filetypes_priority.get(f.name, 0))

    return ftypes


def get_filetype(key: str | FileType) -> FileType:
    if isinstance(key, str):
        return _registered_filetypes[key]
    elif isinstance(key, FileType):
        return key
    else:
        raise ValueError(f"`{key}` is not a registered filetype")
