# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import hoverpower
import pytest
import qvlink
import utilo
import utilotest

import tests


def test_api_upload_from_url(client, httpserver):
    httpserver.serve_content(utilo.file_read_binary(hoverpower.MASTER072_PDF))
    source = httpserver.url
    result = utilotest.apipost(client, '/documents', data={'url': source})
    assert result['documentid']


@pytest.mark.parametrize('source, expected_error', [
    pytest.param('http://invalid.dscom', 'invalid url', id='invalid url'),
    pytest.param(f'file:///{__file__}', 'require pdf', id='no pdf'),
])
def test_api_upload_from_url_with_error(source, client, expected_error):
    result = utilotest.apipost(
        client,
        '/documents',
        data={'url': source},
        expected=http.HTTPStatus.BAD_REQUEST,
    )
    assert expected_error in result['message']


def test_api_upload_from_url_too_large_file(client, httpserver):
    content = b'%PDF-1.5' + b'0' * 1024 * 1024 * 100  # 100 MB
    httpserver.serve_content(content)
    source = httpserver.url
    utilotest.apipost(
        client,
        page='/documents',
        data={'url': source},
        expected=http.HTTPStatus.BAD_REQUEST,
    )


def test_api_upload_file_url(client):
    """Upload one file and check if it is saved at common todo folder"""
    # count files in todo folder
    files_before = qvlink.count_todo()

    utilotest.apiupload(
        client,
        page='/documents',
        field='file',
        path=tests.MINIMAL,
    )
    files_after = qvlink.count_todo()
    # check if file was uploaded
    assert files_after == files_before + 1
