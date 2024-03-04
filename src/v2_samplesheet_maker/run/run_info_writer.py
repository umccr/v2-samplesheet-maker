#!/usr/bin/env python3

# Standard imports
from docopt import docopt

# For __main__ must use absolute imports
# https://docs.python.org/3/tutorial/modules.html#intra-package-references
from v2_samplesheet_maker.utils.cli import check_run_info_xml_writer_args
from v2_samplesheet_maker.utils.docopt_docs import get_run_info_xml_writer_doc_opt
from v2_samplesheet_maker.functions.run_info_writer import run_info_xml_writer


def run_run_info_xml_writer():
    """
    Write out v2 samplesheet to main
    :return:
    """

    # Read in v2 samplesheet args
    args = docopt(get_run_info_xml_writer_doc_opt())

    # Check args
    args = check_run_info_xml_writer_args(args)

    # Read in samplesheet and validate
    run_info_xml_writer(
        args.get("input-json"),
        args.get("output-csv")
    )


def main():
    run_run_info_xml_writer()


if __name__ == "__main__":
    main()
