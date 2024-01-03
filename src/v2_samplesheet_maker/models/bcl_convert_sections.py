#!/usr/bin/env python3

"""
PyDantic Schemas for each of the classes
"""
from typing import Optional, List, ClassVar
from pydantic import BaseModel, ConfigDict

# Relative packages
from ..enums import AdapterBehaviour, FastqCompressionFormat


class BCLConvertSettingsSectionModel(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            "AdapterBehavior": self.adapter_behavior.value if self.adapter_behavior is not None else None,
            "AdapterRead1": self.adapter_read_1,
            "AdapterRead2": self.adapter_read_2,
            "AdapterStringency": self.adapter_stringency,
            "BarcodeMismatchesIndex1": self.barcode_mismatches_index_1,
            "BarcodeMismatchesIndex2": self.barcode_mismatches_index_2,
            "MinimumTrimmedReadLength": self.minimum_trimmed_read_length,
            "MinimumAdapterOverlap": self.minimum_adapter_overlap,
            "MaskShortReads": self.mask_short_reads,
            "OverrideCycles": self.override_cycles,
            "TrimUMI": self.trim_umi,
            "CreateFastqForIndexReads": self.create_fastq_for_index_reads,
            "NoLaneSplitting": self.no_lane_splitting,
            "FastqCompressionFormat": self.fastq_compression_format.value if self.fastq_compression_format is not None else None,
            "FindAdaptersWithIndels": self.find_adapters_with_indels,
            "IndependentIndexCollisionCheck": self.independent_index_collision_check
        }


class BCLConvertDataRowModel(BaseModel):
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

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            # Sample Options
            "Lane": self.lane,
            "Sample_ID": self.sample_id,
            "index": self.index,
            "index2": self.index2,
            "Sample_Project": self.sample_project,
            "Sample_Name": self.sample_name,
            # Per sample settings
            "OverrideCycles": self.override_cycles,
            "BarcodeMismatchesIndex1": self.barcode_mismatches_index1,
            "BarcodeMismatchesIndex2": self.barcode_mismatches_index2,
            "AdapterRead1": self.adapter_read_1,
            "AdapterRead2": self.adapter_read_2,
            "AdapterBehavior": self.adapter_behavior.value if self.adapter_behavior is not None else None,
            "AdapterStringency": self.adapter_stringency
        }


class BCLConvertDataSectionModel(BaseModel):
    # Set data rows
    data_rows: List[BCLConvertDataRowModel]

    # Set row order columns
    row_order_columns: ClassVar[List] = ["Lane", "Sample_ID"]

    model_config = ConfigDict(from_attributes=True)
