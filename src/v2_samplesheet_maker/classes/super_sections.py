#!/usr/bin/env python3

from typing import Dict, Any, Optional
import pandas as pd

# Relative subpackges
from ..utils.logger import get_logger

logger = get_logger()

"""
SampleSheets are actually ini files, not csvs.
Here we define the growing list of samplesheet section formats
"""


class Section:
    """
    Super Class for each section
    """
    def __init__(self, *args, **kwargs):
        self.log_untouched_options(*args, **kwargs)

    def _build_section(self) -> Any:
        raise NotImplementedError

    def to_string(self) -> str:
        """
        Write out the section to string
        :return:
        """
        raise NotImplementedError

    def log_untouched_options(self, *args, **kwargs):
        """
        Show all of the parameters passed that were not used
        :param args:
        :param kwargs:
        :return:
        """
        for arg in list(*args):
            logger.warning(f"Postional argument '{arg}' was not used")

        for kwarg_key, kwarg_value in dict(**kwargs).items():
            logger.warning(f"Keyword argument '{kwarg_key}={kwarg_value}' was not used")

    def validate_model(self):
        """
        Validate inputs against pydantic model of class
        :return:
        """
        raise NotImplementedError


class KVSection(Section):
    """
    Key Value Pair Section
    :return:
    """
    def __init__(self, *args, **kwargs):
        # Set section format
        super().__init__(*args, **kwargs)
        self.section_dict = None

    def _build_section(self) -> Dict:
        return self.build_section_dict()

    def build_section_dict(self) -> Dict:
        raise NotImplementedError

    @staticmethod
    def filter_dict(initial_dict) -> Dict:
        """
        Filter out any values that are None
        :param initial_dict:
        :return:
        """
        return dict(
            filter(
                lambda kv: kv[1] is not None,
                initial_dict.items()
            )
        )

    def to_string(self):
        # Write out each key value pair with a comma between key and value (and a new line between each pair)
        return "\n".join(
            list(
                map(
                    lambda kv: f"{str(kv[0])},{str(kv[1])}",
                    self.section_dict.items()
                )
            )
        ) + "\n"

    def validate_model(self):
        """
        Validate inputs against pydantic model of class
        :return:
        """
        # Implemented in subclass
        raise NotImplementedError


class DataFrameSection(Section):
    """
    DataFrame Section
    A DataFrame section is able to be imported into pandas
    """
    def __init__(self, *args, **kwargs):
        """
        Section Dataframe
        :param section_df:
        """
        # Set section format
        super().__init__(*args, **kwargs)
        self.section_df: Optional[pd.DataFrame] = None

    def _build_section(self) -> pd.DataFrame:
        return self.build_section_df()

    def build_section_df(self) -> pd.DataFrame:
        raise NotImplementedError

    def to_string(self):
        # Write out the dataframe as a dataframe section
        # Termination line already has '\n'
        return self.section_df.to_csv(
            sep=",",
            header=True,
            index=False,
            lineterminator="\n"
        )

    def validate_model(self):
        """
        Validate inputs against pydantic model of class
        :return:
        """
        # Implemented in subclass
        raise NotImplementedError
