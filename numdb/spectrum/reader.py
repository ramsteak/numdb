from __future__ import annotations

from pathlib import Path
from typing import Any

from pandas import Series

from ..exceptions import ReadError
from ..misc import merge_dict
from .conversions import interpolate_spectrum, round_spectrum
from .enums import Spectrum, XAxisType
from .filetypes import FileType, get_filetype, get_filetypes

_read_defaults: dict[str, Any] = {
    "xaxis": XAxisType.Unknown,
    "roundx": None,
    "roundy": None,
    "interp_kind": "linear",
}


def _read_auto(
    fp: Path,
    name: str,
    mode: Spectrum,
    filetype: None | str | FileType = None,
    **kw,
) -> tuple[Series, Series]:
    ext = fp.suffix.lower()

    if filetype is None or filetype == "auto":
        for ftype in get_filetypes():
            if ftype.check_ext(ext):
                spectrum = ftype.read_method(fp, name, mode, **kw)
                metadata = ftype.meta_method(fp, name, mode, **kw)
                if spectrum is None or metadata is None:
                    continue
                break
        else:
            raise ReadError(f"Unable to detect filetype for {name}")

    elif isinstance(filetype, (FileType, str)):
        ftype = get_filetype(filetype)

        if ftype.check_ext(ext):
            spectrum = ftype.read_method(fp, name, mode, **kw)
            metadata = ftype.meta_method(fp, name, mode, **kw)
            if spectrum is None or metadata is None:
                raise ReadError("File was unrecognized")
    else:
        raise ReadError("Invalid filetype specification")

    metadata.index = metadata.index.map(lambda x: ftype.name + "." + x)
    metadata["FILETYPE"] = ftype.name

    return spectrum, metadata


def read_spectrum(
    fp: Path,
    name: str,
    mode: Spectrum = Spectrum.AB,
    *,
    filetype: FileType | str = "auto",
    **kw,
) -> tuple[Series, Series]:
    # Merge passed kw and _read_defaults
    _kw = merge_dict(kw, _read_defaults)
    spectrum, metadata = _read_auto(fp, name, mode, filetype, **_kw)

    # Spectrum interpolation
    if "xvalues" in _kw:
        spectrum = interpolate_spectrum(
            spectrum,
            _kw.get("xvalues"),  # type: ignore
            _kw.get("interp_kind"),  # type: ignore
        )

    # Spectrum rounding
    spectrum = round_spectrum(spectrum, _kw.get("roundx"), _kw.get("roundy"))

    # Add metadata
    metadata["FILEPATH"] = str(fp)
    metadata["FILENAME"] = fp.name
    metadata["MODE"] = mode.name
    return spectrum, metadata
