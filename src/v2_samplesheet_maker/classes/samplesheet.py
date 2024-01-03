#!/usr/bin/env python3

"""
Samplesheet Class
"""
from pathlib import Path
from typing import Dict, Optional, List

from .super_sections import Section, KVSection, DataFrameSection
# Relative modules
from ..section_classes.run_info_sections import (
    HeaderSection, ReadsSection, SequencingSection
)
from ..section_classes.bcl_convert_sections import (
    BCLConvertSettingsSection, BCLConvertDataSection
)
from ..section_classes.cloud_sections import (
    CloudSettingsSection, CloudDataSection
)

# Relative subpackages
from ..utils.logger import get_logger

logger = get_logger()


class SampleSheet:
    """
    SampleSheet object class
    """

    _all_sections: List[Section] = [
        HeaderSection,
        ReadsSection,
        SequencingSection,
        BCLConvertSettingsSection,
        BCLConvertDataSection,
        CloudSettingsSection,
        CloudDataSection
    ]

    def __init__(self, sections_dict: Dict):
        """

        :param sections_dict:
        """
        # Run Info Section
        self.header_section: Optional[HeaderSection] = None
        self.reads_section: Optional[ReadsSection] = None
        self.sequencing_section: Optional[SequencingSection] = None

        # BCLConvert Sections
        self.bclconvert_settings_section: Optional[BCLConvertSettingsSection] = None
        self.bclconvert_data_section: Optional[BCLConvertDataSection] = None

        # Cloud Section
        self.cloud_settings_section: Optional[CloudSettingsSection] = None
        self.cloud_data_section: Optional[CloudDataSection]

        self.section_list = []  # List of non-empty sections

        self.populate_sections(sections_dict)

    def populate_sections(self, sections_dict):
        # Iterate over sections dict
        for section_name, section_dict_or_list in sections_dict.items():
            try:
                section_type: Section = next(
                    filter(
                        lambda section_type_iter: section_type_iter._class_header.lower() == section_name.lower(),
                        self._all_sections
                    )
                )
            except StopIteration:
                logger.error(f"Did not get a known section name '{section_name}' is not a known section name")
                raise ValueError

            if issubclass(section_type, KVSection):
                setattr(self, f"{section_type._class_header.lower()}_section", section_type(**section_dict_or_list))
            elif issubclass(section_type, DataFrameSection):
                setattr(self, f"{section_type._class_header.lower()}_section", section_type(*section_dict_or_list))
            else:
                logger.error(f"Section Type {section_type._class_header} for section name {section_name} is neither a key-value section nor a data section")
                raise ValueError

        # Set section list
        self.section_list = list(
            map(
                lambda dict_iter: dict_iter[0],
                filter(
                    lambda attribute_item: attribute_item[0].endswith("_section") and not attribute_item[1] is None,
                    self.__dict__.items()
                )
            )
        )

    def to_csv(self, output_file: Path):
        """
        Write out the samplesheet in csv format (well ini format but with a csv suffix)
        :return:
        """
        if isinstance(output_file, Path) and not output_file.parent.is_dir():
            logger.error(f"Output file cannot be written because parent {output_file.parent} does not exist")
            raise NotADirectoryError

        with open(output_file, "w") as file_h:
            for index, section_item in enumerate(self.section_list):
                add_new_line_after_section: bool = False if index == len(self.section_list) - 1 else True
                section_obj: Section = getattr(self, section_item)
                section_obj.write_section(file_h, add_new_line_after_section=add_new_line_after_section)


