#!/usr/bin/env python3

"""
Define each of the available section_classes
"""

# Relative modules
from ..classes.super_sections import KVSection

# Relative subpackages
from ..models.run_info_sections import (
    HeaderSectionModel, ReadsSectionModel, SequencingSectionModel
)


class HeaderSection(KVSection):
    """
    The header section contains much of the experiment management configurations
    https://support-docs.illumina.com/SHARE/SampleSheetv2/Content/SHARE/SampleSheetv2/SectionsRunSetup.htm
    """
    _model = HeaderSectionModel
    _class_header = "Header"


class ReadsSection(KVSection):
    """
    The reads section contains the cycle information
    https://support-docs.illumina.com/SHARE/SampleSheetv2/Content/SHARE/SampleSheetv2/SectionsRunSetup.htm
    """
    # Set model
    _model = ReadsSectionModel
    _class_header = "Reads"


class SequencingSection(KVSection):
    """
    The reads section contains the cycle information
    https://support-docs.illumina.com/SHARE/SampleSheetv2/Content/SHARE/SampleSheetv2/Parameters.htm
    """
    # Set model
    _model = SequencingSectionModel
    _class_header = "Sequencing"
