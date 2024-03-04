# V2 SampleSheet Maker


[![Build and Deploy][pipeline_on_tag_badge_svg_url]][pipeline_on_tag_url] [![PyPI version][badge_fury_svg_url]][badge_fury_url]

Generate an Illumina SampleSheet CSV from JSON.

## Supported Sections

Sections currently supported:
  * Header
  * Reads
  * BCLConvert_Settings
  * BCLConvert_Data
  * Cloud_Settings
  * Cloud_Data
  * (Cloud_)?TSO500S_Settings
  * (Cloud_)?TS0500S_Data
  * (Cloud_)?TSO500L_Settings
  * (Cloud_)?TSO500L_Data

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

## Cloud URN Support

We also support URNs for [BSSH auto-launch][analysis_autolaunch_url]

The urn attribute can be placed either in the Cloud_Settings section under the key `<app_name>_Pipeline` or the settings section of the application under the key `urn`. 
In both circumstances, the urn will be placed in the cloud settings section of the samplesheet under `<app_name_Pipeline>`.  

When using the Cloud_Settings and Cloud_Data section, one should place the `library_prep_kit_name` and `index_adapter_kit_name` for 
each element in `bclconvert_data`.  

One will also need to place the following key, value pairs under the `cloud_settings` key:
 * generated_version: "0.0.0",
 * cloud_workflow: "ica_workflow_1"

An example can be seen below:

### Input

<details>

<summary>Click to expand!</summary>

```json
{
  "header": {
    "file_format_version": 2,
    "run_name": "TruSeq-PCRfree-NA12878-10B",
    "instrument_type": "NovaSeqXPlus",
    "index_orientation": "Forward"
  },
  "reads": {
    "read_1_cycles": 151,
    "read_2_cycles": 151,
    "index_1_cycles": 10,
    "index_2_cycles": 10
  },
  "bclconvert_settings": {
    "software_version": "4.1.27",
    "adapter_read_1": "AGATCGGAAGAGCACACGTCTGAACTCCAGTCA",
    "adapter_read_2": "AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT",
    "override_cycles": "Y151;I8N2;N2I8;Y151",
    "fastq_compression_format": "gzip",
    "urn": "urn:ilmn:ica:pipeline:bf93b5cf-cb27-4dfa-846e-acd6eb081aca#BclConvert_v4_2_7"
  },
  "bclconvert_data": [
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep1",
      "index": "CCGCGGTT",
      "index2": "AGCGCTAG",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep1",
      "index": "TTATAACC",
      "index2": "GATATCGA",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep1",
      "index": "GGACTTGG",
      "index2": "CGCAGACG",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep1",
      "index": "AAGTCCAA",
      "index2": "TATGAGTA",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep1",
      "index": "ATCCACTG",
      "index2": "AGGTGCGT",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep1",
      "index": "GCTTGTCA",
      "index2": "GAACATAC",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep1",
      "index": "CAAGCTAG",
      "index2": "ACATAGCG",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep1",
      "index": "TGGATCGA",
      "index2": "GTGCGATA",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep2",
      "index": "AGTTCAGG",
      "index2": "CCAACAGA",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep2",
      "index": "GACCTGAA",
      "index2": "TTGGTGAG",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep2",
      "index": "TCTCTACT",
      "index2": "CGCGGTTC",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep2",
      "index": "CTCTCGTC",
      "index2": "TATAACCT",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep2",
      "index": "CCAAGTCT",
      "index2": "AAGGATGA",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep2",
      "index": "TTGGACTC",
      "index2": "GGAAGCAG",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep2",
      "index": "GGCTTAAG",
      "index2": "TCGTGACC",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep2",
      "index": "AATCCGGA",
      "index2": "CTACAGTT",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep3",
      "index": "TAATACAG",
      "index2": "ATATTCAC",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep3",
      "index": "CGGCGTGA",
      "index2": "GCGCCTGT",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep3",
      "index": "ATGTAAGT",
      "index2": "ACTCTATG",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep3",
      "index": "GCACGGAC",
      "index2": "GTCTCGCA",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep3",
      "index": "GGTACCTT",
      "index2": "AAGACGTC",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep3",
      "index": "AACGTTCC",
      "index2": "GGAGTACT",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep3",
      "index": "GCAGAATT",
      "index2": "ACCGGCCA",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    },
    {
      "lane": 1,
      "sample_id": "TSPF-NA12878-10B-Rep3",
      "index": "ATGAGGCC",
      "index2": "GTTAATTG",
      "library_prep_kit_name": "TruSeqDNAPCRFree",
      "index_adapter_kit_name": "TruSeqDnaUDIndexes96Indexes"
    }
  ],
  "cloud_settings": {
    "generated_version": "0.0.0",
    "cloud_workflow": "ica_workflow_1"
  }
}
```

</details>

Yields

### Output

<details>

<summary>Click to expand!</summary>

