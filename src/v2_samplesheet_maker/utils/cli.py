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
        # input_csv = sys.stdin.fileno()
        input_csv = sys.stdin
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


def check_run_info_reader_args(args) -> Dict:
    """
    Check the run info reader args are legit
    :param args: A dictionary with the following keys:
      * <input-xml> (Path to an input xml)
      * <output-json> (Either '-' for /dev/stdout or a file)
    :return: A dictionary with the following keys
      * input-xml ( A Run Info xml)
      * output-json (Path to an output json file or a file-handle if '-' is specified)
    """
    # Always clone before editing
    args = deepcopy(args)

    # Check input json
    input_xml_arg = args.get("<input-xml>")

    if input_xml_arg == "-":
        # input_csv = sys.stdin.fileno()
        input_xml = sys.stdin
    # Check input_xml file exists
    elif not Path(input_xml_arg).is_file():
        logger.error(f"Could not read {input_xml_arg}")
        raise FileNotFoundError
    else:
        input_xml = Path(input_xml_arg)

    # Assign args
    args["input-xml"] = input_xml

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


def check_run_info_xml_writer_args(args) -> Dict:
    """
    Check the run info args are legit
    :param args: A dictionary with the following keys:
      * <input-json> (Either '-' for /dev/stdin or a file)
      * <output-xml> (Path to an output xml)
    :return: A dictionary with the following keys
      * input-xml ( A dictionary containing the samplesheet information)
      * output-xml (Path to an output csv or a file-handle if '-' is specified)
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

    # Check output xml
    output_xml_arg = args.get("<output-xml>")

    if output_xml_arg == "-":
        output_xml = sys.stdout.fileno()
    elif not Path(output_xml_arg).parent.is_dir():
        logger.error(f"Could not find parent directory '{Path(output_xml_arg).parent}'"
                     f"for '{output_xml_arg}', cannot create file. Please create parent and try again")
        raise NotADirectoryError
    else:
        output_xml = Path(output_xml_arg)

    args["output-xml"] = output_xml

    return args


def check_v2_samplesheet_to_run_info_xml(args) -> Dict:
    """
    Check the samplesheet to run info xml args are legit
    :param args: A dictionary with the following keys:
      * <input-csv> (Path to an input csv)
      * <output-xml> (Either '-' for /dev/stdout or a file)
      * --run-id: The run id
      * --run-number: The run number
      * --flowcell: The flowcell
      * --instrument: The instrument
      * --date: The date
    :return: A dictionary with the following keys
      * input-csv ( A v2 samplesheet)
      * output-xml (Path to an output xml file or a file-handle if '-' is specified)
      * run-number
      * flowcell
      * instrument
      * date
    """
    # Always clone before editing
    args = deepcopy(args)

    # Check input json
    input_csv_arg = args.get("<input-csv>")

    if input_csv_arg == "-":
        # input_csv = sys.stdin.fileno()
        input_csv = sys.stdin
    # Check input_csv file exists
    elif not Path(input_csv_arg).is_file():
        logger.error(f"Could not read {input_csv_arg}")
        raise FileNotFoundError
    else:
        input_csv = Path(input_csv_arg)

    # Assign args
    args["input-csv"] = input_csv

    # Check output xml
    output_xml_arg = args.get("<output-xml>")

    if output_xml_arg == "-":
        output_xml = sys.stdout.fileno()
    elif not Path(output_xml_arg).parent.is_dir():
        logger.error(f"Could not find parent directory '{Path(output_xml_arg).parent}'"
                     f"for '{output_xml_arg}', cannot create file. Please create parent and try again")
        raise NotADirectoryError
    else:
        output_xml = Path(output_xml_arg)

    args["output-xml"] = output_xml

    # Check run id
    run_id = args.get("--run-id")
    if not run_id:
        logger.error(f"Please specify a run id")
        raise ValueError
    args["run-id"] = run_id

    # Check optional inputs
    for optional_input in ["run-number", "instrument", "flowcell", "date"]:
        if args.get(f"--{optional_input}", None) is not None:
            args[optional_input] = args[f"--{optional_input}"]

    return args
