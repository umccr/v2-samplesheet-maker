#!/usr/bin/env python
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Dict

from .logger import set_basic_logger, get_logger

set_basic_logger()

logger = get_logger()


def check_v2_samplesheet_writer_args(args) -> Dict:
    """
    Check the v2 samplesheet args are legit
    :param args: A dictionary with the following keys:
      * <input-json> (Either '-' for /dev/stdin or a file)
      * <output-csv> (Path to an output csv)
    :return: A dictionary with the following keys
      * input-json ( A dictionary containing the samplesheet information)
      * output-csv (Path to an output csv or a file-handle if '-' is specified)
    """
    # Always clone before editing
    args = deepcopy(args)

    # Check input json
    input_json_arg = args.get("<input-json>")

    if input_json_arg == "-":
        input_json = sys.stdin.fileno()
    # Check input_json file exists
    elif not Path(input_json_arg).is_file():
        logger.error(f"Could not read {input_json_arg}")
        raise FileNotFoundError
    else:
        input_json = input_json_arg
    # Read in input json
    with open(input_json, 'r') as input_json_h:
        # Read input
        try:
            input_json_dict = json.loads(input_json_h.read())
        except json.JSONDecodeError:
            logger.error(f"Could not read {input_json_arg} as valid json")
            raise json.JSONDecodeError
        args["input-json"] = input_json_dict

    # Check output csv
    output_csv_arg = args.get("<output-csv>")

    if output_csv_arg == "-":
        output_csv = sys.stdout.fileno()
    elif not Path(output_csv_arg).parent.is_dir():
        logger.error(f"Could not find parent directory '{Path(output_csv_arg).parent}'"
                     f"for '{output_csv_arg}', cannot create file. Please create parent and try again")
        raise NotADirectoryError
    else:
        output_csv = Path(output_csv_arg)

    args["output-csv"] = output_csv

    return args


def check_v2_samplesheet_reader_args(args) -> Dict:
    """
    Check the v2 samplesheet reader args are legit
    :param args: A dictionary with the following keys:
      * <input-csv> (Path to an input csv)
      * <output-json> (Either '-' for /dev/stdout or a file)
    :return: A dictionary with the following keys
      * input-csv ( A v2 samplesheet)
      * output-json (Path to an output json file or a file-handle if '-' is specified)
    """
    # Always clone before editing
    args = deepcopy(args)

    # Check input json
    input_csv_arg = args.get("<input-csv>")

    if input_csv_arg == "-":
        input_csv = sys.stdin.fileno()
    # Check input_csv file exists
    elif not Path(input_csv_arg).is_file():
        logger.error(f"Could not read {input_csv_arg}")
        raise FileNotFoundError
    else:
        input_csv = Path(input_csv_arg)

    # Assign args
    args["input-csv"] = input_csv

    # Check output csv
    output_json_arg = args.get("<output-json>")

    if output_json_arg == "-":
        output_json = sys.stdout.fileno()
    elif not Path(output_json_arg).parent.is_dir():
        logger.error(f"Could not find parent directory '{Path(output_json_arg).parent}'"
                     f"for '{output_json_arg}', cannot create file. Please create parent and try again")
        raise NotADirectoryError
    else:
        output_json = Path(output_json_arg)

    args["output-json"] = output_json

    return args