```
[Header]
FileFormatVersion,2
RunName,TruSeq-PCRfree-NA12878-10B
InstrumentType,NovaSeqXPlus
IndexOrientation,Forward

[Reads]
Read1Cycles,151
Read2Cycles,151
Index1Cycles,10
Index2Cycles,10

[BCLConvert_Settings]
AdapterRead1,AGATCGGAAGAGCACACGTCTGAACTCCAGTCA
AdapterRead2,AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT
OverrideCycles,Y151;I8N2;N2I8;Y151
FastqCompressionFormat,gzip
SoftwareVersion,4.1.27

[BCLConvert_Data]
Lane,Sample_ID,index,index2
1,TSPF-NA12878-10B-Rep1,CCGCGGTT,AGCGCTAG
1,TSPF-NA12878-10B-Rep1,TTATAACC,GATATCGA
1,TSPF-NA12878-10B-Rep1,GGACTTGG,CGCAGACG
1,TSPF-NA12878-10B-Rep1,AAGTCCAA,TATGAGTA
1,TSPF-NA12878-10B-Rep1,ATCCACTG,AGGTGCGT
1,TSPF-NA12878-10B-Rep1,GCTTGTCA,GAACATAC
1,TSPF-NA12878-10B-Rep1,CAAGCTAG,ACATAGCG
1,TSPF-NA12878-10B-Rep1,TGGATCGA,GTGCGATA
1,TSPF-NA12878-10B-Rep2,AGTTCAGG,CCAACAGA
1,TSPF-NA12878-10B-Rep2,GACCTGAA,TTGGTGAG
1,TSPF-NA12878-10B-Rep2,TCTCTACT,CGCGGTTC
1,TSPF-NA12878-10B-Rep2,CTCTCGTC,TATAACCT
1,TSPF-NA12878-10B-Rep2,CCAAGTCT,AAGGATGA
1,TSPF-NA12878-10B-Rep2,TTGGACTC,GGAAGCAG
1,TSPF-NA12878-10B-Rep2,GGCTTAAG,TCGTGACC
1,TSPF-NA12878-10B-Rep2,AATCCGGA,CTACAGTT
1,TSPF-NA12878-10B-Rep3,TAATACAG,ATATTCAC
1,TSPF-NA12878-10B-Rep3,CGGCGTGA,GCGCCTGT
1,TSPF-NA12878-10B-Rep3,ATGTAAGT,ACTCTATG
1,TSPF-NA12878-10B-Rep3,GCACGGAC,GTCTCGCA
1,TSPF-NA12878-10B-Rep3,GGTACCTT,AAGACGTC
1,TSPF-NA12878-10B-Rep3,AACGTTCC,GGAGTACT
1,TSPF-NA12878-10B-Rep3,GCAGAATT,ACCGGCCA
1,TSPF-NA12878-10B-Rep3,ATGAGGCC,GTTAATTG

[Cloud_Settings]
GeneratedVersion,0.0.0
Cloud_Workflow,ica_workflow_1
BCLConvert_Pipeline,urn:ilmn:ica:pipeline:bf93b5cf-cb27-4dfa-846e-acd6eb081aca#BclConvert_v4_2_7

[Cloud_Data]
Sample_ID,LibraryName,LibraryPrepKitName,IndexAdapterKitName
TSPF-NA12878-10B-Rep1,TSPF-NA12878-10B-Rep1_AAGTCCAA_TATGAGTA,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep1,TSPF-NA12878-10B-Rep1_ATCCACTG_AGGTGCGT,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep1,TSPF-NA12878-10B-Rep1_CAAGCTAG_ACATAGCG,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep1,TSPF-NA12878-10B-Rep1_CCGCGGTT_AGCGCTAG,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep1,TSPF-NA12878-10B-Rep1_GCTTGTCA_GAACATAC,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep1,TSPF-NA12878-10B-Rep1_GGACTTGG_CGCAGACG,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep1,TSPF-NA12878-10B-Rep1_TGGATCGA_GTGCGATA,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep1,TSPF-NA12878-10B-Rep1_TTATAACC_GATATCGA,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep2,TSPF-NA12878-10B-Rep2_AATCCGGA_CTACAGTT,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep2,TSPF-NA12878-10B-Rep2_AGTTCAGG_CCAACAGA,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep2,TSPF-NA12878-10B-Rep2_CCAAGTCT_AAGGATGA,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep2,TSPF-NA12878-10B-Rep2_CTCTCGTC_TATAACCT,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep2,TSPF-NA12878-10B-Rep2_GACCTGAA_TTGGTGAG,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep2,TSPF-NA12878-10B-Rep2_GGCTTAAG_TCGTGACC,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep2,TSPF-NA12878-10B-Rep2_TCTCTACT_CGCGGTTC,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep2,TSPF-NA12878-10B-Rep2_TTGGACTC_GGAAGCAG,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep3,TSPF-NA12878-10B-Rep3_AACGTTCC_GGAGTACT,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep3,TSPF-NA12878-10B-Rep3_ATGAGGCC_GTTAATTG,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep3,TSPF-NA12878-10B-Rep3_ATGTAAGT_ACTCTATG,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep3,TSPF-NA12878-10B-Rep3_CGGCGTGA_GCGCCTGT,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep3,TSPF-NA12878-10B-Rep3_GCACGGAC_GTCTCGCA,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep3,TSPF-NA12878-10B-Rep3_GCAGAATT_ACCGGCCA,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep3,TSPF-NA12878-10B-Rep3_GGTACCTT_AAGACGTC,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
TSPF-NA12878-10B-Rep3,TSPF-NA12878-10B-Rep3_TAATACAG_ATATTCAC,TruSeqDNAPCRFree,TruSeqDnaUDIndexes96Indexes
```

