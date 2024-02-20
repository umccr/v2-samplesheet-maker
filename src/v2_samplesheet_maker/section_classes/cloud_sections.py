#!/usr/bin/env python3

"""
Define each of the available section_classes
"""
from copy import deepcopy

import pandas as pd

# Relative modules
from ..utils import snake_case_to_upper_snake_case
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
                # Convert snake_case to upper snake case
                # Since we don't touch these again in the to_dict or to_json methods
                {
                    snake_case_to_upper_snake_case(kwarg_key): kwargs.pop(kwarg_key)
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

    def clean_rows(self):
        """
        Special section for case when Cloud_Data not defined but
        urn in BCLConvert_Settings is defined
        :return:
        """
        # Fillna based on sample_id
        mini_sample_dfs = []
        column_names_to_fill = ["LibraryPrepKitName", "IndexAdapterKitName"]
        for sample_id, sample_df in self.section_df.groupby("Sample_ID"):
            mini_sample_dfs.append(
                (
                    # Starting dataframe
                    sample_df
                    # Drop columns
                    .dropna(
                        how='all',
                        axis='columns'
                    )
                    .fillna("ffill")
                    .drop_duplicates(keep='first')
                )
            )

        cloud_data_list_columns_og = self.section_df.columns
        cloud_data_list_df = (
            # Append sample dfs together
            pd.concat(mini_sample_dfs).
            # Then reindex based on the original columns
            reindex(
                cloud_data_list_columns_og,
                axis='columns'
            )
        )

        # Reset df
        self.section_df = cloud_data_list_df
