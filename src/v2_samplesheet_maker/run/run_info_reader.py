#!/usr/bin/env python3

"""
Read in an xml and output as json
"""

# Standard imports
from docopt import docopt

# Custom imports
from v2_samplesheet_maker.utils.cli import check_run_info_reader_args
from v2_samplesheet_maker.utils.docopt_docs import get_run_info_xml_reader_doc_opt
from v2_samplesheet_maker.functions.run_info_reader import run_info_xml_reader


def run_run_info_reader():
    """
    Write out v2 samplesheet to main
    :return:
    """

    # Read in v2 samplesheet args
    args = docopt(get_run_info_xml_reader_doc_opt())

    # Check args
    args = check_run_info_reader_args(args)

    # Read in samplesheet and validate
    run_info_xml_reader(
        args.get("input-xml"),
        args.get("output-json")
    )


def main():
    run_run_info_reader()


if __name__ == "__main__":
    main()
