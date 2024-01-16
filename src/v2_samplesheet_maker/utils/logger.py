#!/usr/bin/env python3

"""
Collect logger through verboselogs package
"""

import verboselogs
import logging

logging.captureWarnings(True)

logger = verboselogs.VerboseLogger(__name__)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

warnings_logger = logging.getLogger("py.warnings")
warnings_logger.addHandler(stream_handler)

import inspect

LOGGER_STYLE = "%(asctime)s - %(levelname)-8s - %(module)-25s - %(funcName)-40s : LineNo. %(lineno)-4d - %(message)s"


def get_caller_function():
    """
    Get the function that was used to call the previous
    Some loggers report <module>
    :return:
    """
    # Get the inspect stack trace
    inspect_stack = inspect.stack()

    # Since we're already in a function, we need the third attribute
    # i.e function of interest -> function that called this one -> this function
    frame_info = inspect_stack[2]

    # Required attribute is' function
    function_id = getattr(frame_info, "function", None)

    if function_id is None:
        # Don't really want to break on this just yet but code is ready to go for it.
        return None
    else:
        return function_id


def set_basic_logger():
    """
    Set the basic logger before we then take in the --deploy-env values to see where we write to
    :return:
    """
    # Get a basic logger
    logger = logging.getLogger()

    # Get a stderr handler
    console = logging.StreamHandler()

    # Set level
    console.setLevel(logging.INFO)

    # Set format
    formatter = logging.Formatter(LOGGER_STYLE)
    console.setFormatter(formatter)

    logger.addHandler(console)

    return logger


def set_logger(script_dir, script, deploy_env, log_level=logging.INFO):
    """
    Initialise a logger
    :return:
    """
    new_logger = logging.getLogger()
    new_logger.setLevel(log_level)

    # create a logging format
    formatter = logging.Formatter(LOGGER_STYLE)

    # create a console handler
    console_handler = logging.StreamHandler()
    # Hard coded as don't need too much verbosity on the console side
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    new_logger.addHandler(console_handler)


def get_logger():
    """
    Return logger object
    :return:
    """
    function_that_called_this_one = get_caller_function()
    return logging.getLogger(function_that_called_this_one)
