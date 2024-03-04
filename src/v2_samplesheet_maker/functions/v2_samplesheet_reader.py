#!/usr/bin/env python3

"""
Create a function that takes in either an input path or stream of a csv file,
and an option output path and returns the v2 samplesheet as a json object.

If the output path is None, then the function should return a dict object,
otherwise it should write the json object to the output path and return None.

"""

# Standard libraries
from io import TextIOBase
from pathlib import Path
from typing import Union, TextIO, Optional, Dict
import json
from tempfile import NamedTemporaryFile

# Local libraries
from ..classes.samplesheet import SampleSheet


def v2_samplesheet_reader(
    csv_input_path_or_stream: Union[TextIO, Path],
    output_path: Optional[Path] = None
) -> Optional[Dict]:

    # Read in SampleSheet csv
    if isinstance(csv_input_path_or_stream, TextIOBase):
        # Write text to temp file and get samplesheet to read csv from there
        with NamedTemporaryFile(suffix='.csv') as tempfile_obj_h:
            # Write output to temp file
            tempfile_obj_h.write(csv_input_path_or_stream.read().encode())
            # Use flush to make sure all output is written
            tempfile_obj_h.flush()

            # Now read in samplesheet from temp file
            samplesheet = SampleSheet.read_from_samplesheet_csv(Path(tempfile_obj_h.name))

    # Write out samplesheet to json and then stream back in
    elif isinstance(csv_input_path_or_stream, Path):
        samplesheet = SampleSheet.read_from_samplesheet_csv(csv_input_path_or_stream)
    else:
        raise ValueError(
            f"Input csv path or stream is not a valid type, expected one of TextIO or Path"
            f" but got {type(csv_input_path_or_stream)}"
        )

    # Write out samplesheet to csv and then stream back in
    if output_path is None:
        with NamedTemporaryFile(suffix='.json') as tempfile_obj_h:

            # Write out samplesheet to file first
            samplesheet.to_json(Path(tempfile_obj_h.name))

            # Then read in the file and return it as a json object
            with open(tempfile_obj_h.name, "r") as csv_h:
                return json.load(csv_h)

    # Write out samplesheet to regular csv
    else:
        samplesheet.to_json(output_path)
