#!/usr/bin/env python

from typing import Optional
from pydantic import BaseModel

# Relative imports
from .run_info_sections import HeaderSectionModel, ReadsSectionModel
from .bcl_convert_sections import BCLConvertSettingsSectionModel, BCLConvertDataSectionModel


class SampleSheetModel(BaseModel):
    header_section: HeaderSectionModel
    reads_section: ReadsSectionModel
    bclconvert_settings_section: Optional[BCLConvertSettingsSectionModel]
    bclconvert_data_section: Optional[BCLConvertDataSectionModel]
