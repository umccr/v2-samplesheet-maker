#!/usr/bin/env python3

"""
PyDantic Schemas for each of the classes
"""
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

# Relative packages
from ..enums import AdapterBehaviour, FastqCompressionFormat


class HeaderSectionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    file_format_version: Optional[int]
    run_name: Optional[str]
    run_description: Optional[str]
    instrument_platform: Optional[str]
    instrument_type: Optional[str]


class ReadsSectionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    read_1_cycles: int
    read_2_cycles: Optional[int]
    index_1_cycles: Optional[int]
    index_2_cycles: Optional[int]


class BCLConvertSettingsSectionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    adapter_behavior: Optional[AdapterBehaviour]  # One of 'trim' / 'mask'
    adapter_read_1: Optional[str]
    adapter_read_2: Optional[str]
    adapter_stringency: Optional[float]  # Float between 0.5 and 1.0
    barcode_mismatches_index_1: Optional[int]  # 0, 1 or 2
    barcode_mismatches_index_2: Optional[int]  # 0, 1 or 2
    minimum_trimmed_read_length: Optional[int]
    minimum_adapter_overlap: Optional[int]  # 1, 2, or 3
    mask_short_reads: Optional[int]
    override_cycles: Optional[str]  # Y151;N8;N10;Y151
    trim_umi: Optional[bool]  # true or false (1, 0)
    create_fastq_for_index_reads: Optional[bool]  # true or false (1, 0)
    no_lane_splitting: Optional[bool]
    fastq_compression_format: Optional[FastqCompressionFormat]
    find_adapters_with_indels: Optional[bool]
    independent_index_collision_check: Optional[List]


class BCLConvertDataRowModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    sample_id: str
    lane: Optional[int]
    index: Optional[str]
    index2: Optional[str]
    sample_project: Optional[str]
    sample_name: Optional[str]
    # Per Sample Settings
    override_cycles: Optional[str]
    barcode_mismatches_index1: Optional[int]
    barcode_mismatches_index2: Optional[int]
    adapter_read_1: Optional[str]
    adapter_read_2: Optional[str]
    adapter_behavior: Optional[AdapterBehaviour]
    adapter_stringency: Optional[float]


class BCLConvertDataSectionModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    bclconvert_datarows: List[BCLConvertDataRowModel]
