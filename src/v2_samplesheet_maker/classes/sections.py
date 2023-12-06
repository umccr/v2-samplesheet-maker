#!/usr/bin/env python3

"""
Define each of the available sections
"""
from typing import Optional, Dict, List
import pandas as pd

# Relative modules
from .super_sections import KVSection, DataFrameSection

# Relative subpackages
from ..enums import AdapterBehaviour, FastqCompressionFormat
from ..models.sections import HeaderSectionModel, ReadsSectionModel, BCLConvertDataRowModel, \
    BCLConvertSettingsSectionModel, BCLConvertDataSectionModel
from ..utils.logger import get_logger

logger = get_logger()


class HeaderSection(KVSection):
    """
    The header section contains much of the experiment management configurations
    https://support-docs.illumina.com/SHARE/SampleSheetv2/Content/SHARE/SampleSheetv2/SectionsRunSetup.htm
    """
    def __init__(
        self,
        file_format_version: int,
        run_name: Optional[str] = None,
        run_description: Optional[str] = None,
        instrument_platform: Optional[str] = None,
        instrument_type: Optional[str] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.file_format_version = file_format_version
        self.run_name = run_name
        self.run_description = run_description
        self.instrument_platform = instrument_platform
        self.instrument_type = instrument_type

        # Validate model after initialising inputs
        self.validate_model()

        # Build section dict
        self.build_section_dict()

    def build_section_dict(self):
        """
        Build the section dictionary
        :return:
        """
        initial_dict = {
            "FileFormatVersion": self.file_format_version,
            "RunName": self.run_name,
            "RunDescription": self.run_description,
            "InstrumentPlatform": self.instrument_platform,
            "InstrumentType": self.instrument_type
        }

        self.section_dict = self.filter_dict(initial_dict)

    def validate_model(self):
        HeaderSectionModel.model_validate(self)


class ReadsSection(KVSection):
    """
    The reads section contains the cycle information
    https://support-docs.illumina.com/SHARE/SampleSheetv2/Content/SHARE/SampleSheetv2/SectionsRunSetup.htm
    """
    def __init__(
            self,
            read_1_cycles: int,
            read_2_cycles: Optional[int] = None,
            index_1_cycles: Optional[int] = None,
            index_2_cycles: Optional[int] = None,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)

        # Initialise objects
        self.read_1_cycles = read_1_cycles
        self.read_2_cycles = read_2_cycles
        self.index_1_cycles = index_1_cycles
        self.index_2_cycles = index_2_cycles

        # Validate model after initialising inputs
        self.validate_model()

        # Build section dict
        self.build_section_dict()

    def build_section_dict(self):
        """
        Build the section dictionary
        :return:
        """
        initial_dict = {
            "Read1Cycles": self.read_1_cycles,
            "Read2Cycles": self.read_2_cycles,
            "Index1Cycles": self.index_1_cycles,
            "Index2Cycles": self.index_2_cycles,
        }

        self.section_dict = self.filter_dict(initial_dict)

    def validate_model(self):
        ReadsSectionModel.model_validate(self)


class BCLConvertSettingsSection(KVSection):
    """
    BCLConvert Settings Section
    https://support-docs.illumina.com/SW/dragen_v42/Content/SW/DRAGEN/SampleSheet.htm
    """
    def __init__(
        self,
        adapter_behavior: Optional[AdapterBehaviour] = None,  # One of 'trim' / 'mask'
        adapter_read_1: Optional[str] = None,
        adapter_read_2: Optional[str] = None,
        adapter_stringency: Optional[float] = None,  # Float between 0.5 and 1.0
        barcode_mismatches_index_1: Optional[int] = None,  # 0, 1 or 2
        barcode_mismatches_index_2: Optional[int] = None,  # 0, 1 or 2
        minimum_trimmed_read_length: Optional[int] = None,
        minimum_adapter_overlap: Optional[int] = None,  # 1, 2, or 3
        mask_short_reads: Optional[int] = None,
        override_cycles: Optional[str] = None,  # Y151;N8;N10;Y151
        trim_umi: Optional[bool] = None,  # true or false (1, 0)
        create_fastq_for_index_reads: Optional[bool] = None,  # true or false (1, 0)
        no_lane_splitting: Optional[bool] = None,
        fastq_compression_format: Optional[FastqCompressionFormat] = None,
        find_adapters_with_indels: Optional[bool] = None,
        independent_index_collision_check: Optional[List] = None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.adapter_behavior = adapter_behavior
        self.adapter_read_1 = adapter_read_1
        self.adapter_read_2 = adapter_read_2
        self.adapter_stringency = adapter_stringency
        self.barcode_mismatches_index_1 = barcode_mismatches_index_1
        self.barcode_mismatches_index_2 = barcode_mismatches_index_2
        self.minimum_trimmed_read_length = minimum_trimmed_read_length
        self.minimum_adapter_overlap = minimum_adapter_overlap
        self.mask_short_reads = mask_short_reads
        self.override_cycles = override_cycles
        self.trim_umi = trim_umi
        self.create_fastq_for_index_reads = create_fastq_for_index_reads
        self.no_lane_splitting = no_lane_splitting
        self.fastq_compression_format = fastq_compression_format
        self.find_adapters_with_indels = find_adapters_with_indels
        self.independent_index_collision_check = independent_index_collision_check

        # Validate model after initialising inputs
        self.validate_model()

        # Build section dict
        self.build_section_dict()

    def build_section_dict(self):
        """
        Build the section dictionary
        :return:
        """
        initial_dict = {
            "AdapterBehavior": self.adapter_behavior,
            "AdapterRead1": self.adapter_read_1,
            "AdapterRead2": self.adapter_read_2,
            "AdapterStringency": self.adapter_stringency,
            "BarcodeMismatchesIndex1": self.barcode_mismatches_index_1,
            "BarcodeMismatchesIndex2": self.barcode_mismatches_index_2,
            "MinimumTrimmedReadLength": self.minimum_trimmed_read_length,
            "MinimumAdapterOverlap": self.minimum_adapter_overlap,
            "MaskShortReads": self.mask_short_reads,
            "OverrideCycles": self.override_cycles,
            "TrimUMI": self.trim_umi,
            "CreateFastqForIndexReads": self.create_fastq_for_index_reads,
            "NoLaneSplitting": self.no_lane_splitting,
            "FastqCompressionFormat": self.fastq_compression_format,
            "FindAdaptersWithIndels": self.find_adapters_with_indels,
            "IndependentIndexCollisionCheck": self.independent_index_collision_check
        }

        self.section_dict = self.filter_dict(initial_dict)

    def validate_model(self):
        BCLConvertSettingsSectionModel.model_validate(self)


class BCLConvertDataRow:
    """
    A BCLConvert DataRow
    """
    def __init__(
        self,
        sample_id: str,
        lane: Optional[int],
        index: Optional[str],
        index2: Optional[str],
        sample_project: Optional[str],
        sample_name: Optional[str],
        # Per Sample Settings
        override_cycles: Optional[str],
        barcode_mismatches_index1: Optional[int],
        barcode_mismatches_index2: Optional[int],
        adapter_read_1: Optional[str],
        adapter_read_2: Optional[str],
        adapter_behavior: Optional[AdapterBehaviour],
        adapter_stringency: Optional[float]

    ):
        # Sample options
        self.sample_id = sample_id
        self.lane = lane
        self.index = index
        self.index2 = index2
        self.sample_project = sample_project
        self.sample_name = sample_name

        # Sample settings
        self.override_cycles = override_cycles
        self.barcode_mismatches_index1 = barcode_mismatches_index1
        self.barcode_mismatches_index2 = barcode_mismatches_index2
        self.adapter_read_1 = adapter_read_1
        self.adapter_read_2 = adapter_read_2
        self.adapter_behavior = adapter_behavior
        self.adapter_stringency = adapter_stringency

        # Validate model after initialising inputs
        self.validate_model()

    def to_series(self):
        return pd.Series(
            dict(
                filter(
                    lambda kv: kv[1] is not None,
                    {
                        # Sample Options
                        "Lane": self.lane,
                        "Sample_ID": self.sample_id,
                        "index": self.index,
                        "index2": self.index2,
                        "Sample_Project": self.sample_project,
                        "Sample_Name": self.sample_name,
                        # Per sample settings
                        "OverrideCycles": self.override_cycles,
                        "BarcodeMismatchesIndex1": self.barcode_mismatches_index1,
                        "BarcodeMismatchesIndex2": self.barcode_mismatches_index2,
                        "AdapterRead1": self.adapter_read_1,
                        "AdapterRead2": self.adapter_read_2,
                        "AdapterBehavior": self.adapter_behavior,
                        "AdapterStringency": self.adapter_stringency
                    }.items()
                )
            )
        )

    def validate_model(self):
        BCLConvertDataRowModel.model_validate(self)


class BCLConvertDataSection(DataFrameSection):
    """
    For the BCLConvert Data
    """

    def __init__(self, bclconvert_datarows: List[BCLConvertDataRow]):

        super().__init__()

        self.bclconvert_datarows = bclconvert_datarows

        # Build section dict
        self.build_section_df()

    def build_section_df(self):
        # Convert list of
        self.section_df = pd.DataFrame(
            map(
                lambda bclconvert_datarow: bclconvert_datarow.to_series(),
                self.bclconvert_datarows
            )
        ).dropna(how="all", axis="columns")

    @classmethod
    def get_bclconvert_datarows_from_list(cls, bclconvert_data_row_list: List[Dict]):
        bclconvert_data_row_obj_list: List[BCLConvertDataRow] = []
        data_row: Dict
        for data_row in bclconvert_data_row_list:
            sample_id = data_row.pop("sample_id", None)
            lane = data_row.pop("lane", None)
            index = data_row.pop("index", None)
            index2 = data_row.pop("index2", None)
            sample_project = data_row.pop("sample_project", None)
            sample_name = data_row.pop("sample_name", None)
            override_cycles = data_row.pop("override_cycles", None)
            barcode_mismatches_index1 = data_row.pop("barcode_mismatches_index1", None)
            barcode_mismatches_index2 = data_row.pop("barcode_mismatches_index2", None)
            adapter_read_1 = data_row.pop("adapter_read_1", None)
            adapter_read_2 = data_row.pop("adapter_read_2", None)
            adapter_behavior = data_row.pop("adapter_behavior", None)
            adapter_stringency = data_row.pop("adapter_stringency", None)

            if not len(data_row) == 0:
                for key, value in data_row.items():
                    logger.error(f"Did not ingest data row column '{key}' with value '{value}'")
                    raise AttributeError

            bclconvert_data_row_obj_list.append(
                BCLConvertDataRow(
                    sample_id=sample_id,
                    lane=lane,
                    index=index,
                    index2=index2,
                    sample_project=sample_project,
                    sample_name=sample_name,
                    override_cycles=override_cycles,
                    barcode_mismatches_index1=barcode_mismatches_index1,
                    barcode_mismatches_index2=barcode_mismatches_index2,
                    adapter_read_1=adapter_read_1,
                    adapter_read_2=adapter_read_2,
                    adapter_behavior=adapter_behavior,
                    adapter_stringency=adapter_stringency,
                )
            )

        return cls(
            bclconvert_datarows=bclconvert_data_row_obj_list
        )

    def validate_model(self):
        BCLConvertDataSectionModel.model_validate(self)
