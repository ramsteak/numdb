# NumDB

[![Black formatting](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This project imports files, mainly spectral data, organized in a filesystem
structure with folders with leading numbers (or any unique identifier).
This helps with organizing files in a reasonable structure, and to import them without lengthy names or listing all files manually.

```txt
root
├── 01_TEST
│    ├── first.csv
│    └── second.csv
└── 02_PROOF
     ├── 01_TRIAL1
     │    └── trial1.csv
     └── 02_TRIAL2
          ├── trial2.csv
          └── trial3.csv
```

```py
from numdb import importfiles

# This will yield two pandas dataframes, one containing the spectra and one with
# metadata from all the files in the two TRIAL folders.
df,m = importfiles("02:01", "02:02", root=root)
```

## File loading

The module navigates through the file tree and automatically detects the filetype.

### Custom filetypes

The module contains some prepackaged file readers (such as opus files and innospectra files),
but custom filetypes can be specified and registered with `numdb.filetypes.register_filetype(FileType)`

```py
from numdb.filetypes import FileType, register_filetype

def read(fp: Path, name: str, mode: Spectrum, **kw) -> Series | None:...
def meta(fp: Path, name: str, mode: Spectrum, **kw) -> Series | None:...

myType = FileType(
    type_name = "myType",
    allowed_extensions = [".csv", ".tsv"],
    read_method = read,
    meta_method = meta,
)

register_filetype(myType)
```
