from ..filetypes import register_filetype

_FTYPEREADER = "_FTYPEREADER"

from .csv_innospectra import innospectra_ftype

register_filetype(innospectra_ftype)

from .opus_bruker import opus_ftype

register_filetype(opus_ftype)
