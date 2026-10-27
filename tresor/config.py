# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import configos
import utilo

WAITER_TRESOR = 'WAITER_TRESOR'

TRESOR_USE = 'TRESOR_USE'


@utilo.cacheme
def tresor():
    path = configos.env(WAITER_TRESOR, default=None)
    assert path, 'DEFINE: WAITER_TRESOR'
    os.makedirs(path, exist_ok=True)
    return path


@utilo.cacheme
def tresor_space():
    path = os.path.join(tresor(), 'space')
    os.makedirs(path, exist_ok=True)
    return path


def tresor_use():
    return configos.env(TRESOR_USE, default=False)
