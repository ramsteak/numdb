from pathlib import Path
from struct import error
from typing import Any

import numpy as np
from brukeropusreader import read_file
from numpy import typing as npt
from pandas import Series

from ...misc import flatten_dict
from ..conversions import spectrum_conversion
from ..enums import Spectrum, XAxisType
from ..filetypes import FileType


def _get_modestr(mode: Spectrum) -> str:
    match mode:
        case Spectrum.AB:
            return "AB"
        case Spectrum.TR:
            return "TR"
        case Spectrum.SM:
            return "ScSm"
        case Spectrum.IGSM:
            return "IgSm"
        case Spectrum.PHSM:
            return "PhSm"
        case Spectrum.RF:
            return "ScRf"
        case Spectrum.IGRF:
            return "IgRf"
        case Spectrum.PHRF:
            return "PhRf"
        case _:
            raise NotImplementedError


def read(
    fp: Path,
    name: str,
    mode: Spectrum = Spectrum.AB,
    *,
    xaxis=XAxisType.Unknown,
    nan_cutoff: int = 5,
    **kw,
) -> Series | None:
    """The function reads the file using the brukeropusreader library and returns
    the read spectrum as a series, with the XAxisType."""
    modestr = _get_modestr(mode)

    try:
        opus = read_file(str(fp))
        N: npt.NDArray = opus.get_range(modestr)
        D: npt.NDArray = opus.get(modestr, np.zeros_like(N))
    except (KeyError, error):
        return None

    D[abs(D) > nan_cutoff] = np.nan

    s = Series(data=D, index=N, name=name)
    s = spectrum_conversion(s, XAxisType.Wavelength_nm, xaxis)
    return s


def meta(fp: Path, name: str, mode: Spectrum = Spectrum.AB, **kw) -> Series | None:
    modestr = _get_modestr(mode)
    meta = {}

    try:
        opus = read_file(str(fp))
        # need to try and read the file to detect if mode is present
        opus.get_range(modestr)
    except (KeyError, error):
        return None

    # Add all raw meta attributes to meta dict, without any array data
    raw_meta = {
        k: v for k, v in flatten_dict(opus).items() if not isinstance(v, np.ndarray)
    }
    # Remove this key, binary encoded string
    raw_meta.pop("Text Information")
    raw_meta.pop("History")

    meta.update(raw_meta)

    return Series(meta, name=name)


def numericextension(ext: str) -> bool:
    return ext.removeprefix(".").isnumeric()


opus_ftype = FileType("opus", None, read, meta, numericextension)
