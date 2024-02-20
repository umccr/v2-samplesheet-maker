#!/usr/bin/env python3

"""
Samplesheet Class
"""
# Standard Libraries
import json
from pathlib import Path
from typing import Dict, Optional, List, Union
import pandas as pd
from tempfile import NamedTemporaryFile

# Relative modules
from ..utils.logger import get_logger
from ..utils import pascal_case_to_snake_case
from .super_sections import Section, KVSection, DataFrameSection
from ..section_classes.run_info_sections import (
    HeaderSection, ReadsSection, SequencingSection
)
from ..section_classes.bcl_convert_sections import (
    BCLConvertSettingsSection, BCLConvertDataSection
)
from ..section_classes.cloud_sections import (
    CloudSettingsSection, CloudDataSection
)
from ..section_classes.tso500l_sections import (
    TSO500LSettingsSection,
    CloudTSO500LSettingsSection,
    TSO500LDataSection,
    CloudTSO500LDataSection
)

# Get logging
logger = get_logger()


def get_stripped_section_name(section_name: str) -> str:
    """
    Cloud_TSO500L_Settings to tso500l_settings,
    Cloud_Settings to cloud_settings
    :param section_name:
    :return:
    """
    return (
        section_name.lower().lstrip("cloud_") if
        not section_name.lower() == "cloud_settings" and
        not section_name.lower() == "cloud_data"
        else
        section_name.lower()
    )


def is_cloud_section_name(section_name: str) -> bool:
    """
    Cloud_TSO500L_Settings -> True
    Cloud_Settings -> False
    Reads -> False
    :param section_name:
    :return:
    """
    return (
            section_name.lower().startswith("cloud_") and
            not section_name.lower() == "cloud_settings" and
            not section_name.lower() == "cloud_data"
    )


