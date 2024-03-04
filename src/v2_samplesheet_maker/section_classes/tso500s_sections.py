#!/usr/bin/env python3

"""
Define each of the available section_classes
"""

# Relative modules
from ..classes.super_sections import (
    KVSection, DataFrameSection, DataFrameSectionRow
)

# Relative subpackages
from ..models.tso500s_sections import (
    TSO500SSettingsSectionModel,
    TSO500SDataRowModel,
    TSO500SDataSectionModel,
)


class TSO500SSettingsSection(KVSection):
    """
    TSO500S Settings Section
    https://support-docs.illumina.com/SW/DRAGEN_TSO500_v2.5_ICA/Content/LP/TSO500/AutolaunchSampleSheetSettings.htm
    """

    # Set model
    _model = TSO500SSettingsSectionModel

    # Set class name and header
    _class_header = "TSO500S_Settings"


class CloudTSO500SSettingsSection(TSO500SSettingsSection):
    _is_cloud = True


class TSO500SDataRowSection(DataFrameSectionRow):
    """
    A BCLConvert DataRow
    """

    # Set model
    _model = TSO500SDataRowModel

    def get_cloud_data_row(self):
        # Collect original objects
        return self._model(**self.get_dict_object()).get_cloud_data_section_row()


class TSO500SDataSection(DataFrameSection):
    """
    https://support-docs.illumina.com/SW/DRAGEN_TSO500_v2.5_ICA/Content/LP/TSO500/AutolaunchSampleSheetSettings.htm
    """

    # Set model
    _model = TSO500SDataSectionModel
    _row_obj = TSO500SDataRowSection

    # Set class name and Header
    _class_header = "TSO500S_Data"


class CloudTSO500SDataSection(TSO500SDataSection):
    _is_cloud = True

    def get_cloud_data_list(self):
        return list(
            map(
                lambda row_iter: self._row_obj(**row_iter).get_cloud_data_row(),
                self._raw_args
            )
        )
