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
"""


def get_run_info_xml_reader_doc_opt():
    return """
Usage:
run-info-xml-to-json <input-xml> <output-json>

Options:

* input-xml:  Path to the input xml you wish to convert to json. Use '-' for stdin.
* output-json: Path to the output-json. Use '-' to write to stdout


Description:
Given a RunInfo.xml, write out the run info in json format.
Only the minimal amount of information is extracted from the RunInfo.xml file.  
This includes:

* RunInfo Version
* RunName
* Flowcell
* Instrument
* Date
* Reads

Given an input like:
<?xml version="1.0" encoding="utf-8"?>
<RunInfo Version="5">
	<Run Id="240220_A01052_0183_BH5HLHDSXC" Number="183">
		<Flowcell>H5HLHDSXC</Flowcell>
		<Instrument>A01052</Instrument>
		<Date>2/20/2024 4:21:44 PM</Date>
		<Reads>
			<Read Number="1" NumCycles="151" IsIndexedRead="N"/>
			<Read Number="2" NumCycles="20" IsIndexedRead="Y"/>
			<Read Number="3" NumCycles="8" IsIndexedRead="Y"/>
			<Read Number="4" NumCycles="151" IsIndexedRead="N"/>
		</Reads>
		...
	</Run>
</RunInfo>

The output json will look like the following:
{
  "run_info_version": 5,
  "run_name": "240220_A01052_0183_BH5HLHDSXC",
  "flowcell": "H5HLHDSXC",
  "instrument": "A01052",
  "date": "2019-01-01T00:00:00Z",
  "reads": {
    [
      {
        "read_number": 1,
        "cycles": 151,
        "is_index": false
      },
      {
        "read_number": 2,
        "cycles": 10,
        "is_index": true
      },
      {
          "read_number": 3,
          "cycles": 10,
          "is_index": true
      },
      {
          "read_number": 4,
          "cycles": 151,
          "is_index": false
      }
    ]
}

Example:
run-info-xml-to-json RunInfo.xml /path/to/output.json

"""


def get_run_info_xml_writer_doc_opt():
    return """
Usage:
run-info-json-to-xml <input-json> <output-xml>

Options:

* input-json:  Path to the input json you wish to convert to xml. Use '-' for stdin.
* output-xml: Path to the output-xml. Use '-' to write to stdout

Example:

run-info-json-to-xml /path/to/input.json RunInfo.xml

"""


def get_samplesheet_csv_to_run_info_xml_doc_opt():
    return """
Usage:
samplesheet-csv-to-run-info-xml <input-csv> <output-xml> 
                                (--run-id=<run_id>)
                                [--run-number=<run_number>]
                                [--flowcell=<flowcell>]
                                [--instrument=<instrument>]
                                [--date=<date>]
                                
                                
Options:

* input-csv:    Path to the input csv you wish to convert to xml. Use '-' for stdin.
* output-xml:   Path to the output-xml. Use '-' to write to stdout
* --run-id:     The run id to use in the RunInfo.xml file, 
                note if this is in the format of YYMMDD_<INSTRUMENT_ID>_<RUN_NUMBER>_A|B<FLOWCELL_ID>
                then none of --run-number, --flowcell, --instrument or --date are required
* --flowcell:   The flowcell id to use in the RunInfo.xml file
* --instrument: The instrument id to use in the RunInfo.xml file
* --date:       The date to use in the RunInfo.xml file (YYYYMMDD)

Example:

samplesheet-csv-to-run-info-xml SampleSheet.csv RunInfo.xml --run-id=240220_A01052_0183_BH5HLHDSXC
"""


