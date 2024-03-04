#!/usr/bin/env python3

"""
Create a function that takes in either an input path or stream,
and an option output path and returns the v2 samplesheet as a StringIO if the output path is not set
or writes the v2 samplesheet to the output path if it is set.
"""

# Standard libraries
from io import StringIO, TextIOBase
from pathlib import Path
from typing import Union, TextIO, Optional, Dict
import json
from tempfile import NamedTemporaryFile

# Local libraries
from ..classes.samplesheet import SampleSheet


def v2_samplesheet_writer(
    json_input_path_or_stream: Union[Dict, TextIO, Path],
    output_path: Optional[Path] = None
) -> Optional[TextIO]:

    # Read in SampleSheet object
    if isinstance(json_input_path_or_stream, Dict):
        samplesheet = SampleSheet(json_input_path_or_stream)
    elif isinstance(json_input_path_or_stream, TextIOBase):
        try:
            json_input_path_or_stream = json.load(json_input_path_or_stream)
        except json.JSONDecodeError:
            raise ValueError("Input stream is not a valid JSON object")
        samplesheet = SampleSheet(json_input_path_or_stream)
    elif isinstance(json_input_path_or_stream, Path):
        # Check path exists
        if not json_input_path_or_stream.exists():
            raise FileNotFoundError(f"File {json_input_path_or_stream} does not exist")
        with open(json_input_path_or_stream, "r") as input_path_h:
            samplesheet = SampleSheet(json.load(input_path_h))
    else:
        raise ValueError(
            f"Input path or stream is not a valid type, expected one of Dict, TextIO or Path"
            f" but got {type(json_input_path_or_stream)}"
        )

    # Write out samplesheet to csv and then stream back in
    if output_path is None:
        with NamedTemporaryFile(suffix='.csv') as tempfile_obj_h:

            # Write out samplesheet to file first
            samplesheet.to_csv(Path(tempfile_obj_h.name))

            # Then read in the file and return it as a string
            with open(tempfile_obj_h.name, "r") as csv_h:
                return StringIO(csv_h.read())

    # Write out samplesheet to regular csv
    else:
        samplesheet.to_csv(output_path)
