#!/usr/bin/env python

import re

# https://regex101.com/r/AneCvL/1
HEADER_REGEX_MATCH = re.compile(
    r"\[([a-zA-Z0-9_]+)](?:,*)?"
)
