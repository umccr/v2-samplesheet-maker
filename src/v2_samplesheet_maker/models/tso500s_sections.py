#!/usr/bin/env python3

"""
PyDantic Schemas for each of the classes
"""
from typing import Optional, List, ClassVar
from pydantic import BaseModel, ConfigDict

from ..enums import TSO500SSampleType, AdapterBehaviour, TSO500SSampleFeature


class TSO500SSettingsSectionModel(BaseModel):
    # BCLConvert Settings for within TSO500S
    adapter_read_1: Optional[str]
    adapter_read_2: Optional[str]
    adapter_behaviour: Optional[AdapterBehaviour]
    minimum_trimmed_read_length: Optional[int]
    mask_short_reads: Optional[int]
    override_cycles: Optional[str]

    # Settings
    starts_from_fastq: Optional[bool]

    # Cloud values
    software_version: Optional[str]
    urn: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            "AdapterRead1": self.adapter_read_1,
            "AdapterRead2": self.adapter_read_2,
            "AdapterBehaviour": self.adapter_behaviour.value if self.adapter_behaviour is not None else None,
            "MinimumTrimmedReadLength": self.minimum_trimmed_read_length,
            "MaskShortReads": self.mask_short_reads,
            "OverrideCycles": self.override_cycles,
            "SoftwareVersion": self.software_version,
            "StartsFromFastq": self.starts_from_fastq
        }

    def to_json(self):
        return {
            "adapter_read_1": self.adapter_read_1,
            "adapter_read_2": self.adapter_read_2,
            "adapter_behaviour": self.adapter_behaviour.value if self.adapter_behaviour is not None else None,
            "minimum_trimmed_read_length": self.minimum_trimmed_read_length,
            "mask_short_reads": self.mask_short_reads,
            "override_cycles": self.override_cycles,
            "software_version": self.software_version,
            "starts_from_fastq": self.starts_from_fastq
        }


class TSO500SDataRowModel(BaseModel):
    # From https://support-docs.illumina.com/SW/DRAGEN_TSO500_v2.5_ICA/Content/LP/TSO500/AutolaunchSampleSheetSettings.htm
    sample_id: str
    index_id: Optional[str]  # Use when using [Cloud_TSO500L_Data]
    sample_type: TSO500SSampleType
    sample_feature: Optional[TSO500SSampleFeature]
    sample_description: Optional[str]
    lane: Optional[int]
    index: str
    index2: str
    pair_id: str

    # Cloud Data
    # If URN is specified in TSO500L_Settings
    # and no Cloud_Data section is specified we add in the Cloud_Data section for each sample
    # Sample_ID is obvs just sample_id
    # LibraryName is <Sample_ID>_<index>_<index2>
    library_prep_kit_name: Optional[str]
    index_adapter_kit_name: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            "Sample_ID": self.sample_id,
            "Index_ID": self.index_id,
            "Sample_Type": self.sample_type.value if self.sample_type is not None else None,
            "Sample_Feature": self.sample_feature,
            "Sample_Description": self.sample_description,
            "Lane": self.lane,
            "Index": self.index,
            "Index2": self.index2,
            "Pair_ID": self.pair_id
        }

    def to_json(self):
        return {
            "sample_id": self.sample_id,
            "index_id": self.index_id,
            "sample_type": self.sample_type.value if self.sample_type is not None else None,
            "sample_feature": self.sample_feature,
            "sample_description": self.sample_description,
            "lane": self.lane,
            "index": self.index,
            "index2": self.index2,
            "pair_id": self.pair_id
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


class TSO500SDataSectionModel(BaseModel):
    # Set data rows
    data_rows: List[TSO500SDataRowModel]

    # Set row order columns
    row_order_columns: ClassVar[List] = ["Sample_Type", "Pair_ID", "Sample_ID", "Index_ID"]

    model_config = ConfigDict(from_attributes=True)
