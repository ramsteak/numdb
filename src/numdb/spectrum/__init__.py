from __future__ import annotations

from .filetypes import get_filetypes, register_filetype
from .enums import Spectrum, XAxisType
from .reader import read_spectrum

# Imports in order to load files
from .ftypereader import _FTYPEREADER


__all__ = [
    "Spectrum",
    "XAxisType",
    "read_spectrum",
    "register_filetype",
    "get_filetypes",
]
