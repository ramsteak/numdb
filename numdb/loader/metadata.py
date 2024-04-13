from __future__ import annotations

from typing import Callable, TypeAlias

from pandas import DataFrame

_registered_metaparsers: list[MetaParser] = []

MetaParser: TypeAlias = Callable[[DataFrame], DataFrame]


def register_metaparser(func: MetaParser) -> None:
    _registered_metaparsers.append(func)


class MetaParsers:
    @staticmethod
    def underscore_splitter(meta: DataFrame) -> DataFrame:
        und = DataFrame(
            meta["FILENAME_NOEXT"].str.split("_").to_list(), index=meta.index
        )
        und.columns = und.columns.map(lambda x: f"_{x}")
        return und
