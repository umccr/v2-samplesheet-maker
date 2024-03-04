#!/usr/bin/env python3

"""
Read in a v2 samplesheet and output as json
"""

# Standard imports
from docopt import docopt

# Custom imports
from v2_samplesheet_maker.utils.cli import check_v2_samplesheet_to_run_info_xml
from v2_samplesheet_maker.utils.docopt_docs import get_samplesheet_csv_to_run_info_xml_doc_opt
from v2_samplesheet_maker.functions.v2_samplesheet_to_run_info import samplesheet_csv_to_run_info_xml


def v2_samplesheet_to_run_info_xml():
    """
    Convert a v2 samplesheet to a run info xml
    :return:
    """

    # Read in v2 samplesheet args
    args = docopt(get_samplesheet_csv_to_run_info_xml_doc_opt())

    # Check args
    args = check_v2_samplesheet_to_run_info_xml(args)

    # Read in samplesheet and validate
    samplesheet_csv_to_run_info_xml(
        args.get("input-csv"),
        run_id=args.get("run-id"),
        output_path=args.get("output-xml"),
        number=args.get('number'),
        flowcell=args.get('flowcell'),
        instrument=args.get('instrument'),
        date=args.get('date'),
        align_to_phix=args.get('align-to-phix'),
        image_dimensions=args.get('image-dimensions'),
        image_channels=args.get('image-channels')
    )


def main():
    v2_samplesheet_to_run_info_xml()


if __name__ == "__main__":
    main()
