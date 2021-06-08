# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import flask_login
import link

import viewo_api
import viewo_api.config
import viewo_api.user
import viewo_api.user.create
import viewo_api.user.password
import viewo_api.user.update


def create_document(resource, public: bool):
    userid, password = user_account(public)
    document = store_resource(resource.pdf, resource.filename, userid)
    return document, userid, password


def user_account(public: bool = False):
    if public:
        nopassword = ''
        return link.PUBLIC_OWNER, nopassword
    password = viewo_api.password_generate()
    userid = flask_login.current_user.get_id()
    if not userid:
        # generate new random user
        created = viewo_api.user.create.create_user(password)
        userid = created.userid
        viewo_api.login(userid, password, publicpassword=True)
    else:
        password = ''  # nosec
    return userid, password


def store_resource(pdf, filename, userid):
    todo = link.create_todo(
        file=pdf,
        filename=filename,
        todopath=viewo_api.config.todo(),
        owner=userid,
    )
    _, resource = os.path.split(todo)
    # allow user to access document
    viewo_api.user.update.user_append_document(userid, resource)
    return resource
