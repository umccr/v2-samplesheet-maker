#!/usr/bin/env python3
import json
from copy import deepcopy
from typing import Dict, Any, Optional, List
import pandas as pd
from pydantic import BaseModel
import warnings

# Relative subpackges
from ..utils.logger import get_logger

# Get logger
logger = get_logger()

"""
SampleSheets are actually ini files, not csvs.
Here we define the growing list of samplesheet section formats
"""


class Section:
    """
    Super Class for each section
    """

    _model: Optional[BaseModel] = None
    _is_cloud: Optional[bool] = False
    _class_header: Optional[str] = None

    def __init__(self, *args, **kwargs):

        # Assign both
        kwargs_dict = deepcopy(kwargs)
        for key in self._model.model_fields.keys():
            if hasattr(self, key):
                # Don't set key if it already exists
                # This occurs in the rare case of analysis_urns which are set in the subclass
                # Pop out key so not logged in untouched options
                _ = kwargs.pop(key, None)
                continue
            elif key in kwargs_dict.keys():
                setattr(self, key, kwargs.pop(key))
            else:
                # Set value to None
                setattr(self, key, None)

        # Log any keys that still exist that aren't in the model
        self.log_untouched_options(*args, **kwargs)

    def log_untouched_options(self, *args, **kwargs):
        """
        Show all of the parameters passed that were not used
        :param args:
        :param kwargs:
        :return:
        """
        for arg in list(args):
            logger.warning(f"Postional argument '{arg}' was not used for {self._model}")
            warnings.warn(
                f"Postional argument '{arg}' was not used for {self._model}",
                UserWarning
            )

        for kwarg_key, kwarg_value in dict(**kwargs).items():
            logger.warning(f"Keyword argument '{kwarg_key}={kwarg_value}' was not used for {self._model}")
            warnings.warn(
                f"Keyword argument '{kwarg_key}={kwarg_value}' was not used for {self._model}",
                UserWarning,
            )

    def _build_section(self) -> Any:
        raise NotImplementedError

    def to_string(self) -> str:
        """
        Write out the section to string
        :return:
        """
        raise NotImplementedError

    def to_json(self) -> str:
        """
        Write out the section as a json object
        Implemented in subclass
        :return:
        """
        raise NotImplementedError

    def print_class_header(self) -> str:
        """
        Print out the class header, including [] and "Cloud_" prefix if appropriate
        :return:
        """
        header_str = self._class_header
        if self._is_cloud:
            header_str = "Cloud_" + header_str

        return f"[{header_str}]"

    def print_class_header_json(self) -> str:
        """
        Print out the class header, with "Cloud_" prefix if appropriate
        Do not print out the [] as this is not required for json
        :return:
        """
        header_str = self._class_header.lower()
        if self._is_cloud:
            header_str = "cloud_" + header_str

        return header_str

    def validate_model(self):
        """
        Validate inputs against pydantic model of class
        :return:
        """
        self._model.model_validate(self)

    def write_section(self, file_h, add_new_line_after_section=True):
        """
        Write the section as a string
        :return:
        """
        # Write the class header
        file_h.write(
            self.print_class_header() + "\n"
        )

        # Write out the section as a string
        file_h.write(
            self.to_string() + ("\n" if add_new_line_after_section is True else "")
        )

    def write_section_json(self, file_h):
        """
        Write the section out as a json object
        :param file_h:
        :return:
        """
        file_h.write(self.to_json())


class KVSection(Section):
    """
    Key Value Pair Section
    :return:
    """
    def __init__(self, *args, **kwargs):
        self._raw_kwargs_dict = deepcopy(kwargs)
        # Set section format
        super().__init__(*args, **kwargs)
        self.section_dict = None

        # Validate model after initialising inputs
        self.validate_model()

        # Coerce objects
        self.coerce_values()

        # Build section dict
        self.build_section_dict()

    def _build_section(self):
        return self.build_section_dict()

    def coerce_values(self):
        # Coerce with model dump
        coerced_dict = self._model(**self.get_dict_object()).model_dump()

        for key, value in coerced_dict.items():
            self.__setattr__(key, value)

    def get_dict_object(self):
        return {
            kv[0]: kv[1]
            for kv in filter(
                lambda kv_iter: not kv_iter[0] in ["section_dict", "_raw_kwargs_dict"],
                self.__dict__.items()
            )
        }

    def build_section_dict(self):
        # Collect original objects
        self.section_dict = self._model(**self.get_dict_object()).to_dict()
        self.section_dict = self.filter_dict(self.section_dict)

    def filter_dict(self, initial_dict) -> Dict:
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

    def to_json(self) -> str:
        # Write out each key value pair with a comma between key and value (and a new line between each pair)
        return json.dumps({self.print_class_header_json(): self.filter_dict(self._model(**self.get_dict_object()).to_json())})


