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
import viewo_waiter.api.documents
import viewo_waiter.api_.document.upload


@viewo_waiter.api.documents.api_documents.route('/documents', methods=['POST'])
def document_create() -> str:
    resource = viewo_waiter.api_.document.upload.receive_resource()
    if not hasattr(resource, 'pdf'):
        # could not load resource, provide error message
        return resource

    # if public flag is provided, document is accessable by all user
    public = utila.str2bool(flask.request.args.get('public', False))
    userid, password = user_account(public)
    resource = store_resource(resource.pdf, resource.filename, userid)

    result = viewo_api.success(
        userid=userid,
        password=password,
        document=flask.url_for(
            'api_documents.document_get',
            documentid=resource,
        ),
        # link=flask.url_for('waiting.waiting_view', process=resource),
    )
    return result


def user_account(public: bool = False):
    if public:
        nopassword = ''
        return link.PUBLIC_OWNER, nopassword
    userid = flask_login.current_user.get_id()
    if not userid:
        # generate new random user
        userid, password = viewo.api.users.post.create_user()
        # TODO: REFACTOR
        viewo.user.auth.login_user(userid)
    else:
        password = ''  # nosec
    viewo.user.auth.public_password_set(password)
    return userid, password


def store_resource(pdf, filename, userid):
    todo = link.create_todo(
        file=pdf,
        filename=filename,
        todopath=viewo.path.todo(),
        owner=userid,
    )
    _, resource = os.path.split(todo)
    # allow user to access document
    viewo.api.users.utils.user.user_document_append(userid, resource)
    return resource
