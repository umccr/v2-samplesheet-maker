#!/usr/bin/env python3
from docopt import docopt
import sys

# For __main__ must use absolute imports
# https://docs.python.org/3/tutorial/modules.html#intra-package-references
from v2_samplesheet_maker.classes.samplesheet import SampleSheet
from v2_samplesheet_maker.utils.cli import check_v2_samplesheet_writer_args
from v2_samplesheet_maker.utils.docopt_docs import get_v2_samplesheet_writer_doc_opt


def run_v2_samplesheet():
    """
    Write out v2 samplesheet to main
    :return:
    """

    # Read in v2 samplesheet args
    args = docopt(get_v2_samplesheet_writer_doc_opt())

    # Check args
    args = check_v2_samplesheet_writer_args(args)

    # Read in samplesheet and validate
    samplesheet = SampleSheet(args.get("input-json"))

    # Write out samplesheet to csv
    samplesheet.to_csv(args.get("output-csv"))


def main():
    run_v2_samplesheet()


if __name__ == "__main__":
    main()
