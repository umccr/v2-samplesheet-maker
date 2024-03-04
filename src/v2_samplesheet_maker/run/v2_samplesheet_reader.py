#!/usr/bin/env python3

"""
Read in a v2 samplesheet and output as json
"""

# Standard imports
from docopt import docopt

# Custom imports
from v2_samplesheet_maker.utils.cli import check_v2_samplesheet_reader_args
from v2_samplesheet_maker.utils.docopt_docs import get_v2_samplesheet_reader_doc_opt
from v2_samplesheet_maker.functions.v2_samplesheet_reader import v2_samplesheet_reader


def read_v2_samplesheet():
    """
    Write out v2 samplesheet to main
    :return:
    """

    # Read in v2 samplesheet args
    args = docopt(get_v2_samplesheet_reader_doc_opt())

    # Check args
    args = check_v2_samplesheet_reader_args(args)

    # Read in samplesheet and validate
    v2_samplesheet_reader(
        args.get("input-csv"),
        args.get("output-json")
    )


def main():
    read_v2_samplesheet()


if __name__ == "__main__":
    main()
