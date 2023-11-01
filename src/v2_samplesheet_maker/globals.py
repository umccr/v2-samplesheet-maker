#!/usr/bin/env python

from .enums import SectionFormat

SECTION_FORMAT_BY_SECTION_NAME = {
    "Header": SectionFormat.KV_PAIRS,
    "Reads": SectionFormat.KV_PAIRS,
    "BCLConvert_Settings": SectionFormat.KV_PAIRS,
    "BCLConvert_Data": SectionFormat.DATAFRAME
}


