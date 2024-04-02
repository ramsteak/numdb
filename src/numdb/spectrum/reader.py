from __future__ import annotations
from pathlib import Path
from pandas import Series, Index
from .enums import Spectrum, XAxisType
from ..exceptions import ReadError
from .filetypes import FileType, _registered_filetypes
from numpy import typing as npt
import numpy as np
from scipy.interpolate import interp1d


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

    # X axis conversions
    curr_xexp = curr_xaxis.value
    desr_xexp = xaxis.value

    X = s.index

    if curr_xexp != desr_xexp:
        # unit inversion
        if curr_xexp > 50 and curr_xexp < 50:
            X = 1 / X
            curr_xexp -= 100
        elif curr_xexp < 50 and curr_xexp > 50:
            X = 1 / X
            curr_xexp += 100

        # unit alignment
        if curr_xexp != desr_xexp:
            diff = -(desr_xexp - curr_xexp)
            X *= 10**diff

    # X axis interpolation
    if xinterp is not None:
        interp = interp1d(s.index.values, s.values, kind=interp_kind, fill_value="extrapolate")  # type: ignore
        s = Series(interp(xinterp), index=Index(xinterp), name=s.name)  # type: ignore

    # X, Y axis rounding
    if roundx is not None:
        s.index = np.round(s.index, roundx)  # type: ignore
    if roundy is not None:
        s = s.round(roundy)

    return s