class SampleSheet:
    """
    SampleSheet object class
    """

    _all_sections: List[Section] = [
        # Run Info
        HeaderSection,
        ReadsSection,
        SequencingSection,
        # BCLConvert
        BCLConvertSettingsSection,
        BCLConvertDataSection,
        # Cloud Settings
        CloudSettingsSection,
        CloudDataSection,
        # TSO500L (Local and Cloud)
        TSO500LSettingsSection,
        CloudTSO500LSettingsSection,
        TSO500LDataSection,
        CloudTSO500LDataSection,
    ]

    # Import Cloud settings last
    # so we can copy over the urns from each of the settings
    # Cloud_Data should also be last so we can
    _import_sections_order = [
        section_item
        for section_item in _all_sections
        if section_item not in [
            CloudSettingsSection,
            CloudDataSection
        ]
    ] + [
        CloudSettingsSection,
        CloudDataSection
    ]

    def __init__(self, sections_dict: Dict):
        """

        :param sections_dict:
        """
        # Make as function
        class_headers_as_list = list(
            map(lambda y: y._class_header.lower(), self._import_sections_order)
        )
        sections_dict_as_list = sorted(
            map(
                lambda dict_iter: {
                    dict_iter[0]: dict_iter[1]
                },
                sections_dict.items()
            ),
            # Order by _import_sections_order
            key=lambda x: class_headers_as_list.index(get_stripped_section_name(list(x.keys())[0]))
        )

        # Run Info Section
        self.header_section: Optional[HeaderSection] = None
        self.reads_section: Optional[ReadsSection] = None
        self.sequencing_section: Optional[SequencingSection] = None

        # BCLConvert Sections
        self.bclconvert_settings_section: Optional[BCLConvertSettingsSection] = None
        self.bclconvert_data_section: Optional[BCLConvertDataSection] = None

        # Cloud Section
        self.cloud_settings_section: Optional[CloudSettingsSection] = None
        self.cloud_data_section: Optional[CloudDataSection] = None

        # TSO500 Section (can be both cloud and non-cloud)
        self.tso500l_settings_section: Optional[Union[TSO500LSettingsSection|CloudTSO500LSettingsSection]] = None
        self.tso500l_data_section: Optional[Union[TSO500LDataSection|CloudTSO500LDataSection]] = None

        # Initialise the section list
        self.section_list = []  # List of non-empty sections

        # Now populate the sections
        self.populate_sections(sections_dict_as_list)

    def populate_sections(self, sections_dict_as_list):
        # We place urns inside the settings of the application, these are then moved to the Cloud_Settings section
        cloud_analysis_urns_dict = {}
        cloud_data_list: List[Dict] = []
        urs_bool_list: Dict = {}
        has_bclconvert_urn = False

        # Check first if there's a cloud data section
        has_cloud_data_section = any(
            [
                get_stripped_section_name(section_name_iter) == "cloud_data"
                for section_dict_iter in sections_dict_as_list
                for section_name_iter in section_dict_iter.keys()
            ]
        )

        # Iterate over sections dict
        for section_dict in sections_dict_as_list:
            # Iterate over single dict
            for section_name, section_dict_or_list in section_dict.items():
                try:
                    stripped_section_name = get_stripped_section_name(section_name)
                    is_cloud_name = is_cloud_section_name(section_name)
                    # Get section type
                    section_type: Section = next(
                        filter(
                            lambda section_type_iter: (
                                section_type_iter._class_header.lower() == stripped_section_name and
                                is_cloud_name == section_type_iter._is_cloud
                            ),
                            self._all_sections
                        )
                    )
                except StopIteration:
                    logger.error(f"Did not get a known section name '{section_name}' is not a known section name")
                    raise ValueError

                if section_type == CloudSettingsSection:
                    # Check if we have any existing analysis urns
                    if (
                            section_dict_or_list.get("analysis_urns", None) is not None and
                            isinstance(section_dict_or_list.get("analysis_urns"), dict)
                    ):
                        cloud_analysis_urns_dict.update(
                            section_dict_or_list.get("analysis_urns")
                        )
                    section_dict_or_list.update(
                        {
                            "analysis_urns": cloud_analysis_urns_dict
                        }
                    )

                if issubclass(section_type, KVSection):
                    setattr(self, f"{section_type._class_header.lower()}_section", section_type(**section_dict_or_list))
                elif issubclass(section_type, DataFrameSection):
                    setattr(self, f"{section_type._class_header.lower()}_section", section_type(*section_dict_or_list))
                else:
                    logger.error(f"Section Type {section_type._class_header} for section name {section_name} is neither a key-value section nor a data section")
                    raise ValueError

                # Collect the section object
                section_obj = getattr(self, f"{section_type._class_header.lower()}_section")

                # Update the cloud analysis urns dict
                if is_cloud_name and issubclass(section_type, KVSection):
                    if hasattr(section_obj, "urn") and section_obj.urn is not None:
                        cloud_analysis_urns_dict.update(
                            {
                                "Cloud_" + section_type._class_header.rstrip("_Settings") + "_Pipeline": getattr(section_obj, "urn")
                            }
                        )
                        urs_bool_list[stripped_section_name.replace("_settings", "_data")] = True
                elif stripped_section_name == "bclconvert_settings":
                    if hasattr(section_obj, "urn") and section_obj.urn is not None:
                        urs_bool_list[stripped_section_name.replace("_settings", "_data")] = True
                        cloud_analysis_urns_dict.update(
                            {
                                "BCLConvert_Pipeline": getattr(section_obj, "urn")
                            }
                        )

                # Update the Cloud Data section if no Cloud_Data section
                if (
                        urs_bool_list.get(stripped_section_name, False) and
                        not has_cloud_data_section
                ):
                    # Coerce section type
                    section_type: BCLConvertDataSection
                    setattr(self, f"cloud_data_section", CloudDataSection(*section_type(*section_dict_or_list).get_cloud_data_list()))
        # Set section list
        self.section_list = list(
            map(
                lambda dict_iter: dict_iter[0],
                sorted(
                    filter(
                        lambda attribute_item: attribute_item[0].endswith("_section") and not attribute_item[1] is None,
                        self.__dict__.items()
                    ),
                    # Order by sections list above
                    key=lambda section_iter: self._all_sections.index(type(section_iter[1]))
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

    def to_json(self, output_file: Path):
        """
        Write out the samplesheet in json format
        We use this in the samplesheet reader
        :param output_file:
        :return:
        """
        # Check if output file is a valid writable path
        if isinstance(output_file, Path) and not output_file.parent.is_dir():
            logger.error(f"Output file cannot be written because parent {output_file.parent} does not exist")
            raise NotADirectoryError

        # Write sections to jsonlines file
        temp_jsonl_file = NamedTemporaryFile(suffix=".jsonl")
        with open(temp_jsonl_file.name, "w") as file_h:
            for index, section_item in enumerate(self.section_list):
                section_obj: Section = getattr(self, section_item)
                section_obj.write_section_json(file_h)
                file_h.write("\n")

        # Read in jsonlines from temp fileins
        samplesheet_dict = {}
        with open(temp_jsonl_file.name, "r") as file_h:
            for line in file_h:
                samplesheet_dict.update(json.loads(line.strip()))

        # Write out to json file
        with open(output_file, "w") as file_h:
            json.dump(
                samplesheet_dict,
                file_h,
                indent=2
            )
            # Write final newline
            file_h.write("\n")

    @classmethod
    def read_from_samplesheet_csv(cls, samplesheet_csv: Path) -> "SampleSheet":
        """
        Read in a samplesheet from a csv file
        :param samplesheet_csv:
        :return:
        """
        if not samplesheet_csv.is_file():
            logger.error(f"Samplesheet file {samplesheet_csv} does not exist")
            raise FileNotFoundError

        # Read in the samplesheet
        with open(samplesheet_csv, "r") as file_h:
            samplesheet_dict = {}
            section_name = None
            section_lines = []
            # Iterate through all lines
            for line in file_h:
                # Strip ending of line
                line = line.strip()

                # Skip empty values
                if line == "":
                    continue

                # Check if header
                if line.startswith("[") and line.endswith("]"):
                    if section_name is not None:
                        samplesheet_dict[section_name] = section_lines
                    section_name = line.lstrip("[").rstrip("]")
                    section_lines = []
                else:
                    section_lines.append(line)
            # Add the last section
            if section_name is not None:
                samplesheet_dict[section_name] = section_lines
            else:
                # Not sure how we got here
                logger.error(f"Did not get a section name")
                raise ValueError

        # Convert all pascal case to snake case for both section names and values
        samplesheet_dict_sanitised = {}
        for section_name, section_lines in samplesheet_dict.items():
            sanitised_section_name = pascal_case_to_snake_case(section_name)

            if sanitised_section_name.endswith("_data"):
                # This should be a list of dicts
                sanitised_section_values = pd.DataFrame(
                    columns=list(
                        map(
                            lambda header_iter: pascal_case_to_snake_case(header_iter),
                            section_lines[0].split(",")
                        )
                    ),
                    data=list(
                        map(
                            lambda row_iter: row_iter.split(","),
                            section_lines[1:]
                        )
                    )
                )
                sanitised_section_values = sanitised_section_values.to_dict(orient="records")
            else:
                # This should be a set of key, value pairs
                sanitised_section_values = {
                    pascal_case_to_snake_case(line_iter.split(",")[0]): line_iter.split(",")[1]
                    for line_iter in section_lines
                }

            # Update the new samplesheet dict
            samplesheet_dict_sanitised[sanitised_section_name] = sanitised_section_values

        # Perform exception to Sequence model library_prep_kits and convert to a list
        if "sequencing" in samplesheet_dict_sanitised.keys():
            if "library_prep_kits" in samplesheet_dict_sanitised["sequencing"].keys():
                samplesheet_dict_sanitised["sequencing"]["library_prep_kits"] = (
                    samplesheet_dict_sanitised["sequencing"]["library_prep_kits"].split(";")
                )

        # Perform exception to Cloud_Settings, find all keys that end with _pipeline and append to analysis_urns dict
        if "cloud_settings" in samplesheet_dict_sanitised.keys():
            cloud_settings = samplesheet_dict_sanitised["cloud_settings"]
            cloud_analysis_urns = {}
            for key, value in cloud_settings.items():
                if key.endswith("_pipeline") and value.startswith("urn:"):
                    cloud_analysis_urns[key] = value
            cloud_settings["analysis_urns"] = cloud_analysis_urns
            samplesheet_dict_sanitised["cloud_settings"] = cloud_settings


        # Return the samplesheet object
        return cls(samplesheet_dict_sanitised)
