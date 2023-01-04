#!/usr/bin/env python
# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

PACKAGES = [
    'tresor',
    'viewo_waiter',
    'viewo_waiter.api',
    'viewo_waiter.api.document',
    'viewo_waiter.api_',
    'viewo_waiter.api_.document',
]
ENTRY_POINTS = dict(console_scripts=[
    'viewo_waiter = viewo_waiter.cli:main',
])

if __name__ == "__main__":
    utila.install(__file__)
