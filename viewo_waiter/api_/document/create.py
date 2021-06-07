# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import flask_login
import link


def create_document(resource, public:bool):
    userid, password = user_account(public)
    document = store_resource(resource.pdf, resource.filename, userid)
    return document, userid, password


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
