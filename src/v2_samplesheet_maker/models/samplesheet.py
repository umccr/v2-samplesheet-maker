#!/usr/bin/env python

from typing import Optional
from pydantic import BaseModel

# Relative imports
from .run_info_sections import (
    HeaderSectionModel, ReadsSectionModel, SequencingSectionModel
)
from .bcl_convert_sections import (
    BCLConvertSettingsSectionModel, BCLConvertDataSectionModel
)
from .cloud_section import (
    CloudSettingsSectionModel, CloudDataSectionModel
)


class SampleSheetModel(BaseModel):
    # Run Info Sections
    header_section: HeaderSectionModel
    reads_section: ReadsSectionModel
    sequencing_section: Optional[SequencingSectionModel]

    # BCLConvert Sections
    bclconvert_settings_section: Optional[BCLConvertSettingsSectionModel]
    bclconvert_data_section: Optional[BCLConvertDataSectionModel]

    # Cloud Sections
    cloud_settings_section: Optional[CloudSettingsSectionModel]
    cloud_data_section: Optional[CloudDataSectionModel]
