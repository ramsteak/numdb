from __future__ import annotations
from pandas import Series, Index
from .enums import XAxisType
from numpy import typing as npt
import numpy as np
from scipy.interpolate import interp1d



def spectrum_conversion(
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


def round_spectrum(
    sp: Series, roundx: int | None, roundy: int | None, copy: bool = False
) -> Series:
    s = sp.copy() if copy else sp

    if roundx is not None:
        s.index = np.round(s.index, roundx)  # type: ignore
    if roundy is not None:
        s = s.round(roundy)

    return s


def interpolate_spectrum(sp: Series, xvalues: npt.ArrayLike, interp_kind: str) -> Series:
    interp = interp1d(sp.index.values, sp.values, kind=interp_kind, fill_value="extrapolate")  # type: ignore
    s = Series(interp(xvalues), index=Index(xvalues), name=sp.name)  # type: ignore
    return s
