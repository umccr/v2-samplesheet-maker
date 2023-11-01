#!/usr/bin/env python3

"""
Samplesheet Class
"""
from pathlib import Path
from typing import Dict, Optional

# Relative modules
from .sections import HeaderSection, ReadsSection, BCLConvertSettingsSection, BCLConvertDataSection

# Relative subpackages
from ..utils.logger import get_logger

logger = get_logger()


class SampleSheet:
    """
    SampleSheet object class
    """

    def __init__(self, sections_dict: Dict):
        """

        :param sections_dict:
        """
        self.header_section: Optional[HeaderSection] = None
        self.reads_section: Optional[ReadsSection] = None
        self.bclconvert_settings_section: Optional[BCLConvertSettingsSection] = None
        self.bclconvert_data_section: Optional[BCLConvertDataSection] = None

        for section_name, section_dict_or_list in sections_dict.items():
            if section_name.lower() == "header":
                self.header_section = HeaderSection(**section_dict_or_list)
            elif section_name.lower() == "reads":
                self.reads_section = ReadsSection(**section_dict_or_list)
            elif section_name.lower() == "bclconvert_settings":
                self.bclconvert_settings_section = BCLConvertSettingsSection(**section_dict_or_list)
            elif section_name.lower() == "bclconvert_data":
                self.bclconvert_data_section = BCLConvertDataSection.get_bclconvert_datarows_from_list(section_dict_or_list)
            else:
                logger.error(f"Did not get a known section name '{section_name}' is not a known section name")

    def to_csv(self, output_file: Path):
        """
        Write out the samplesheet in csv format (well ini format but with a csv suffix)
        :return:
        """
        if isinstance(output_file, Path) and not output_file.parent.is_dir():
            logger.error(f"Output file cannot be written because parent {output_file.parent} does not exist")
            raise NotADirectoryError

        with open(output_file, "w") as file_h:
            # Write header section
            file_h.write("[Header]\n")
            file_h.write(self.header_section.to_string())

            # Write reads section
            file_h.write("\n[Reads]\n")
            file_h.write(self.reads_section.to_string())

            # Write out bclconvert settings section if it exists
            if self.bclconvert_settings_section is not None:
                file_h.write("\n[BCLConvert_Settings]\n")
                file_h.write(self.bclconvert_settings_section.to_string())

            # Write out bclconvert data section if it exists
            if self.bclconvert_data_section is not None:
                file_h.write("\n[BCLConvert_Data]\n")
                file_h.write(self.bclconvert_data_section.to_string())

            # End of file

