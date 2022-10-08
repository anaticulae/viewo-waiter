# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configo
import utila

WAITER_TRESOR = 'WAITER_TRESOR'

TRESOR_USE = 'TRESOR_USE'


@utila.cacheme
def tresor():
    path = configo.env(WAITER_TRESOR, default=None)
    assert path, 'DEFINE: WAITER_TRESOR'
    os.makedirs(path, exist_ok=True)
    return path


@utila.cacheme
def tresor_space():
    path = os.path.join(tresor(), 'space')
    os.makedirs(path, exist_ok=True)
    return path


def tresor_use():
    return configo.env(TRESOR_USE, default=False)