class DataFrameSectionRow(KVSection):
    """
    Abstract class for a row of a DataFrame section
    """

    _model: Optional[BaseModel] = None

    def to_series(self):
        return pd.Series(
            dict(
                filter(
                    lambda kv: kv[1] is not None,
                    self.section_dict.items()
                )
            )
        )

    def to_string(self):
        # Cannot use to-string for SectionRow
        raise NotImplementedError

    def to_json(self) -> str:
        # Needed for dataframe object
        return json.dumps(self.filter_dict(self._model(**self.get_dict_object()).to_json()))


class CloudKVSection(KVSection):
    is_cloud = True

    def __init__(self, *args, **kwargs):
        self.urn = kwargs.pop("urn")
        self.pipeline_name = kwargs.pop("pipeline_name")
        super().__init__(*args, **kwargs)


class DataFrameSection(Section):
    """
    DataFrame Section
    A DataFrame section is able to be imported into pandas
    """

    _row_obj: Optional[BaseModel] = None

    def __init__(self, *args, **kwargs):
        """
        Section Dataframe
        :param section_df:
        """
        # Assign args to data_rows
        data_rows = args
        self._raw_args = deepcopy(args)

        # Set section format
        super().__init__()

        # Initialise vars
        self.section_df: Optional[pd.DataFrame] = None
        self.data_rows: Optional[List[DataFrameSectionRow]] = list(
            map(
                lambda data_row_dict_iter: self._row_obj(**data_row_dict_iter),
                data_rows
            )
        )

        # Build section dataframe
        self.build_section_df()

    def _build_section(self):
        return self.build_section_df()

    def build_section_df(self):
        # Convert list of
        self.section_df = pd.DataFrame(
            map(
                lambda data_row: data_row.to_series(),
                self.data_rows
            )
        ).dropna(
            how="all", axis="columns"
        )

        try:
            self.clean_rows()
        except NotImplementedError:
            pass

        self.order_rows()

    def to_string(self):
        # Write out the dataframe as a dataframe section
        # Termination line already has '\n'
        return self.section_df.to_csv(
            sep=",",
            header=True,
            index=False,
            lineterminator="\n"
        )

    def order_rows(self):
        """
        Define which columns should be used to order the rows
        :return:
        """

        if not hasattr(self._model, "row_order_columns"):
            return

        # Get order list of columns in list
        order_list = list(
            filter(
                lambda order_col_iter: order_col_iter in self._model.row_order_columns,
                self.section_df.columns
            )
        )

        if len(order_list) == 0:
            return

        # Order rows by values in order list
        self.section_df = self.section_df.sort_values(by=order_list)

    def clean_rows(self):
        """
        A DataFrame section may have a method to clean up rows (i.e drop duplicates)
        :return:
        """
        raise NotImplementedError

    def validate_model(self):
        """
        Validate inputs against pydantic model of class
        :return:
        """
        # Implemented in subclass
        raise NotImplementedError

    def to_json(self) -> str:
        # Write out the dataframe as a dataframe section
        return json.dumps(
            {
                self.print_class_header_json(): list(
                    map(
                        lambda data_row_iter: json.loads(data_row_iter.to_json()),
                        self.data_rows
                    )
                )
            }
        )


class CloudDataFrameSection(DataFrameSection):
    is_cloud = True

    def __init__(self, *args, **kwargs):
        self.pipeline_name = kwargs.pop("pipeline_name")
        super().__init__(*args, **kwargs)
