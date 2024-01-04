#!/usr/bin/env python3

"""
Define each of the available section_classes
"""

# Relative modules
from ..classes.super_sections import KVSection, DataFrameSection, DataFrameSectionRow
from ..models.cloud_section import (
    CloudSettingsSectionModel,
    CloudDataSectionModel, CloudDataSectionRowModel
)


class CloudSettingsSection(KVSection):
    """
    The CloudSettings Section
    https://help.ica.illumina.com/sequencer-integration/analysis_autolaunch#secondary-analysis-settings
    """
    _model = CloudSettingsSectionModel
    _class_header = "Cloud_Settings"


class CloudDataSectionRow(DataFrameSectionRow):
    """
    A BCLConvert DataRow
    """

    # Set model
    _model = CloudDataSectionRowModel


class CloudDataSection(DataFrameSection):
    """
    The CloudData Section
    https://help.ica.illumina.com/sequencer-integration/analysis_autolaunch#secondary-analysis-settings
    """
    # Set model
    _model = CloudDataSectionModel
    _row_obj = CloudDataSectionRow
    _class_header = "Cloud_Data"
