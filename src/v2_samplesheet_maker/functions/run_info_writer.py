#!/usr/bin/env python3

"""
Given a dictionary,

{
  "RunInfo": {
    "@Version": "5",
    "Run": {
      "@Id": "240229_A01052_0184_AHNVH5DMXY",
      "@Number": "184",
      "Flowcell": "HNVH5DMXY",
      "Instrument": "A01052",
      "Date": "2/29/2024 12:27:04 PM",
      "Reads": {
        "Read": [
          {
            "@Number": "1",
            "@NumCycles": "151",
            "@IsIndexedRead": "N"
          },
          {
            "@Number": "2",
            "@NumCycles": "8",
            "@IsIndexedRead": "Y"
          },
          {
            "@Number": "3",
            "@NumCycles": "8",
            "@IsIndexedRead": "Y"
          },
          {
            "@Number": "4",
            "@NumCycles": "151",
            "@IsIndexedRead": "N"
          }
        ]
      },
      "AlignToPhiX": null,
      "ImageDimensions": {
        "@Width": "3200",
        "@Height": "3607"
      },
      "ImageChannels": {
        "Name": [
          "RED",
          "GREEN"
        ]
      }
    }
  }
}


generate an xml file with the following format:

<?xml version="1.0" encoding="utf-8"?>
<RunInfo Version="5">
        <Run Id="240229_A01052_0184_AHNVH5DMXY" Number="184">
                <Flowcell>HNVH5DMXY</Flowcell>
                <Instrument>A01052</Instrument>
                <Date>2/29/2024 12:27:04 PM</Date>
                <Reads>
                        <Read Number="1" NumCycles="151" IsIndexedRead="N"/>
                        <Read Number="2" NumCycles="8" IsIndexedRead="Y"/>
                        <Read Number="3" NumCycles="8" IsIndexedRead="Y"/>
                        <Read Number="4" NumCycles="151" IsIndexedRead="N"/>
                </Reads>
                <AlignToPhiX/>
                <ImageDimensions Width="3200" Height="3607"/>
                <ImageChannels>
                        <Name>RED</Name>
                        <Name>GREEN</Name>
                </ImageChannels>
        </Run>
</RunInfo>
"""

# Standard libraries
from io import StringIO, TextIOBase
from pathlib import Path
from typing import Union, TextIO, Optional, Dict
import json
import xmltodict
import re
from datetime import datetime


def run_info_xml_writer(
    json_input_path_or_stream: Union[Dict, TextIO, Path],
    output_path: Optional[Path] = None
) -> Optional[TextIO]:

    # Read in SampleSheet object
    if isinstance(json_input_path_or_stream, Dict):
        pass
    elif isinstance(json_input_path_or_stream, TextIOBase):
        try:
            json_input_path_or_stream = json.load(json_input_path_or_stream)
        except json.JSONDecodeError:
            raise ValueError("Input stream is not a valid JSON object")
    elif isinstance(json_input_path_or_stream, Path):
        # Check path exists
        if not json_input_path_or_stream.exists():
            raise FileNotFoundError(f"File {json_input_path_or_stream} does not exist")
        with open(json_input_path_or_stream, "r") as input_path_h:
            json_input_path_or_stream = json.load(input_path_h)
    else:
        raise ValueError(
            f"Input path or stream is not a valid type, expected one of Dict, TextIO or Path"
            f" but got {type(json_input_path_or_stream)}"
        )

    # Generate XML
    if output_path is None:
        return StringIO(xmltodict.unparse(json_input_path_or_stream, pretty=True))
    else:
        with open(output_path, "w") as output_path_h:
            output_path_h.write(xmltodict.unparse(json_input_path_or_stream, pretty=True))
            output_path_h.write("\n")


def generate_run_info_xml_from_minimal_inputs(
    input_dict: Dict,
):
    # Check Run ID Number
    if input_dict["Run"].get("@Id") is None:
        raise ValueError("Expected to have a Run.@ID attribute")

    # Set RunInfo Version
    if input_dict.get("@Version") is None:
        input_dict["@Version"] = "5"

    # Get @Number, Flowcell, Instrument and Date from @ID
    # Assume @ID is in the format: YYMMDD_INSTRUMENT_NUMBER_A|B_FLOWCELL 240229_A01052_0184_AHNVH5DMXY
    run_id = input_dict["Run"]["@Id"]

    # Check optional inputs
    number = input_dict["Run"].get("@Number", None)
    flowcell = input_dict["Run"].get("Flowcell", None)
    instrument = input_dict["Run"].get("Instrument", None)
    date = input_dict["Run"].get("Date", None)

    # Check if any of the optional inputs are None
    if any(map(lambda x: x is None, [number, flowcell, instrument, date])):
        # Check if run_id is in the expected format
        run_id_regex = re.match(r"(\d{6})_([A-Z0-9]+)_(\d+)_A|B([A-Z0-9]+)", run_id)

        if run_id_regex is None:
            raise ValueError(
                f"Run ID {run_id} does not match the expected format, you must manually specify each of "
                f"@Number, Flowcell, Instrument and Date"
            )

        # Set @Number, Flowcell, Instrument and Date
        number = str(int(run_id_regex.group(3)))
        flowcell = run_id_regex.group(4)
        instrument = run_id_regex.group(2)
        date = datetime.strptime(run_id_regex.group(1), "%y%m%d").strftime("%m/%d/%Y") + " 12:00:00 AM"

        # Update input_dict
        input_dict["Run"]["@Number"] = number
        input_dict["Run"]["Flowcell"] = flowcell
        input_dict["Run"]["Instrument"] = instrument
        input_dict["Run"]["Date"] = date

        # Set AlignToPhix
        if input_dict["Run"].get("AlignToPhiX") is None:
            input_dict["Run"]["AlignToPhiX"] = None

        # Set ImageDimensions
        if input_dict["Run"].get("ImageDimensions") is None:
            input_dict["Run"]["ImageDimensions"] = {
                "@Width": "3200",
                "@Height": "3607"
            }

        # Set ImageChannels
        if input_dict["Run"].get("ImageChannels") is None:
            input_dict["Run"]["ImageChannels"] = {
                "Name": [
                    "RED",
                    "GREEN"
                ]
            }

    return generate_run_info_xml_from_minimal_inputs(
        {
            "RunInfo": input_dict
        }
    )
