import os
from io import StringIO
from pathlib import Path
import sys

import pytest
from v2_samplesheet_maker.utils.cli import (
    check_v2_samplesheet_writer_args,
    check_v2_samplesheet_reader_args
)


@pytest.fixture
def set_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', open('examples/json_inputs/standard-sheet-with-settings.json', 'r'))


@pytest.mark.usefixtures("set_stdin")
class TestCheckV2SampleSheetArgs:
    valid_args = {
        "<input-json>": "examples/json_inputs/standard-sheet-with-settings.json",
        "<output-csv>": "examples/csv_outputs/standard-sheet-with-settings.csv"
    }

    invalid_valid_args_bad_input = {
        "<input-json>": "examples/json_inputs/standard-sheet-with-settings.doesnotexist.json",
        "<output-csv>": "examples/csv_outputs/standard-sheet-with-settings.csv"
    }

    invalid_valid_args_bad_output = {
        "<input-json>": "examples/json_inputs/standard-sheet-with-settings.json",
        "<output-csv>": "examples/doesnotexist_outputs/standard-sheet-with-settings.csv"
    }

    stdin_args = {
        "<input-json>": "-",
        "<output-csv>": "examples/csv_outputs/standard-sheet-with-settings.csv"
    }

    stdout_args = {
        "<input-json>": "examples/json_inputs/standard-sheet-with-settings.json",
        "<output-csv>": "-"
    }

    def test_check_v2_samplesheet_args_valid_arguments(self):
        args = check_v2_samplesheet_writer_args(self.valid_args)

        # Check input json is valid
        assert args.get("input-json", None) is not None

        # Check input json has expected fields
        input_json = args.get("input-json")
        assert input_json.get("header", None) is not None
        assert input_json.get("reads", None) is not None
        assert input_json.get("bclconvert_settings", None) is not None
        assert input_json.get("bclconvert_data", None) is not None

        # Assert output is not None
        assert args.get("output-csv", None) is not None

        # Assert output parent path exists
        assert Path(args.get("output-csv")).parent.is_dir()

    def test_check_v2_samplesheet_args_invalid_input(self):
        try:
            args = check_v2_samplesheet_writer_args(self.invalid_valid_args_bad_input)
            assert False
        except FileNotFoundError:
            assert True

    def test_invalid_valid_args_bad_output(self):
        try:
            args = check_v2_samplesheet_writer_args(self.invalid_valid_args_bad_output)
            assert False
        except NotADirectoryError:
            assert True

    def test_input_stdin(self, set_stdin):
        args = check_v2_samplesheet_writer_args(self.stdin_args)

    def test_stdout(self):
        args = check_v2_samplesheet_writer_args(self.stdout_args)

        # Assign fileno of sys.stdout to output-csv
        assert isinstance(args.get("output-csv"), int)


@pytest.mark.usefixtures("set_stdin")
class TestCheckV2SampleSheetToJSONArgs:
    valid_args = {
        "<input-csv>": "examples/csv_outputs/standard-sheet-with-settings.csv",
        "<output-json>": "examples/csv_to_json_outputs/standard-sheet-with-settings.json"
    }

    # FIMXE - not used yet
    valid_args_excel_input = {
        "<input-csv>": "examples/inputs/samplesheet_from_excel.csv",
        "<output-json>": "examples/csv_to_json_outputs/samplesheet_from_excel.json"
    }

    invalid_valid_args_bad_input = {
        "<input-csv>": "examples/csv_outputs/standard-sheet-with-settings.doesnotexist.csv",
        "<output-json>": "examples/json_inputs/standard-sheet-with-settings.json",
    }

    invalid_valid_args_bad_output = {
        "<input-csv>": "examples/csv_outputs/standard-sheet-with-settings.csv",
        "<output-json>": "examples/doesnotexist_csv_to_json_outputs/standard-sheet-with-settings.json"
    }

    stdin_args = {
        "<input-csv>": "-",
        "<output-json>": "examples/csv_to_json_outputs/standard-sheet-with-settings.json"
    }

    stdout_args = {
        "<input-csv>": "examples/csv_outputs/standard-sheet-with-settings.csv",
        "<output-json>": "-"
    }

    def test_check_v2_samplesheet_args_valid_arguments(self):
        args = check_v2_samplesheet_reader_args(self.valid_args)

        # Check input csv is valid
        assert args.get("input-csv", None) is not None

        # Input csv is a file
        assert Path(args.get("input-csv")).is_file()

        # Assert output is not None
        assert args.get("output-json", None) is not None

        # Assert output parent path exists
        assert Path(args.get("output-json")).parent.is_dir()

    def test_check_v2_samplesheet_args_invalid_input(self):
        try:
            args = check_v2_samplesheet_reader_args(self.invalid_valid_args_bad_input)
            assert False
        except FileNotFoundError:
            assert True

    def test_invalid_valid_args_bad_output(self):
        try:
            args = check_v2_samplesheet_reader_args(self.invalid_valid_args_bad_output)
            assert False
        except NotADirectoryError:
            assert True

    def test_input_stdin(self, set_stdin):
        args = check_v2_samplesheet_reader_args(self.stdin_args)

    def test_stdout(self):
        args = check_v2_samplesheet_reader_args(self.stdout_args)

        # Assign fileno of sys.stdout to output-json
        assert isinstance(args.get("output-json"), int)
