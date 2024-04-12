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
            if ftype.accept_extension_rule(ext):
                read_result = ftype.read_method(fp, name, mode, **kw)
                meta_result = ftype.meta_method(fp, name, mode, **kw)
                if read_result is None or meta_result is None:
                    continue

                spectrum, metadata = read_result, meta_result
                break
        else:
            raise ReadError("Unable to detect filetype")

    elif isinstance(filetype, (FileType, str)):
        filetype = get_filetype(filetype)

        if filetype.accept_extension_rule(ext):
            read_result = filetype.read_method(fp, name, mode, **kw)
            meta_result = filetype.meta_method(fp, name, mode, **kw)
            if read_result is None or meta_result is None:
                raise ReadError("File was unrecognized")

            spectrum, metadata = read_result, meta_result

    else:
        raise ReadError("Invalid filetype specification")

    return spectrum, metadata


def read_spectrum(
    fp: Path,
    name: str,
    mode: Spectrum = Spectrum.AB,
    *,
    filetype: FileType | str = "auto",
    **kw,
) -> tuple[Series, Series]:
    s, m = _read_auto(fp, name, mode, filetype, **kw)

    _set = merge_dict(kw, _read_defaults)

    s = round_spectrum(s, _set.get("roundx"), _set.get("roundy"))

    if "xvalues" in _set:
        s = interpolate_spectrum(
            s,
            _set.get("xvalues"),  # type: ignore
            _set.get("interp_kind"),  # type: ignore
        )

    return s, m
