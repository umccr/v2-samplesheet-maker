#!/usr/bin/env python
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Dict

from .logger import set_basic_logger, get_logger

set_basic_logger()

logger = get_logger()


def check_v2_samplesheet_args(args) -> Dict:
    """
    Check the v2 samplesheet args are legit
    :param args: A dictionary with the following keys:
      * <input-json> (Either '-' for /dev/stdin or a file)
      * <output-csv> (Path to an output csv)
    :return: A dictionary with the following keys
      * input-json ( A dictionary containing the samplesheet information)
      * output-csv (Path to an output csv or a file-handle if '-' is specified)  # TODO
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






