from __future__ import annotations

from .filetypes import get_filetypes, register_filetype
from .enums import Spectrum, XAxisType

from .csv_innospectra import read as _  # noqa: F401
from .opus_bruker import read as _  # noqa: F811, F401

from .reader import read_spectrum

__all__ = [
    "Spectrum",
    "XAxisType",
    "read_spectrum",
    "register_filetype",
    "get_filetypes",
]
