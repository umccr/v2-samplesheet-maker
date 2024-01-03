#!/usr/bin/env python3

"""
PyDantic Schemas for each of the classes
"""
# Imports
from typing import Optional, List, ClassVar, Dict
from pydantic import BaseModel, ConfigDict

from ..classes.super_sections import CloudKVSection, CloudDataFrameSection


class CloudSettingsSectionModel(BaseModel):
    # Standard options
    cloud_workflow: str
    generated_version: Optional[str]

    # Analysis urns
    analysis_urns: Optional[Dict]

    model_config = ConfigDict(from_attributes=True)

    def to_dict(self):
        initial_dict = {
            "GeneratedVersion": self.generated_version,
            "Cloud_Workflow": self.cloud_workflow,
            "BCLConvert_Pipeline": self.bclconvert_pipeline,
        }
        if self.analysis_urns is None:
            return initial_dict

        initial_dict.update(self.analysis_urns)

        return initial_dict


class CloudDataSectionRowModel(BaseModel):
    """
    https://support-docs.illumina.com/SW/DRAGEN_TSO500_v2.1_ICA/Content/LP/TSO500/AutolaunchSampleSheetSettings.htm
    """
    sample_id: Optional[str]
    project_name: Optional[str]
    library_name: Optional[str]
    library_prep_kit_name: Optional[str]
    index_adapter_kit_name: Optional[str]


class CloudDataSectionModel(BaseModel):
    # Set data rows
    data_rows: List[CloudDataSectionRowModel]

    # Set row order columns
    row_order_columns: ClassVar[List] = ["ProjectName", "Sample_ID", "LibraryName"]

    model_config = ConfigDict(from_attributes=True)
