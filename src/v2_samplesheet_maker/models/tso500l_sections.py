#!/usr/bin/env python3

"""
PyDantic Schemas for each of the classes
"""
from typing import Optional, List, ClassVar
from pydantic import BaseModel, ConfigDict

from ..enums import TSO500LSampleType


class TSO500LSettingsSectionModel(BaseModel):
    # Settings
    starts_from_fastq: bool

    # Cloud values
    software_version: Optional[str]
    urn: Optional[str]

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        return {
            "SoftwareVersion": self.software_version,
            "StartsFromFastq": self.starts_from_fastq
        }


class TSO500LDataRowModel(BaseModel):
    sample_id: str
    index_id: str
    sample_type: TSO500LSampleType
    sample_description: Optional[str]
    index: Optional[str]
    index2: Optional[str]

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
            "Sample_Description": self.sample_description,
            "Index": self.index,
            "Index2": self.index2
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


class TSO500LDataSectionModel(BaseModel):
    # Set data rows
    data_rows: List[TSO500LDataRowModel]

    # Set row order columns
    row_order_columns: ClassVar[List] = ["Sample_Type", "Sample_ID", "Index_ID"]

    model_config = ConfigDict(from_attributes=True)
