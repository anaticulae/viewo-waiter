# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os

WAITER_TRESOR = 'WAITER_TRESOR'


@functools.lru_cache
def tresor():
    path = os.getenv(WAITER_TRESOR, None)
    assert path, 'DEFINE: WAITER_TRESOR'
    os.makedirs(path, exist_ok=True)
    return path


def tresor_space():
    path = os.path.join(tresor(), 'space')
    os.makedirs(path, exist_ok=True)
    return path
