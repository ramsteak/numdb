from os.path import join
from pathlib import Path
from typing import Any

from pandas import DataFrame, Series, concat

from ..misc import get_first
from ..spectrum import read_spectrum
from ..spectrum.reader import ReadError
from .metadata import _registered_metaparsers

_load_defaults: dict[str, Any] = {}


def import_files(
    *npaths: str, root: Path | None = None, ignore_errors: bool|None = None, **kw
) -> tuple[DataFrame, DataFrame]:
    root = get_first("root", root, _load_defaults)

    # Get the list of all files to be collected.
    # Stored as list of (name, path)
    files: list[tuple[str, Path]] = []
    for ndbp, path in ((np, resolve_npath(np, root)) for np in npaths):
        files.extend((f"{ndbp}:{p.name}", p) for p in _get_files_path(path))

    spectra: list[Series] = []
    metadata: list[Series] = []
    for name, path in files:
        try:
            s, m = read_spectrum(path, name, **kw)
            spectra.append(s)
            metadata.append(m)
        except ReadError:
            if not get_first(
                "ignore_errors", ignore_errors, _load_defaults, default=False
            ):
                raise

    df_spectra = DataFrame(spectra)
    df_metadata = DataFrame(metadata)

    addmeta = [parser(df_metadata) for parser in _registered_metaparsers]
    df_metadata = concat((df_metadata, *addmeta), axis=1)
    return df_spectra, df_metadata


def resolve_npath(npath: str, root: Path | None) -> Path:
    pwd = get_first("root", root, _load_defaults)

    for dir in npath.split(":"):
        if (pwd / dir).is_file():
            return pwd / dir
        for d in (_d for _d in pwd.iterdir() if _d.is_dir()):
            if d.name.startswith(dir):
                break
        else:
            raise ValueError(f"Nonexistent folder {join(pwd, dir)}")
        pwd = d
    return pwd


def _get_files_path(path: Path) -> list[Path]:
    if path.is_dir():
        return [f for f in path.iterdir() if f.is_file()]
    return [path]


# def set_default(key: str, value: Any) -> None:
#     _load_defaults[key] = value


def set_loader_defaults(**kwargs) -> None:
    _load_defaults.update(kwargs)


def set_root(path: Path | str) -> None:
    if not isinstance(path, Path):
        path = Path(path)

    _load_defaults["root"] = path
