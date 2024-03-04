#!/usr/bin/env python3

# Standard imports
from docopt import docopt

# For __main__ must use absolute imports
# https://docs.python.org/3/tutorial/modules.html#intra-package-references
from v2_samplesheet_maker.utils.cli import check_v2_samplesheet_writer_args
from v2_samplesheet_maker.utils.docopt_docs import get_v2_samplesheet_writer_doc_opt
from v2_samplesheet_maker.functions.v2_samplesheet_writer import v2_samplesheet_writer


def run_v2_samplesheet_writer():
    """
    Write out v2 samplesheet to main
    :return:
    """

    # Read in v2 samplesheet args
    args = docopt(get_v2_samplesheet_writer_doc_opt())

    # Check args
    args = check_v2_samplesheet_writer_args(args)

    # Read in samplesheet and validate
    v2_samplesheet_writer(
        args.get("input-json"),
        args.get("output-csv")
    )


def main():
    run_v2_samplesheet_writer()


if __name__ == "__main__":
    main()
