#!/usr/bin/env python

import re

# https://regex101.com/r/oRfry0/1
HEADER_REGEX_MATCH = re.compile(
    r"\[([a-zA-Z_]+)](?:,*)?"
)
