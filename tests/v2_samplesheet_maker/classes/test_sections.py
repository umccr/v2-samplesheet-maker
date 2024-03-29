#!/usr/bin/env python
import logging
from copy import deepcopy

import pytest
from pydantic import ValidationError

from v2_samplesheet_maker.section_classes.run_info_sections import (
    HeaderSection,
    ReadsSection
)

from v2_samplesheet_maker.section_classes.bcl_convert_sections import (
    BCLConvertSettingsSection,
    BCLConvertDataRow,
    BCLConvertDataSection,
)


class TestHeaderSection:
    valid_header_section_dict = {
        "file_format_version": 2,
        "run_name": "my-illumina-sequencing-run",
        "run_description": "A test run",
        "instrument_platform": "NovaSeq 6000",
        "instrument_type": "NovaSeq"
    }

    valid_header_section_dict_extra_params = deepcopy(valid_header_section_dict)
    valid_header_section_dict_extra_params.update(
        {
            "additional_field_key": "additional_field_value"
        }
    )

    invalid_header_section_dict = deepcopy(valid_header_section_dict)
    invalid_header_section_dict.update(
        {
            "file_format_version": "1b"
        }
    )

    def test_header_section(self):
        HeaderSection(**self.valid_header_section_dict)

    def test_header_section_with_extra_params(self):
        with pytest.warns(UserWarning):
            HeaderSection(**self.valid_header_section_dict_extra_params)

    def test_invalid_header_section_dict(self):
        try:
            HeaderSection(**self.invalid_header_section_dict)
            assert False
        except (TypeError, ValidationError):
            assert True


class TestReadsSection:
    valid_reads_section_dict = {
        "read_1_cycles": 151,
        "read_2_cycles": 151,
        "index_1_cycles": 10,
        "index_2_cycles": 10
    }

    valid_reads_section_dict_extra_params = deepcopy(valid_reads_section_dict)
    valid_reads_section_dict_extra_params.update(
        {
            "additional_field_key": "additional_field_value"
        }
    )

    invalid_reads_section_dict = deepcopy(valid_reads_section_dict)
    invalid_reads_section_dict.update(
        {
            "read_1_cycles": "151b"
        }
    )

    def test_reads_section(self):
        ReadsSection(**self.valid_reads_section_dict)

    def test_reads_section_with_extra_params(self):
        with pytest.warns(UserWarning):
            ReadsSection(**self.valid_reads_section_dict_extra_params)

    def test_invalid_reads_section_dict(self):
        try:
            ReadsSection(**self.invalid_reads_section_dict)
            assert False
        except (TypeError, ValidationError):
            assert True


class TestBCLConvertSettingsSection:
    valid_bclconvert_settings_section_dict = {
        "adapter_behavior": "trim",
        "adapter_read_1": None,
        "adapter_read_2": None,
        "adapter_stringency": None,
        "barcode_mismatches_index_1": 1,
        "barcode_mismatches_index_2": 1,
        "minimum_trimmed_read_length": None,
        "minimum_adapter_overlap": 2,
        "mask_short_reads": None,
        "override_cycles": "Y151;Y10;Y8N2;Y151",
        "trim_umi": None,
        "create_fastq_for_index_reads": False,
        "no_lane_splitting": False,
        "fastq_compression_format": "gzip",
        "find_adapters_with_indels": None,
        "independent_index_collision_check": None
      }

    valid_bclconvert_settings_section_dict_extra_params = deepcopy(valid_bclconvert_settings_section_dict)
    valid_bclconvert_settings_section_dict_extra_params.update(
        {
            "additional_field_key": "additional_field_value"
        }
    )

    invalid_bclconvert_settings_section_dict = deepcopy(valid_bclconvert_settings_section_dict)
    invalid_bclconvert_settings_section_dict.update(
        {
            "adapter_behavior": "tram"
        }
    )

    def test_bclconvert_settings_section(self):
        BCLConvertSettingsSection(**self.valid_bclconvert_settings_section_dict)

    def test_bclconvert_settings_section_with_extra_params(self):
        with pytest.warns(UserWarning):
            BCLConvertSettingsSection(**self.valid_bclconvert_settings_section_dict_extra_params)

    def test_invalid_bclconvert_settings_section_dict(self):
        try:
            BCLConvertSettingsSection(**self.invalid_bclconvert_settings_section_dict)
            assert False
        except (TypeError, ValidationError):
            assert True


