from ..filetypes import register_filetype
from .csv_innospectra import innospectra_ftype
from .opus_bruker import opus_ftype

_FTYPEREADER = "_FTYPEREADER"

register_filetype(innospectra_ftype)
register_filetype(opus_ftype)

__all__ = ["_FTYPEREADER"]
