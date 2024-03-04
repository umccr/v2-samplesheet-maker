#!/usr/bin/env python3

"""
Given a samplesheet json input, create a run info xml json

One could imply that this function could be used to generate a RunInfo.xml file from a SampleSheet.csv,

but we let the other functions to the rest of the work on that front.
"""

# Standard libraries
from io import TextIOBase
from tempfile import NamedTemporaryFile
from pathlib import Path
from typing import Optional, Dict, Union, TextIO
from datetime import datetime

# Local libraries
from ..section_classes.run_info_sections import ReadsSection
from ..classes.samplesheet import SampleSheet


def samplesheet_to_run_info_json(
    samplesheet: SampleSheet,
    run_id: str,
    number: Optional[int] = None,
    flowcell: Optional[int] = None,
    instrument: Optional[str] = None,
    date: Optional[datetime] = None,
    align_to_phix: Optional[bool] = None,
    image_dimensions: Optional[Dict] = None,
    image_channels: Optional[Dict] = None,
) -> Optional[Dict]:

    # From a SampleSheet object - we need to collect the reads
    reads_section: ReadsSection = samplesheet.reads_section

    # Collect index cycles
    read_1_cycles = getattr(reads_section, "read_1_cycles")
    read_2_cycles = getattr(reads_section, "read_2_cycles", None)
    index_1_cycles = getattr(reads_section, "index_1_cycles")
    index_2_cycles = getattr(reads_section, "index_2_cycles", None)

    # Generate xml json
    reads_list = []
    index_iter = 0

    for (section_name, section) in zip(
            ["read_1_cycles", "index_1_cycles", "index_2_cycles", "read_2_cycles"],
            [read_1_cycles, index_1_cycles, index_2_cycles, read_2_cycles]
    ):
        if section is None:
            continue
        # Update index iterable
        index_iter += 1
        reads_list.append({
            "@Number": index_iter,
            "@NumCycles": section,
            "@IsIndexedRead": "N" if section_name.startswith("read") else "Y"
        })

    run_dict = {
        "@Id": run_id,
        "Reads": {
            "Read": reads_list
        }
    }

    # Append optional fields
    if number is not None:
        run_dict["@Number"] = number
    if flowcell is not None:
        run_dict["Flowcell"] = flowcell
    if instrument is not None:
        run_dict["Instrument"] = instrument
    if date is not None:
        # "2/29/2024 12:27:04 PM"
        run_dict["Date"] = date.strftime("%m/%d/%Y %I:%M:%S %p")
    if align_to_phix is not None:
        run_dict["AlignToPhiX"] = "Y" if align_to_phix else None
    if image_dimensions is not None:
        run_dict["ImageDimensions"] = image_dimensions
    if image_channels is not None:
        run_dict["ImageChannels"] = image_channels

    return {
        "Run": run_dict
    }


def samplesheet_csv_to_run_info_xml(
    csv_input_path_or_stream: Union[TextIO, Path],
    run_id: str,
    output_path: Optional[Path] = None,
    number: Optional[int] = None,
    flowcell: Optional[int] = None,
    instrument: Optional[str] = None,
    date: Optional[datetime] = None,
    align_to_phix: Optional[bool] = None,
    image_dimensions: Optional[Dict] = None,
    image_channels: Optional[Dict] = None
) -> Optional[Dict]:
    # Convert run info json to xml
    from .run_info_writer import run_info_xml_writer

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

    # Convert samplesheet to run info json
    run_info_json = samplesheet_to_run_info_json(
        samplesheet=samplesheet,
        run_id=run_id,
        number=number,
        flowcell=flowcell,
        instrument=instrument,
        date=date,
        align_to_phix=align_to_phix,
        image_dimensions=image_dimensions,
        image_channels=image_channels
    )

    if output_path is None:
        return run_info_xml_writer(
            json_input_path_or_stream=run_info_json
        )
    else:
        run_info_xml_writer(
            json_input_path_or_stream=run_info_json,
            output_path=output_path
        )
        return None

