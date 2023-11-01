from enum import Enum


class SectionFormat(Enum):
    KV_PAIRS = "key_value_pairs"
    DATAFRAME = "dataframe"


class AdapterBehaviour(Enum):
    TRIM = "trim"
    MASK = "mask"


class FastqCompressionFormat(Enum):
    GZIP = "gzip"
    DRAGEN = "dragen"
    DRAGEN_INTERLEAVED = "dragen-interleaved"