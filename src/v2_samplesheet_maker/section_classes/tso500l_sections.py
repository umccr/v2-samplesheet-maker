#!/usr/bin/env python3

"""
Define each of the available section_classes
"""

# Relative modules
from ..classes.super_sections import (
    KVSection, DataFrameSection, DataFrameSectionRow
)

# Relative subpackages
from ..models.tso500l_sections import (
    TSO500LSettingsSectionModel,
    TSO500LDataRowModel,
    TSO500LDataSectionModel,
)


class TSO500LSettingsSection(KVSection):
    """
    TSO500L Settings Section
    https://support.illumina.com/content/dam/illumina-support/documents/documentation/software_documentation/trusight/trusight-oncology-500/200034937-00-dragen-trusight-oncology-ctdna-500-analysis-software-v211-ica-user-guide.pdf
    """

    # Set model
    _model = TSO500LSettingsSectionModel

    # Set class name and header
    _class_header = "TSO500L_Settings"


class CloudTSO500LSettingsSection(TSO500LSettingsSection):
    _is_cloud = True


class TSO500LDataRowSection(DataFrameSectionRow):
    """
    A BCLConvert DataRow
    """

    # Set model
    _model = TSO500LDataRowModel


class TSO500LDataSection(DataFrameSection):
    """
    https://support.illumina.com/content/dam/illumina-support/documents/documentation/software_documentation/trusight/trusight-oncology-500/200034937-00-dragen-trusight-oncology-ctdna-500-analysis-software-v211-ica-user-guide.pdf
    """

    # Set model
    _model = TSO500LDataSectionModel
    _row_obj = TSO500LDataRowSection

    # Set class name and Header
    _class_header = "TSO500L_Data"


class CloudTSO500LDataSection(TSO500LDataSection):
    _is_cloud = True
