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
import flask_login
import utila

import viewo_api
import viewo_waiter
import viewo_waiter.config


def create_app(config=None) -> flask.Flask:
    # Flask determines template- and static-folder automatically.
    result = flask.Flask(__name__)

    result.config['MAX_CONTENT_LENGTH'] = viewo_waiter.config.MAX_FILE_SIZE
    result.secret_key = viewo_waiter.config.SECRET_KEY
    configure(result, config)

    # data API
    result.register_blueprint(
        viewo_waiter.api_documents,
        url_prefix=viewo_waiter.config.API_PREFIX,
    )
    return result


def run_app(host, port, config=None):
    created = create_app(config)
    logsetup(created, host, port)
    created.run(host=host, port=port)


def configure(app, config):
    """Set environment for application. Decide between test environment and
    production environment

    Args:
        app(Flask): application to configure, which holds config
        config(dict): vars to export as global environment
    """
    if config is None:
        # Production environment
        # load the instance config, if it exists
        common_, todo_, ready_ = configo.environment()
        app.config['COMMON'] = common_
        app.config['TODO'] = todo_
        app.config['READY'] = ready_
    else:
        # Test environment
        # load the test config if passed in
        app.config.update(config)
    create_loginmanager(app)


def create_loginmanager(app):
    loginmanager = flask_login.LoginManager()
    loginmanager.init_app(app)
    loginmanager._user_callback = load_user  # pylint:disable=W0212
    # loginmanager.localize_callback = localize_callback


def load_user(userid):
    return viewo_api.FlaskUser(identifier=userid)


def logsetup(app, host, port):
    utila.log('\nSETUP VIEWO_WAITER\n')
    utila.log(f'host: {host}')
    utila.log(f'port: {port}')
    for key in ['COMMON', 'TODO', 'READY']:
        utila.log(f'{key.lower()}:{app.config[key]}')
    utila.log()


# def localize_callback(message: str) -> str:
#     if message == flask_login.LOGIN_MESSAGE:
#         return 'Bitte einloggen um Zugriff zu erhalten.'
#     if message == flask_login.LOGIN_MESSAGE:
#         return 'Bitte erneut einloggen um Zugriff zu erhalten.'
#     return message
