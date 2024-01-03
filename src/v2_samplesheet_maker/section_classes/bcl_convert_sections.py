#!/usr/bin/env python3

"""
Define each of the available section_classes
"""

# Relative modules
from ..classes.super_sections import (
    KVSection, DataFrameSection, DataFrameSectionRow
)

# Relative subpackages
from ..models.bcl_convert_sections import (
    BCLConvertDataRowModel,
    BCLConvertSettingsSectionModel,
    BCLConvertDataSectionModel
)


class BCLConvertSettingsSection(KVSection):
    """
    BCLConvert Settings Section
    https://support-docs.illumina.com/SW/dragen_v42/Content/SW/DRAGEN/SampleSheet.htm
    """

    # Set model
    _model = BCLConvertSettingsSectionModel

    # Set class name and header
    _class_header = "BCLConvert_Settings"


class BCLConvertDataRow(DataFrameSectionRow):
    """
    A BCLConvert DataRow
    """

    # Set model
    _model = BCLConvertDataRowModel


class BCLConvertDataSection(DataFrameSection):
    """
    For the BCLConvert Data
    """

    # Set model
    _model = BCLConvertDataSectionModel
    _row_obj = BCLConvertDataRow

    # Set class name and Header
    _class_header = "BCLConvert_Data"
