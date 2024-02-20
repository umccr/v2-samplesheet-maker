#!/usr/bin/env python

def get_v2_samplesheet_writer_doc_opt():
    return """
Usage:
v2-samplesheet-maker <input-json> <output-csv>

Options:

* input-json: Path to the input json you wish to convert to the samplesheet csv. Use '-' for stdin.
* output-csv: Path to the output-csv. Use '-' to write to stdout

Example:
v2-samplesheet-maker /path/to/input.json SampleSheet.csv

Description:
Given a json file, write out a samplesheet csv.

An example input might look like the following:
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
        "index_2_cycles": 10,
      },
      "bclconvert_settings": {
        "adapter_behavior": "trim",
        "adapter_read_1": null,
        "adapter_read_2": null,
        "adapter_stringency": null,
        "barcode_mismatches_index_1":  1,
        "barcode_mismatches_index_2":  1,
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

Where the output is then written as
[Header]
FileFormatVersion,2
RunName,my-illumina-sequencing-run
RunDescription,A test run
InstrumentPlatform,NovaSeq 6000
InstrumentType,NovaSeq

[Reads]
Read1Cycles,151
Read2Cycles,151
Index1Cycles,10
Index2Cycles,10

[BCLConvert_Settings]
AdapterBehavior,trim
BarcodeMismatchesIndex1,1
BarcodeMismatchesIndex2,1
MinimumAdapterOverlap,2
OverrideCycles,Y151;Y10;Y8N2;Y151
CreateFastqForIndexReads,False
NoLaneSplitting,False
FastqCompressionFormat,gzip

[BCLConvert_Data]
Lane,Sample_ID,index,index2,Sample_Project
1,MyFirstSample,AAAAAAAAAA,CCCCCCCC,SampleProject
1,MySecondSample,GGGGGGGGGG,TTTTTTTT,SampleProject
"""


def get_v2_samplesheet_reader_doc_opt():
    return """
Usage:
v2-samplesheet-to-json <input-csv> <output-json>

Options:

* input-csv:  Path to the input csv you wish to convert to json. Use '-' for stdin.
* output-json: Path to the output-json. Use '-' to write to stdout

Example:
v2-samplesheet-maker SampleSheet.csv /path/to/output.json

Description:
Given a samplesheet, write out the samplesheet in json format.
:return:
"""

