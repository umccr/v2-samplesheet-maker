#!/usr/bin/env python3

"""
Read in a runinfo xml file and return a dictionary of the runinfo data
"""
import json
from io import TextIOBase
from pathlib import Path
from typing import Union, TextIO, Optional, Dict
import xmltodict


def run_info_xml_reader(
    xml_input_path_or_stream: Union[TextIO, Path],
    output_path: Optional[Path] = None,
    keep_flowcell_layout: bool = False,
) -> Optional[Dict]:

    # Read in SampleSheet csv
    if isinstance(xml_input_path_or_stream, TextIOBase):
        run_info_dict = xmltodict.parse(xml_input_path_or_stream.read())
    elif isinstance(xml_input_path_or_stream, Path):
        with open(xml_input_path_or_stream, "r") as xml_h:
            run_info_dict = xmltodict.parse(xml_h.read())
    else:
        raise ValueError(
            f"Input xml path or stream is not a valid type, expected one of TextIO or Path"
            f" but got {type(xml_input_path_or_stream)}"
        )

    # Remove the FlowcellLayout attribute from the run_info_dict
    # The FlowcellLayout is a huge dictionary that is not needed for the run_info_dict
    if not keep_flowcell_layout:
        # Remove the FlowcellLayout attribute from the run_info_dict
        del run_info_dict['RunInfo']['Run']["FlowcellLayout"]

    # Check output path
    if output_path is not None:
        with open(output_path, "w") as output_h:
            json.dump(
                run_info_dict, output_h, indent=4
            )
        return None
    else:
        return run_info_dict

