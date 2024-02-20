#!/usr/bin/env python3

"""
Read in a v2 samplesheet and output as json
"""
import sys
from pathlib import Path

from docopt import docopt

from v2_samplesheet_maker.utils.cli import check_v2_samplesheet_reader_args
from v2_samplesheet_maker.utils.docopt_docs import get_v2_samplesheet_reader_doc_opt
from v2_samplesheet_maker.classes.samplesheet import SampleSheet


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
    samplesheet = SampleSheet.read_from_samplesheet_csv(args.get("input-csv"))

    # Write out samplesheet to csv
    samplesheet.to_json(args.get("output-json"))


def main():
    read_v2_samplesheet()


if __name__ == "__main__":
    main()
