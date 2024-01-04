#!/usr/bin/env python3

"""
PyDantic Schemas for each of the classes
"""
from typing import Optional, List
from pydantic import BaseModel, ConfigDict


class HeaderSectionModel(BaseModel):

    file_format_version: Optional[int]
    run_name: Optional[str]
    run_description: Optional[str]
    instrument_platform: Optional[str]
    instrument_type: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            "FileFormatVersion": self.file_format_version,
            "RunName": self.run_name,
            "RunDescription": self.run_description,
            "InstrumentPlatform": self.instrument_platform,
            "InstrumentType": self.instrument_type
        }


class ReadsSectionModel(BaseModel):
    read_1_cycles: int
    read_2_cycles: Optional[int]
    index_1_cycles: Optional[int]
    index_2_cycles: Optional[int]

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            "Read1Cycles": self.read_1_cycles,
            "Read2Cycles": self.read_2_cycles,
            "Index1Cycles": self.index_1_cycles,
            "Index2Cycles": self.index_2_cycles
        }


class SequencingSectionModel(BaseModel):
    custom_index_1_primer: Optional[bool]
    custom_index_2_primer: Optional[bool]
    custom_read_1_primer: Optional[bool]
    custom_read_2_primer: Optional[bool]
    library_prep_kits: Optional[List]

    def to_dict(self):
        return {
            "CustomIndex1Primer": self.custom_index_1_primer,
            "CustomIndex2Primer": self.custom_index_2_primer,
            "CustomRead1Primer": self.custom_read_1_primer,
            "CustomRead2Primer": self.custom_read_2_primer,
            "LibraryPrepKits": ";".join(self.library_prep_kits) if self.library_prep_kits is not None else None
        }