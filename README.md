# NumDB

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
          └── trial2.csv
```

```py
from numdb import importfiles

# This will yield a single pandas dataframe containing both of the spectra from the two folders
df = importfiles("02:01", "02:02", root=root)
```
