from brukeropusreader import read_file
from pathlib import Path
from ..enums import XAxisType, Spectrum
from pandas import Series
import numpy as np
from numpy import typing as npt
from struct import error
from ..filetypes import FileType
from typing import Any
from ..conversions import spectrum_conversion


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
    fp: Path, name: str, mode: Spectrum = Spectrum.AB, *, xaxis= XAxisType.Unknown, nan_cutoff: int = 5, **kw
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
    meta: dict[str, Any] = {}

    try:
        opus = read_file(str(fp))
        # need to try and read the file to detect if mode is present
        opus.get_range(modestr)
    except (KeyError, error):
        return None

    return Series()


opus_ftype = FileType("opus", None, read, meta, lambda x: x.removeprefix(".").isnumeric())
