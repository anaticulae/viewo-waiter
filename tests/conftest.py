# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utilasafe

import tresor.config
import viewo_waiter

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PUBLIC = os.path.join(viewo_waiter.ROOT, 'tests/rsa/public.pem')
PRIVATE = os.path.join(viewo_waiter.ROOT, 'tests/rsa/private.pem')


@pytest.fixture
def tresornew(testdir, monkeypatch):
    with monkeypatch.context() as context:
        context.setenv(tresor.config.WAITER_TRESOR, str(testdir.tmpdir))
        context.setenv(utilasafe.UTILASAFE_PUBLIC_KEY, str(PUBLIC))
        yield testdir.tmpdir
