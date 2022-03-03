#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import contextlib
import http
import json
import json.decoder
import os

import power
import werkzeug.datastructures

import viewo_waiter.config

MINIMAL = power.DOCU007_PDF


def apiupload(
    client,
    page: str,
    field: str,
    path: str,
    prefix=viewo_waiter.config.API_PREFIX,
    expected=http.HTTPStatus.OK,
):
    """Upload file via http post command"""
    assert field, path
    assert os.path.exists(path), path
    request = prefix + page
    fields = werkzeug.datastructures.MultiDict([(field, open(path, 'rb'))])
    response = client.post(request, data=fields, follow_redirects=True)
    assert response.status_code == expected, request + str(response)
    return decode(response, expected=expected)


def decode(
    response,
    expected=None,
) -> dict:
    """Read binary data from response and convert them to str"""
    result = response.data.decode('utf8')
    if expected is not None:
        assert response.status_code == expected
    with contextlib.suppress(json.decoder.JSONDecodeError):
        # json format
        return json.loads(result)
    # html format
    return result


def post(
    client,
    page: str,
    data: dict,
    expected=http.HTTPStatus.OK,
):
    response = client.post(page, data=data, follow_redirects=True)
    assert response.status_code == expected, f'path: {page}, error: {response.status_code}'
    return decode(response, expected=expected)


def apipost(
    client,
    page: str,
    data: dict,
    prefix=viewo_waiter.config.API_PREFIX,
    expected=http.HTTPStatus.OK,
):
    request = prefix + page
    return post(client, page=request, data=data, expected=expected)
