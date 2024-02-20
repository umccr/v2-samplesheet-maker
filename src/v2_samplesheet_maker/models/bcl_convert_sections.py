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

    # Software version required when running through auto-launch
    # Urn also required when running through auto-launch on BaseSpace
    software_version: Optional[str]
    urn: Optional[str]

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
            "IndependentIndexCollisionCheck": ";".join(self.independent_index_collision_check) if self.independent_index_collision_check is not None else None,
            "SoftwareVersion": self.software_version
        }

    def to_json(self):
        return {
            "adapter_behavior": self.adapter_behavior.value if self.adapter_behavior is not None else None,
            "adapter_read_1": self.adapter_read_1,
            "adapter_read_2": self.adapter_read_2,
            "adapter_stringency": self.adapter_stringency,
            "barcode_mismatches_index_1": self.barcode_mismatches_index_1,
            "barcode_mismatches_index_2": self.barcode_mismatches_index_2,
            "minimum_trimmed_read_length": self.minimum_trimmed_read_length,
            "minimum_adapter_overlap": self.minimum_adapter_overlap,
            "mask_short_reads": self.mask_short_reads,
            "override_cycles": self.override_cycles,
            "trim_umi": self.trim_umi,
            "create_fastq_for_index_reads": self.create_fastq_for_index_reads,
            "no_lane_splitting": self.no_lane_splitting,
            "fastq_compression_format": self.fastq_compression_format.value if self.fastq_compression_format is not None else None,
            "find_adapters_with_indels": self.find_adapters_with_indels,
            "independent_index_collision_check": self.independent_index_collision_check,
            "software_version": self.software_version
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
    barcode_mismatches_index_1: Optional[int]
    barcode_mismatches_index_2: Optional[int]
    adapter_read_1: Optional[str]
    adapter_read_2: Optional[str]
    adapter_behavior: Optional[AdapterBehaviour]
    adapter_stringency: Optional[float]

    # Cloud Data
    # If URN is specified in BCLConvert_Settings
    # and no Cloud_Data section is specified we add in the Cloud_Data section for each sample
    # Sample_ID is obvs just sample_id
    # LibraryName is <Sample_ID>_<index>_<index2>
    library_prep_kit_name: Optional[str]
    index_adapter_kit_name: Optional[str]

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
            "BarcodeMismatchesIndex1": self.barcode_mismatches_index_1,
            "BarcodeMismatchesIndex2": self.barcode_mismatches_index_2,
            "AdapterRead1": self.adapter_read_1,
            "AdapterRead2": self.adapter_read_2,
            "AdapterBehavior": self.adapter_behavior.value if self.adapter_behavior is not None else None,
            "AdapterStringency": self.adapter_stringency
        }

    def to_json(self):
        return {
            # Sample Options
            "lane": self.lane,
            "sample_id": self.sample_id,
            "index": self.index,
            "index2": self.index2,
            "sample_project": self.sample_project,
            "sample_name": self.sample_name,
            # Per sample settings
            "override_cycles": self.override_cycles,
            "barcode_mismatches_index_1": self.barcode_mismatches_index_1,
            "barcode_mismatches_index_2": self.barcode_mismatches_index_2,
            "adapter_read_1": self.adapter_read_1,
            "adapter_read_2": self.adapter_read_2
        }

    def get_cloud_data_section_row(self):
        """
        Special case for populating cloud data section when BCLConvert URN is specified
        but not cloud data section is specified
        :return:
        """
        # library name is combination of sample_id, index and index2
        library_name = "_".join(
            map(
                str,
                filter(
                    lambda filter_iter: filter_iter is not None,
                    [
                        getattr(self, "sample_id", None),
                        getattr(self, "index", None),
                        getattr(self, "index2", None)
                    ]
                )
            )
        )

        return {
            "sample_id": self.sample_id,
            "library_name": library_name,
            "library_prep_kit_name": self.library_prep_kit_name,
            "index_adapter_kit_name": self.index_adapter_kit_name
        }


class BCLConvertDataSectionModel(BaseModel):
    # Set data rows
    data_rows: List[BCLConvertDataRowModel]

    # Set row order columns
    row_order_columns: ClassVar[List] = ["Lane", "Sample_ID"]
    model_config = ConfigDict(from_attributes=True)
