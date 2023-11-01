import os
from io import StringIO
from pathlib import Path
import sys

import pytest
from v2_samplesheet_maker.utils.cli import check_v2_samplesheet_args


@pytest.fixture
def set_stdin(monkeypatch):
    monkeypatch.setattr('sys.stdin', open('examples/inputs/standard-sheet-with-settings.json', 'r'))


@pytest.mark.usefixtures("set_stdin")
class TestCheckV2SampleSheetArgs:
    valid_args = {
        "<input-json>": "examples/inputs/standard-sheet-with-settings.json",
        "<output-csv>": "examples/outputs/standard-sheet-with-settings.csv"
    }

    invalid_valid_args_bad_input = {
        "<input-json>": "examples/inputs/standard-sheet-with-settings.doesnotexist.json",
        "<output-csv>": "examples/outputs/standard-sheet-with-settings.csv"
    }

    invalid_valid_args_bad_output = {
        "<input-json>": "examples/inputs/standard-sheet-with-settings.json",
        "<output-csv>": "examples/doesnotexist_outputs/standard-sheet-with-settings.csv"
    }

    stdin_args = {
        "<input-json>": "-",
        "<output-csv>": "examples/outputs/standard-sheet-with-settings.csv"
    }

    stdout_args = {
        "<input-json>": "examples/inputs/standard-sheet-with-settings.json",
        "<output-csv>": "-"
    }

    def test_check_v2_samplesheet_args_valid_arguments(self):
        args = check_v2_samplesheet_args(self.valid_args)

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
            args = check_v2_samplesheet_args(self.invalid_valid_args_bad_input)
            assert False
        except FileNotFoundError:
            assert True

    def test_invalid_valid_args_bad_output(self):
        try:
            args = check_v2_samplesheet_args(self.invalid_valid_args_bad_output)
            assert False
        except NotADirectoryError:
            assert True

    def test_input_stdin(self, set_stdin):
        args = check_v2_samplesheet_args(self.stdin_args)

    def test_stdout(self):
        args = check_v2_samplesheet_args(self.stdout_args)

        # Assign fileno of sys.stdout to output-csv
        assert isinstance(args.get("output-csv"), int)
