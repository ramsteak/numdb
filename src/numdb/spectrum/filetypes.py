from __future__ import annotations
from pathlib import Path
from pandas import Series
from .enums import Spectrum, XAxisType
from typing import Callable

_registered_filetypes: dict[str, FileType] = {}

class FileType:
    def __init__(
        self,
        type_name: str,
        allowed_extensions: list[str] | None,
        read_method: Callable[[Path, str, Spectrum], tuple[Series, XAxisType] | None],
        meta_method: Callable[[Path, str], tuple[Series] | None],
        accept_extension_rule: Callable[[str], bool] | None = None,
    ) -> None:
        self.name = type_name

        self.allowed_extensions = allowed_extensions

        self.read_method = read_method

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


def register_filetype(ftype: FileType, *, overwrite: bool = False) -> None:
    if not overwrite:
        if ftype.name in _registered_filetypes:
            raise KeyCollisionError(f'Key "{ftype.name}" already exists')

    _registered_filetypes[ftype.name] = ftype


def get_filetypes():
    return _registered_filetypes.keys()
