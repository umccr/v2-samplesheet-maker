#!/usr/bin/env python3

"""
Write an xml file to json and vice-versa
"""
from pathlib import Path
from typing import Optional, Dict

import xmltodict
import json


def xml_to_json(xml_file: Path, output_path: Optional[Path] = None) -> Optional[Dict]:
    """
    Convert a xml file to a json file

    :param xml_file:  Path to the xml file to read
    :param output_path:  Path to the json file to write.  If None, return the json data

    :return: If output_path is None, return the json data.  Otherwise, return None
    """
    # Open an xml file to read
    with open(xml_file) as xml_h:
        data_dict = xmltodict.parse(xml_h.read())

    if output_path is not None:
        # Make sure the parent path exists first
        # Fail if it doesn't exist
        if not output_path.parent.exists():
            raise FileNotFoundError(f"Parent path {output_path.parent} does not exist")

        # Write the json file
        with open(output_path, 'w') as json_h:
            json.dump(data_dict, json_h)
    else:
        return data_dict


def json_to_xml(json_file: Path, output_path: Optional[Path] = None) -> Optional[str]:
    """
    Write out a json file

    :param json_file:
    :param output_path:

    :return: If output_path is None, return the xml string.  Otherwise, return None
    """

    # Open up the json file
    with open(json_file, 'r') as json_h:
        data_dict = json.load(json_h)

    xml_str = xmltodict.unparse(
        data_dict
    )

    if output_path is not None:
        # Check first to see if the parent exists
        # Fail if it doesn't
        if not output_path.parent.exists():
            raise FileNotFoundError(f"Parent path {output_path.parent} does not exist")

        # Write out the xml file
        with open(output_path, 'w') as xml_h:
            xml_h.write(xml_str)
            xml_h.write('\n')
    else:
        return xml_str
