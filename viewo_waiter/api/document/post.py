# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask
import utila

import viewo_api
import viewo_waiter.api.document
import viewo_waiter.api_.document.create
import viewo_waiter.api_.document.upload


@viewo_waiter.api.document.api_documents.route('/documents', methods=['POST'])
def document_create() -> str:
    resource = viewo_waiter.api_.document.upload.receive_resource()
    if not hasattr(resource, 'pdf'):
        # could not load resource, provide error message
        return resource

    documentid, userid, password = viewo_waiter.api_.document.create.create_document(
        resource,
        public=public(),
    )

    result = viewo_api.success(
        userid=userid,
        password=password,
        documentid=documentid,
        # document=flask.url_for(
        #     'api_documents.document_get',
        #     documentid=resource,
        # ),
        # link=flask.url_for('waiting.waiting_view', process=resource),
    )
    return result


def public() -> bool:
    # if public flag is provided, document is accessable by all user
    result = utila.str2bool(flask.request.args.get('public', False))
    return result
