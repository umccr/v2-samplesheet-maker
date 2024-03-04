from enum import Enum


class AdapterBehaviour(Enum):
    TRIM = "trim"
    MASK = "mask"


class FastqCompressionFormat(Enum):
    GZIP = "gzip"
    DRAGEN = "dragen"
    DRAGEN_INTERLEAVED = "dragen-interleaved"


class TSO500LSampleType(Enum):
    DNA = "DNA"


class TSO500SSampleType(Enum):
    DNA = "DNA"
    RNA = "RNA"


class TSO500SSampleFeature(Enum):
    HRD = "HRD"