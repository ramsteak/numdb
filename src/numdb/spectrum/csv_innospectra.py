from pathlib import Path
from .enums import XAxisType, Spectrum
from pandas import Series, read_csv
import numpy as np
from io import StringIO
from .filetypes import register_filetype, FileType


def read(fp: Path, name: str, mode: Spectrum, **kw) -> tuple[Series, XAxisType] | None:
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

    return Series(data=A, index=N, name=name), XAxisType.Wavelength_nm


def meta(fp: Path, name: str):
    ...


ftype = FileType("inno_spectra", [".csv"], read, meta)
register_filetype(ftype)
