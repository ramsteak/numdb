from io import StringIO
from pathlib import Path

import numpy as np
from pandas import Series, read_csv

from ..conversions import spectrum_conversion
from ..enums import Spectrum, XAxisType
from ..filetypes import FileType


def read(
    fp: Path, name: str, mode: Spectrum, xaxis: XAxisType = XAxisType.Unknown, **kw
) -> Series | None:
    match mode:
        case Spectrum.AB:
            modestr = "Absorbance (AU)"
        case Spectrum.SM:
            modestr = "Sample Signal (unitless)"
        case Spectrum.RF:
            modestr = "Reference Signal (unitless)"
        case _:
            raise NotImplementedError
    try:
        with open(fp, "rt", encoding="utf-8-sig") as fl:
            fc = fl.read()
    except (FileNotFoundError, UnicodeDecodeError):
        return None

    if not fc.startswith("***Scan Config Information***,,,,,,,"):
        return None
    if "Wavelength (nm)" not in fc:
        return None
    if "***Scan Data***,,,,,,,,,,,,,,," not in fc:
        return None

    csv = fc.partition("***Scan Data***,,,,,,,,,,,,,,,")[-1]
    df = read_csv(
        StringIO(csv),
        na_filter=True,
        na_values="∞",
        keep_default_na=True,
        dtype=np.float64,
    )
    pass
    N = np.array(df["Wavelength (nm)"])
    A = np.array(df[modestr])

    s = Series(data=A, index=N, name=name)
    s = spectrum_conversion(s, XAxisType.Wavelength_nm, xaxis)
    return s


def meta(
    fp: Path, name: str, mode: Spectrum, xaxis=XAxisType.Unknown, **kw
) -> Series | None:
    ...


innospectra_ftype = FileType("innospectra", [".csv"], read, meta)
