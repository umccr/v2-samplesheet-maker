#!/usr/bin/env python3

def pascal_case_to_snake_case(pascal_case_string: str) -> str:
    """
    Convert a string from PascalCase to snake_case
    We make the following exceptions
    TrimUMI -> TrimUmi -> trim_umi
    Sample_ID -> SampleId -> sample_id
    Cloud_Workflow -> CloudWorkflow -> cloud_workflow
    Index_ID -> IndexId -> index_id
    I7_Index_ID -> I7IndexId -> i7_index_id
    I5_Index_ID -> I5IndexId -> i5_index_id
    Sample_Type -> SampleType -> sample_type
    Sample_Description -> SampleDescription -> sample_description
    BCLConvert_Settings -> BclconvertSettings -> bclconvert_settings
    TSO500L_Settings -> Tso500lSettings -> tso500l_settings
    TSO500_Settings -> Tso500Settings -> tso500_settings
    # Needs to be processed after converting to snake case
    Read1Cycles -> Read_1_Cycles -> read1cycles -> read_1_cycles
    :param pascal_case_string:
    :return:
    """
    # Replace UMI with Umi
    pascal_case_string = pascal_case_string.replace("UMI", "Umi")
    # Replace ID with Id
    pascal_case_string = pascal_case_string.replace("ID", "Id")
    # Replace BCLConvert with BclConvert
    pascal_case_string = pascal_case_string.replace("BCLConvert", "Bclconvert")
    # Replace TSO500L with Tso500L
    pascal_case_string = pascal_case_string.replace("TSO500L", "Tso500l")
    # Replace TSO500 with Tso500
    pascal_case_string = pascal_case_string.replace("TSO500", "Tso500")

    # Remove underscores
    pascal_case_string = "".join(pascal_case_string.split("_"))

    snake_case_string = ""
    for i in range(len(pascal_case_string)):
        if pascal_case_string[i].isupper() and i != 0:
            snake_case_string += "_"
        snake_case_string += pascal_case_string[i].lower()

    # Replace read1_cycles with read_1_cycles
    snake_case_string = snake_case_string.replace("read1_cycles", "read_1_cycles")
    # Replace read2_cycles with read_2_cycles
    snake_case_string = snake_case_string.replace("read2_cycles", "read_2_cycles")
    # Replace index1_cycles with index_1_cycles
    snake_case_string = snake_case_string.replace("index1_cycles", "index_1_cycles")
    # Replace index2_cycles with index_2_cycles
    snake_case_string = snake_case_string.replace("index2_cycles", "index_2_cycles")
    # Replace barcode_mismatches_index1 with barcode_mismatches_index_1
    snake_case_string = snake_case_string.replace("barcode_mismatches_index1", "barcode_mismatches_index_1")
    # Replace barcode_mismatches_index2 with barcode_mismatches_index_2
    snake_case_string = snake_case_string.replace("barcode_mismatches_index2", "barcode_mismatches_index_2")
    # Replace adapter_read1 with adapter_read_1
    snake_case_string = snake_case_string.replace("adapter_read1", "adapter_read_1")
    # Replace adapter_read2 with adapter_read_2
    snake_case_string = snake_case_string.replace("adapter_read2", "adapter_read_2")

    return snake_case_string


def snake_case_to_upper_snake_case(snake_case_str: str) -> str:
    """
    Convert cloud_tso500l_pipeline to Cloud_TSO500L_Pipeline
    :param snake_case_str:
    :return:
    """
    upper_snake_case_str = "_".join(
        list(
            map(
                lambda str_iter: str_iter[0].title() + str_iter[1:],
                snake_case_str.split("_")
            )
        )
    )

    # Replace tso500l with TSO500L
    upper_snake_case_str = upper_snake_case_str.replace("Tso500l", "TSO500L")

    return upper_snake_case_str
