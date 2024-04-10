from __future__ import annotations
from pathlib import Path
from pandas import Series, Index
from .enums import Spectrum, XAxisType
from ..exceptions import ReadError
from .filetypes import FileType, _registered_filetypes
from numpy import typing as npt
import numpy as np
from scipy.interpolate import interp1d


def _spectrum_conversion(
    sp: Series, xaxis0: XAxisType, xaxis1: XAxisType, copy: bool = False
) -> Series:
    s = sp.copy() if copy else sp

    if (xaxis1 == XAxisType.Unknown) or (xaxis0 == XAxisType.Unknown):
        return s

    X = s.index
    xa0, xa1 = xaxis0.value, xaxis1.value

    if xa0 != xa1:
        # inversion
        if (xa0 > 50) and (xa1 < 50):
            X = 1 / X
            xa0 -= 100
        elif (xa0 < 50) and (xa1 > 50):
            X = 1 / X
            xa0 += 100

    if xa0 != xa1:
        # alignment
        diff = -(xa1 - xa0)
        X *= 10**diff

    s.index = X
    return s


def _round_spectrum(
    sp: Series, roundx: int | None, roundy: int | None, copy: bool = False
) -> Series:
    s = sp.copy() if copy else sp

    if roundx is not None:
        s.index = np.round(s.index, roundx)  # type: ignore
    if roundy is not None:
        s = s.round(roundy)

    return s


def _interpolate_spectrum(
    sp: Series, xvalues: npt.ArrayLike, kind: str = "linear"
) -> Series:
    interp = interp1d(sp.index.values, sp.values, kind=kind, fill_value="extrapolate")  # type: ignore
    s = Series(interp(xvalues), index=Index(xvalues), name=sp.name)  # type: ignore
    return s


def _read_auto(
    fp: Path, name: str, mode=Spectrum.AB, filetype: None | str | FileType = None, **kw
) -> tuple[Series, XAxisType]:
    ext = fp.suffix.lower()

    if filetype is None or filetype == "auto":
        for _, ftype in _registered_filetypes.items():
            if ftype.accept_extension_rule(ext):
                read_result = ftype.read_method(fp, name, mode, **kw)
                if read_result is None:
                    continue

                spectrum, xaxistype = read_result
                break
        else:
            raise ReadError("Unable to detect filetype")

    elif isinstance(filetype, (FileType, str)):
        if isinstance(filetype, str):
            filetype = _registered_filetypes[filetype]

        if filetype.accept_extension_rule(ext):
            read_result = filetype.read_method(fp, name, mode, **kw)
            if read_result is None:
                raise ReadError("File was unrecognized")

            spectrum, xaxistype = read_result

    else:
        raise ReadError("Invalid filetype specification")

    return spectrum, xaxistype


def read_spectrum(
    fp: Path,
    name: str,
    mode: Spectrum = Spectrum.AB,
    xaxis: XAxisType = XAxisType.Unknown,
    roundx: int | None = 5,
    roundy: int | None = 5,
    filetype: FileType | str = "auto",
    xinterp: npt.ArrayLike | None = None,
    interp_kind: str = "linear",
    **kw,
) -> Series:
    s, curr_xaxis = _read_auto(fp, name, mode, filetype, **kw)

    # x axis conversion
    s = _spectrum_conversion(s, curr_xaxis, xaxis)

    # spectrum interpolation
    if xinterp is not None:
        s = _interpolate_spectrum(s, xinterp, interp_kind)

    # x axis rounding
    s = _round_spectrum(s, roundx, roundy)

    return s