</details>


## Testing your outputs

The v2-samplesheet-maker will validate that your parameters are the correct type, the correct name AND within the appropriate range. 
It will NOT however determine if your settings are appropriate or compatible with a BCLConvert run, i.e it will NOT
ensure that your indexes have an appropriate hamming distance.  

If you wish to validate your output samplesheet with BCLConvert, you can use the following script - 

`scripts/build-samplesheet-and-validate-with-bcl-convert.sh <input-json> [docker-image]`. This will convert the input json to csv and then run the 
docker container bclconvert against your samplesheet.  

You will need both jq and docker installed for this to work.

## Additional Usage

### Parsing a SampleSheet CSV to JSON

We also have created a parser between the csv and json, with the following usage syntax

```
v2-samplesheet-to-json SampleSheet.csv -
```

**Input SampleSheet CSV**

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

Gives us

<details>

<summary>Click to expand!</summary>

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
    "barcode_mismatches_index_1": 1,
    "barcode_mismatches_index_2": 1,
    "minimum_adapter_overlap": 2,
    "override_cycles": "Y151;Y10;Y8N2;Y151",
    "create_fastq_for_index_reads": false,
    "no_lane_splitting": false,
    "fastq_compression_format": "gzip"
  },
  "bclconvert_data": [
    {
      "lane": 1,
      "sample_id": "MyFirstSample",
      "index": "AAAAAAAAAA",
      "index2": "CCCCCCCC",
      "sample_project": "SampleProject"
    },
    {
      "lane": 1,
      "sample_id": "MySecondSample",
      "index": "GGGGGGGGGG",
      "index2": "TTTTTTTT",
      "sample_project": "SampleProject"
    }
  ]
}
```

</details>


### Manipulating a samplesheet by parsing through JSON

For this component, you will need some basic knowledge of the [jq][jq_url] command line tool. 

In this example we are given a standard samplesheet but want to edit the adapters for one of the samples.  

Whilst we could do this with grep, sed or awk, it's a little hacky, instead we can
1. Parse the samplesheet to json to stdout
2. Use jq to update the samplesheet 
3. Write out the updated samplesheet to csv

```bash
# Initialise new index variable
NEW_I7_INDEX="TTTTTTTTTT"
SAMPLE_ID="MySecondSample"

# Convert the SampleSheet to JSON
# Update the index for the sample "MySecondSample" in the bclconvert_data section
# Write out the new samplesheet to csv
v2-samplesheet-to-json SampleSheet.csv - | \
jq --raw-output \
  --arg sample_id "${SAMPLE_ID}" \
  --arg replacement_index "${NEW_I7_INDEX}" \
  '
    .bclconvert_data=( 
      .bclconvert_data |
      map(
        if .sample_id == $sample_id then
          .index = $replacement_index
        else
          .
        end
      )
    )
  ' | \
v2-samplesheet-maker - SampleSheet.updated_index.csv 
```

Gives us the following samplesheet as an output

<details>

```
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
1,MySecondSample,TTTTTTTTTT,TTTTTTTT,SampleProject
```

</details>

If we run a diff on our original and updated samplesheet, we can see that the index for "MySecondSample" has been updated. 

```bash
diff SampleSheet.csv SampleSheet.updated_index.csv
```

Yields

```
27c27
< 1,MySecondSample,GGGGGGGGGG,TTTTTTTT,SampleProject
---
> 1,MySecondSample,TTTTTTTTTT,TTTTTTTT,SampleProject
```


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

[pipeline_on_tag_url]: https://github.com/umccr/v2-samplesheet-maker/actions/workflows/pipeline_on_tag.yml
[pipeline_on_tag_badge_svg_url]: https://github.com/umccr/v2-samplesheet-maker/actions/workflows/pipeline_on_tag.yml/badge.svg
[badge_fury_url]: https://badge.fury.io/py/v2-samplesheet-maker
[badge_fury_svg_url]: https://badge.fury.io/py/v2-samplesheet-maker.svg

[section_models_file]: src/v2_samplesheet_maker/models/sections.py
[samplesheet_models_file]: src/v2_samplesheet_maker/models/samplesheet.py
[section_class_file]: src/v2_samplesheet_maker/section_classes/sheet_sections.py
[samplesheet_class_file]: src/v2_samplesheet_maker/classes/samplesheet.py
[test_sections_file]: tests/v2_samplesheet_maker/classes/test_sections.py
[jq_url]: https://stedolan.github.io/jq/
[analysis_autolaunch_url]: https://help.ica.illumina.com/sequencer-integration/analysis_autolaunch
