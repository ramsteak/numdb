from brukeropusreader import read_file
from pathlib import Path
from .enums import XAxisType, Spectrum
from pandas import Series
import numpy as np
from numpy import typing as npt
from struct import error
from .filetypes import register_filetype, FileType


def read(
    fp: Path, name: str, mode: Spectrum = Spectrum.AB, *, nan_cutoff: int = 5, **kw
) -> tuple[Series, XAxisType] | None:
    match mode:
        case Spectrum.AB:
            modestr = "AB"
        case Spectrum.TR:
            modestr = "TR"
        case Spectrum.SM:
            modestr = "ScSm"
        case Spectrum.IGSM:
            modestr = "IgSm"
        case Spectrum.PHSM:
            modestr = "PhSm"
        case Spectrum.RF:
            modestr = "ScRf"
        case Spectrum.IGRF:
            modestr = "IgRf"
        case Spectrum.PHRF:
            modestr = "PhRf"
        case _:
            raise NotImplementedError

    try:
        opus = read_file(str(fp))
        N: npt.NDArray = opus.get_range(modestr)
        D: npt.NDArray = opus.get(modestr, np.zeros_like(N))
    except (KeyError, error):
        return None

    D[abs(D) > nan_cutoff] = np.nan
    return Series(D, index=N, name=name), XAxisType.Wavenumber_cm

def meta(fp: Path, name: str, **kw):
    ...

ftype = FileType("opus", None, read, meta, lambda x: x.removeprefix(".").isnumeric())
register_filetype(ftype)
