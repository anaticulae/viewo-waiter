# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import pytest
import utila
import utilasafe
import utilatest
from utilatest import mp  # pylint:disable=W0611
from utilatest import td  # pylint:disable=W0611

import tresor.config
import viewo_waiter
import viewo_waiter.app
import viewo_waiter.config

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PUBLIC = os.path.join(viewo_waiter.ROOT, 'tests/rsa/public.pem')
PRIVATE = os.path.join(viewo_waiter.ROOT, 'tests/rsa/private.pem')

utilatest.setup(viewo_waiter.config.API_PREFIX)

# required to access tresor correctly
utila.cache_disable()


@pytest.fixture
def tresornew(td, mp):  # pylint:disable=W0621
    with mp.context() as context:
        context.setenv(tresor.config.WAITER_TRESOR, str(td.tmpdir))
        context.setenv(utilasafe.UTILASAFE_PUBLIC_KEY, str(PUBLIC))
        yield td.tmpdir


@pytest.fixture
def app(td):  # pylint:disable=W0621
    """Create and configure a new app instance for each test."""

    todo = os.path.join(td.tmpdir, 'todo')
    ready = os.path.join(td.tmpdir, 'ready')

    os.makedirs(todo)
    os.makedirs(ready)

    assert os.path.exists(todo), todo
    assert os.path.exists(ready), ready

    # create the app with common test config
    config = {
        'TESTING': True,
        'COMMON': td.tmpdir,
        'TODO': todo,
        'READY': ready,
    }
    # disable tracking in test run # TODO: MOVE TO CONFIG
    application = viewo_waiter.app.create_app(config=config)

    # ensure to create app context: TODO: THINK ABOUT IT
    with application.app_context():
        yield application


@pytest.fixture
def client(app):  # pylint:disable=W0621
    """A test client for the app."""
    return app.test_client()
