#!/usr/bin/env bash

set -euo pipefail

: '
Build an Illumina RunInfo.xml from the reads segment of a samplesheet
'

## FUNCTIONS ##
print_help(){
  echo "
Usage: build-runinfo-xml-from-reads-json.sh <input-json-str> <output-file>

Options:
  <input-json-str>:   Required, the number of cycles per read as a json string
  -h | --help         Optional, print this help page and exit

Description:
Build a DUMMY RunInfo.xml based on the Reads Section of an Illumina V2 SampleSheet.

This is useful for running bcl-convert --validate-samplesheet-only which requires a V2 SampleSheet complemented with a RunInfo.xml.
Please do NOT use the output file as a replacement for the RunInfo.xml in an Illumina Sequencing Run.

This script is also called by build-samplesheet-and-validate-with-bcl-convert.sh which builds a V2 SampleSheet through v2-samplesheet-maker followed by
testing the new SampleSheet through the bcl-convert binary (which needs a RunInfo file).

Requirements:
  * jq    (v1.5+)
  * yq    (v4.18+)

Example:
build-runinfo-xml-from-reads-json.sh '{\"read_1_cycles\":151,\"read_2_cycles\":151,\"index_1_cycles\":10,\"index_2_cycles\":10}' RunInfo.xml
"
}

echo_stderr(){
  : '
  Write output to stderr
  '
  echo "${@}" 1>&2
}

mock_read_xml_section(){
  : '
  Return a section like
  from input

  {
     "+@Number": "1",
     "+@NumCycles": "151",
     "+@IsIndexedRead": "N"
  }
  '
  local lane_number="${1}"
  local num_cycles="${2}"
  local is_indexed_read="${3}"

  jq \
    --null-input --raw-output \
    --argjson lane_number "${lane_number}" \
    --argjson num_cycles "${num_cycles}" \
    --arg is_indexed_read "${is_indexed_read}" \
    '
      {
        "+@Number": "\($lane_number)",
        "+@NumCycles": "\($num_cycles)",
        "+@IsIndexedRead": $is_indexed_read
      }
    '
}

mock_tile_section(){
  : '
  Returns something line
  [
    "1_1000",
    "2_1000",
    "3_1000",
    "4_1000"
  ]
  '
  local lane_count="${1}"

  seq 1 "${lane_count}" | \
  jq --raw-output --slurp \
    '
      map(
        "\(.)_1000"
      )
    '
}

## Check requirements
if ! type yq 1>/dev/null 2>&1; then
  echo_stderr "Please install yq"
  print_help | echo_stderr
  exit 1
fi

## Get inputs
input_json_str=""
run_info_xml_output_file=""
positional_args_array=()

while [ $# -gt 0 ]; do
  case "$1" in
    -h | --help)
      print_help
      exit 0
      ;;
    --*)
      echo_stderr "No key word arguments excepted"
      print_help
      exit 1
      ;;
    *)
      positional_args_array+=( "${1-}" )
      ;;
  esac
  shift 1
done

# Get positional args
input_json_str="${positional_args_array[0]}"
run_info_xml_output_file="${positional_args_array[1]-}"

## Check inputs
if [[ -z "${input_json_str}" ]]; then
  echo_stderr "Input Json String was not specified"
elif ! jq <<< "${input_json_str}" 1>/dev/null 2>&1; then
  echo_stderr "input json parameter '${input_json_str}' is not valid json"
  exit 1
fi

if [[ -z "${run_info_xml_output_file}" ]]; then
  echo_stderr "Please specify output path"
  exit 1
elif [[ ! -d "$(dirname "${run_info_xml_output_file}")" ]]; then
  echo_stderr "Parent directory of ${run_info_xml_output_file} does not exist"
  exit 1
elif [[ -r "${run_info_xml_output_file}" ]]; then
  echo_stderr "${run_info_xml_output_file} file already exists. Please delete and try again or specify another path"
  exit 1
fi

## Mock Up RunInfo.xml
echo_stderr "Generating RunInfo.xml file"
key_value_pair_json_str="$(
  jq --raw-output --compact-output \
    '
      . | to_entries |
      # Add is_index attribute and order by expectations of runinfo xml
      map (
        . +
        {
          "is_index": (
            if .key | startswith("read") then
              "N"
            else
              "Y"
            end
          ),
          "ordering": (
            if .key == "read_1_cycles" then
              1
            elif .key == "index_1_cycles" then
              2
            elif .key == "index_2_cycles" then
              3
            elif .key == "read_2_cycles" then
              4
            else
              empty
            end
          )
        }
      ) |
      # Sort by ordering key
      sort_by(.ordering) |
      # Now delete ordering key
      map(
        del(.ordering)
      ) |
      # Unlist
      .[]
    ' <<< "${input_json_str}"
)"

# Math
(( lane_iter=1 ))

reads_json_str="$( \
  for key_value_pair in ${key_value_pair_json_str}; do
    mock_read_xml_section \
      "${lane_iter}" \
      "$(jq -r '.value' <<< "${key_value_pair}")" \
      "$(jq -r '.is_index' <<< "${key_value_pair}")"

    # Increment lane
    (( lane_iter+=1 ))
  done | \
  jq --slurp --raw-output --compact-output \
)"

num_lanes="$( \
  jq --raw-output \
    '.reads | length' \
    <<< "${input_json_str}"
)"

mock_tiles_json_str="$( \
  mock_tile_section "${num_lanes}"
)"

# Write out run info xml
jq --raw-output --null-input \
  --argjson mock_reads_list "${reads_json_str}" \
  --argjson mock_tiles_list "${mock_tiles_json_str}" \
  '
    {
      "+p_xml": "version=\"1.0\" encoding=\"utf-8\"",
      "RunInfo": {
        "+@Version": "5",
        "Run": {
          "+@Id": "MAGICAL_ID",
          "+@Number": "123",
          "Flowcell": "ABCD",
          "Instrument": "A456",
          "Date": "01-Jan-70 00:00:00 AM",
          "Reads": {
            "Read": $mock_reads_list
          },
          "FlowcellLayout": {
            "+@LaneCount": "4",
            "+@SurfaceCount": "2",
            "+@SwathCount": "6",
            "+@TileCount": "78",
            "+@FlowcellSide": "1",
            "TileSet": {
              "+@TileNamingConvention": "FourDigit",
              "Tiles": {
                "Tile": $mock_tiles_list
              }
            }
          },
          "AlignToPhiX": null,
          "ImageDimensions": {
            "+@Width": "9999",
            "+@Height": "9999"
          },
          "ImageChannels": {
            "Name": [
              "RED",
              "GREEN"
            ]
          }
        }
      }
    }
  ' | \
yq \
  --input-format=json --output-format=xml \
  > "${run_info_xml_output_file}"
echo_stderr "Completed generation of RunInfo.xml file to '${run_info_xml_output_file}'"