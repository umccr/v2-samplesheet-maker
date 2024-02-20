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
    index_orientation: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            "FileFormatVersion": self.file_format_version,
            "RunName": self.run_name,
            "RunDescription": self.run_description,
            "InstrumentPlatform": self.instrument_platform,
            "InstrumentType": self.instrument_type,
            "IndexOrientation": self.index_orientation
        }

    def to_json(self):
        return {
            "file_format_version": self.file_format_version,
            "run_name": self.run_name,
            "run_description": self.run_description,
            "instrument_platform": self.instrument_platform,
            "instrument_type": self.instrument_type,
            "index_orientation": self.index_orientation
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

    def to_json(self):
        return {
            "read_1_cycles": self.read_1_cycles,
            "read_2_cycles": self.read_2_cycles,
            "index_1_cycles": self.index_1_cycles,
            "index_2_cycles": self.index_2_cycles
        }


class SequencingSectionModel(BaseModel):
    custom_index_1_primer: Optional[bool]
    custom_index_2_primer: Optional[bool]
    custom_read_1_primer: Optional[bool]
    custom_read_2_primer: Optional[bool]
    library_prep_kits: Optional[List[str]]

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            "CustomIndex1Primer": self.custom_index_1_primer,
            "CustomIndex2Primer": self.custom_index_2_primer,
            "CustomRead1Primer": self.custom_read_1_primer,
            "CustomRead2Primer": self.custom_read_2_primer,
            "LibraryPrepKits": ";".join(self.library_prep_kits) if self.library_prep_kits is not None else None
        }

    def to_json(self):
        return {
            "custom_index_1_primer": self.custom_index_1_primer,
            "custom_index_2_primer": self.custom_index_2_primer,
            "custom_read_1_primer": self.custom_read_1_primer,
            "custom_read_2_primer": self.custom_read_2_primer,
            "library_prep_kits": self.library_prep_kits
        }