#!/usr/bin/env python3

"""
PyDantic Schemas for each of the classes
"""
from typing import Optional, List, ClassVar
from pydantic import BaseModel, ConfigDict

from ..enums import TSO500LSampleType


class TSO500LSettingsSectionModel(BaseModel):
    software_version: Optional[str]
    starts_from_fastq: bool
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


class TSO500LDataSectionModel(BaseModel):
    # Set data rows
    data_rows: List[TSO500LDataRowModel]

    # Set row order columns
    row_order_columns: ClassVar[List] = ["Sample_Type", "Sample_ID", "Index_ID"]

    model_config = ConfigDict(from_attributes=True)
