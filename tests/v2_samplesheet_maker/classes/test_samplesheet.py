#!/usr/bin/env python3
import json

from v2_samplesheet_maker.classes.samplesheet import SampleSheet


class TestSampleSheetSection:
    valid_samplesheet = json.loads(
        """
        {
          "header": {
            "file_format_version": 2,
            "run_name": "my-illumina-sequencing-run",
            "run_description": "A test run",
            "instrument_platform": "NovaSeq 6000",
            "instrument_type": "NovaSeq"
          },
          "reads": {
            "read_1_cycles": 151,
            "read_2_cycles": 151,
            "index_1_cycles": 10,
            "index_2_cycles": 10
          },
          "bclconvert_settings": {
            "adapter_behavior": "trim",
            "adapter_read_1": null,
            "adapter_read_2": null,
            "adapter_stringency": null,
            "barcode_mismatches_index_1": 1,
            "barcode_mismatches_index_2": 1,
            "minimum_trimmed_read_length": null,
            "minimum_adapter_overlap": 2,
            "mask_short_reads": null,
            "override_cycles": "Y151;Y10;Y8N2;Y151",
            "trim_umi": null,
            "create_fastq_for_index_reads": false,
            "no_lane_splitting": false,
            "fastq_compression_format": "gzip",
            "find_adapters_with_indels": null,
            "independent_index_collision_check": null
          },
          "bclconvert_data": [
            {
              "sample_id": "MyFirstSample",
              "lane": 1,
              "index": "AAAAAAAAAA",
              "index2": "CCCCCCCC",
              "sample_project": "SampleProject",
              "sample_name": null
            },
            {
              "sample_id": "MySecondSample",
              "lane": 1,
              "index": "GGGGGGGGGG",
              "index2": "TTTTTTTT",
              "sample_project": "SampleProject",
              "sample_name": null
            }
          ]
        }
        """
    )

    def test_valid_samplesheet(self):
        SampleSheet(self.valid_samplesheet)
