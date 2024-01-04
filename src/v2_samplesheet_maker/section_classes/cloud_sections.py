#!/usr/bin/env python3

"""
Define each of the available section_classes
"""
from copy import deepcopy

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

    def __init__(self, *args, **kwargs):
        # Initialise set
        self.analysis_urns = {}
        for kwarg_key, kwarg_value in deepcopy(kwargs).items():
            # Check kwarg is a pipeline variable
            if not (
                    kwarg_key.lower().endswith("_pipeline") and
                    kwarg_value.lower().startswith("urn:")
            ):
                continue

            # Update set
            self.analysis_urns.update(
                # Pop urn from key at the same time
                {
                    kwarg_key: kwargs.pop(kwarg_key)
                }
            )

        super().__init__(*args, **kwargs)

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
