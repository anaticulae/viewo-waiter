# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import pytest

import tresor.config

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name


@pytest.fixture
def tresornew(testdir, monkeypatch):
    with monkeypatch.context() as context:
        context.setenv(tresor.config.WAITER_TRESOR, str(testdir.tmpdir))
        yield testdir.tmpdir