class TestBCLConvertDataRow:
    valid_bclconvert_data_row = {
      "sample_id": "MyFirstSample",
      "lane": 1,
      "index": "AAAAAAAAAA",
      "index2": "CCCCCCCC",
      "sample_project": "SampleProject",
      "sample_name": None,
      # DataRows are generated by Data and so these are made to none on generation
      "override_cycles": None,
      "barcode_mismatches_index_1": None,
      "barcode_mismatches_index_2": None,
      "adapter_read_1": None,
      "adapter_read_2": None,
      "adapter_behavior": None,
      "adapter_stringency": None
    }

    bclconvert_data_row_with_extra_params = deepcopy(valid_bclconvert_data_row)
    bclconvert_data_row_with_extra_params.update(
        {
            "foo": "bar"
        }
    )

    valid_bclconvert_data_row_with_settings = deepcopy(valid_bclconvert_data_row)
    valid_bclconvert_data_row_with_settings.update(
        {
            "override_cycles": "Y151;Y10;Y8N2;Y151",
            "barcode_mismatches_index_1": 1,
            "barcode_mismatches_index_2": 2,
            "adapter_read_1": "AAAA",
            "adapter_read_2": "CCCC",
            "adapter_behavior": "trim",
            "adapter_stringency": 2
        }
    )

    invalid_bclconvert_data_row = deepcopy(valid_bclconvert_data_row)
    invalid_bclconvert_data_row.update(
        {
            "lane": "one"
        }
    )

    def test_bclconvert_data_row(self):
        BCLConvertDataRow(**self.valid_bclconvert_data_row)

    def test_bclconvert_data_row_with_extra_params(self):
        with pytest.warns(UserWarning):
            BCLConvertDataRow(**self.bclconvert_data_row_with_extra_params)

    def test_bclconvert_data_row_with_settings(self):
        BCLConvertDataRow(**self.valid_bclconvert_data_row_with_settings)

    def test_invalid_bclconvert_data_row_dict(self):
        try:
            BCLConvertDataRow(**self.invalid_bclconvert_data_row)
            assert False
        except (TypeError, ValidationError):
            assert True


class TestBCLConvertDataSection:
    # Check valid bclconvert data
    valid_bclconvert_data = [
        {
          "sample_id": "MyFirstSample",
          "lane": 1,
          "index": "AAAAAAAAAA",
          "index2": "CCCCCCCC",
          "sample_project": "SampleProject",
          "sample_name": None
        },
        {
          "sample_id": "MySecondSample",
          "lane": 1,
          "index": "GGGGGGGGGG",
          "index2": "TTTTTTTT",
          "sample_project": "SampleProject",
          "sample_name": None
        }
    ]

    valid_bclconvert_data_with_settings = deepcopy(valid_bclconvert_data)

    for index, bclconvert_row_dict in enumerate(valid_bclconvert_data_with_settings):
        new_bclconvert_row_dict = deepcopy(bclconvert_row_dict)
        new_bclconvert_row_dict.update(
            {
                "override_cycles": "Y151;Y10;Y8N2;Y151",
            }
        )
        valid_bclconvert_data_with_settings[index] = new_bclconvert_row_dict

    invalid_bclconvert_data_with_settings = deepcopy(valid_bclconvert_data)

    for index, bclconvert_row_dict in enumerate(valid_bclconvert_data_with_settings):
        new_bclconvert_row_dict = deepcopy(bclconvert_row_dict)
        new_bclconvert_row_dict.update(
            {
                "foo": "bar",
            }
        )
        invalid_bclconvert_data_with_settings[index] = new_bclconvert_row_dict

    def test_bclconvert_data_section(self):
        # Get valid standard data
        BCLConvertDataSection(*self.valid_bclconvert_data)

    def test_bclconvert_data_section_with_settings(self):
        # Get valid data with settings input
        BCLConvertDataSection(*self.valid_bclconvert_data_with_settings)

    def test_bclconvert_data_with_invalid_rows(self):
        # Get data with invalid settings
        with pytest.warns(UserWarning):
            BCLConvertDataSection(*self.invalid_bclconvert_data_with_settings)
