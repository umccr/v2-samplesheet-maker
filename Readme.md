# V2 SampleSheet Maker


[![Build and Deploy][pipeline_on_tag_badge_svg_url]][pipeline_on_tag_url] [![PyPI version][badge_fury_svg_url]][badge_fury_url]

Generate an Illumina SampleSheet CSV from JSON.

## Supported Sections

Sections currently supported:
  * Header
  * Reads
  * BCLConvert_Settings
  * BCLConvert_Data

## Installation

Installation from pypi

```
pip install v2-samplesheet-maker
```

Alternatively one may use the docker container `ghcr.io/umccr/v2-samplesheet-maker:latest`

## Usage

```
Usage:
v2-samplesheet-maker <input-json> <output-csv>
```

Use `-` for `input-json` parameter to parse json from stdin,  
Use `-` for `output-json` parameter to parse output samplesheet csv to stdout.  

## Examples

See [examples/](examples) for more info 

## Input JSON

<details>

<summary>Click to expand! </summary>

```json
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

```

</details>


## Output CSV

<details>

<summary>Click to expand! </summary>

```ini
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
```

</details>

## Testing your outputs

The v2-samplesheet-maker will validate that your parameters are the correct type, the correct name AND within the appropriate range. 
It will NOT however determine if your settings are appropriate or compatible with a BCLConvert run, i.e it will NOT
ensure that your indexes have an appropriate hamming distance.  

If you wish to validate your output samplesheet with BCLConvert, you can use the following script - 

`scripts/test_bclconvert.sh <input-json> [docker-image]`. This will convert the input json to csv and then run the 
docker container bclconvert against your samplesheet.  

You will need both jq and docker installed for this to work.

## Contributing

Is there a missing section you'd like to see?

You can generate your own sections by 
1. Forking this repository.
2. Adding the section pydantic model to the [section models module][section_models_file]
3. Extending the SampleSheel pydantic model in the [samplesheet models module][samplesheet_models_file]
4. Generating a class for your section in the [section class module][section_class_file]
5. Extending the SampleSheet class to write out your section in the [samplesheet class module][samplesheet_class_file]
6. Add a test for your section in the [test_sections module][test_sections_file]
7. Generating a PR back to this repository! ( Please squash your commits :) )

## Release Cycles

We try and update this repository for every new Dragen Release (which coincides with a BCLConvert release) and tag accordingly.  

[pipeline_on_tag_url]: https://github.com/umccr/v2-samplesheet-maker/workflows/pipeline_on_tag.yml
[pipeline_on_tag_badge_svg_url]: https://github.com/umccr/v2-samplesheet-maker/workflows/pipeline_on_tag.yml/badge.svg
[badge_fury_url]: https://badge.fury.io/py/v2-samplesheet-maker
[badge_fury_svg_url]: https://badge.fury.io/py/v2-samplesheet-maker.svg

[section_models_file]: src/v2_samplesheet_maker/models/sections.py
[samplesheet_models_file]: src/v2_samplesheet_maker/models/samplesheet.py
[section_class_file]: src/v2_samplesheet_maker/classes/sections.py
[samplesheet_class_file]: src/v2_samplesheet_maker/classes/samplesheet.py
[test_sections_file]: tests/v2_samplesheet_maker/classes/test_sections.py