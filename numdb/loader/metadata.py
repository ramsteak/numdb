from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from pandas import DataFrame

_registered_metaparsers: list[MetaParser] = []


class MetaParser(ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def __call__(self, meta: DataFrame) -> DataFrame:
        ...


def register_metaparser(metaparser: MetaParser | type[MetaParser]) -> None:
    if isinstance(metaparser, type):
        return register_metaparser(metaparser())

    if not isinstance(metaparser, MetaParser):
        raise TypeError(f"Invalid metaparser of type {type(metaparser)}")
    _registered_metaparsers.append(metaparser)


class UnderscoreSplitter(MetaParser):
    def __call__(self, meta: DataFrame) -> DataFrame:
        ameta = meta["FILENAME_NOEXT"].str.split("_").to_list()
        dfmeta = DataFrame(ameta, index=meta.index)
        dfmeta.columns = dfmeta.columns.map(lambda x: f"_{x}")
        return dfmeta


class FileReader(MetaParser):
    def __init__(self, *fs: str | Path) -> None:
        self.fs = fs
        super().__init__()

    def __call__(self, meta: DataFrame) -> DataFrame:
        raise NotImplementedError
