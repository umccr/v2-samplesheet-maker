#!/usr/bin/env python

from typing import Optional
from pydantic import BaseModel

# Relative modules
from .sections import (
    HeaderSectionModel,
    ReadsSectionModel,
    BCLConvertSettingsSectionModel,
    BCLConvertDataSectionModel
)


class SampleSheetModel(BaseModel):
    header_section: HeaderSectionModel
    reads_section: ReadsSectionModel
    bclconvert_settings_section: Optional[BCLConvertSettingsSectionModel]
    bclconvert_data_section: Optional[BCLConvertDataSectionModel]
