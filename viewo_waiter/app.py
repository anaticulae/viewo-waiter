# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import flask

import viewo_waiter.config
from viewo_waiter.api.document import *  # pylint:disable=wildcard-import,W0614


def create_app(config=None) -> flask.Flask:
    # Flask determines template- and static-folder automatically.
    result = flask.Flask(__name__)

    result.config['MAX_CONTENT_LENGTH'] = viewo_waiter.config.MAX_FILE_SIZE
    result.secret_key = viewo_waiter.config.SECRET_KEY
    configure(result, config)

    # data API
    result.register_blueprint(
        viewo_waiter.api.document.api_documents,
        url_prefix=viewo_waiter.config.API_PREFIX,
    )
    return result


def configure(appi, config):
    """Set environment for application. Decide between test environment and
    production environment

    Args:
        appi(Flask): application to configure, which holds config
        config(dict): vars to export as global environment
    """
    if config is None:
        # Production environment
        # load the instance config, if it exists
        common_, todo_, ready_ = configo.environment()
        appi.config['COMMON'] = common_
        appi.config['TODO'] = todo_
        appi.config['READY'] = ready_
    else:
        # Test environment
        # load the test config if passed in
        appi.config.update(config)
