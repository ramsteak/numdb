from __future__ import annotations

from .enums import Spectrum, XAxisType
from .filetypes import get_filetypes, register_filetype
from .ftypereader import _FTYPEREADER
from .reader import read_spectrum

__all__ = [
    "Spectrum",
    "XAxisType",
    "read_spectrum",
    "register_filetype",
    "get_filetypes",
]
