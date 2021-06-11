# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import contextlib

import flask
import utila
import viewo_api
import werkzeug.routing

import viewo_waiter.api.document
import viewo_waiter.api_.document.create
import viewo_waiter.api_.document.upload


@viewo_waiter.api.document.api_documents.route('/documents', methods=['POST'])
def document_create() -> str:
    resource = viewo_waiter.api_.document.upload.receive_resource(flask.request)
    if not hasattr(resource, 'pdf'):
        # could not load resource, provide error message
        return resource

    documentid, userid, password = viewo_waiter.api_.document.create.create_document(
        resource,
        public=public(flask.request),
        usesafe=usesafe(),
    )
    optional = optional_links(documentid)

    result = viewo_api.success(
        userid=userid,
        password=password,
        documentid=documentid,
        **optional,
    )
    return result


def public(request) -> bool:
    # if public flag is provided, document is access able by all user
    result = utila.str2bool(request.args.get('public', False))
    return result


def usesafe() -> bool:
    with contextlib.suppress(KeyError):
        return flask.current_app.config['USE_SAFE']
    return False


def optional_links(documentid):
    """Optional links to forward user.

    These are not necessary for usage as a service.
    """
    try:
        # yapf:disable
        optional = dict(
            document=flask.url_for('api_documents.document_get', documentid=documentid),
            link=flask.url_for('waiting.waiting_view', process=documentid),
        )
        # yapf:enable
    except werkzeug.routing.BuildError:
        optional = {}
        utila.debug('skip routes: api_documents.document_get, '
                    'waiting.waiting_view')
    return optional
