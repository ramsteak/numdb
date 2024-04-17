from __future__ import annotations

from .enums import Spectrum, XAxisType
from .filetypes import get_filetypes, register_filetype
from .ftypereader import _FTYPEREADER  # noqa: F401
from .reader import read_spectrum, set_reader_defaults

__all__ = [
    "Spectrum",
    "XAxisType",
    "read_spectrum",
    "register_filetype",
    "get_filetypes",
    "set_reader_defaults",
]
