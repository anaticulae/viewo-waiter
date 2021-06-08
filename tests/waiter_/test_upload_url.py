# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http

import link
import power
import pytest
import utilatest

import tests


def test_api_upload_from_url(client, httpserver):
    httpserver.serve_content(open(power.MASTER072_PDF, mode='br').read())
    source = httpserver.url
    result = utilatest.apipost(client, '/documents', data={'url': source})
    assert result['documentid']


@pytest.mark.parametrize('source, expected_error', [
    pytest.param('http://invalid.dscom', 'invalid url', id='invalid url'),
    pytest.param(f'file:///{__file__}', 'require pdf', id='no pdf'),
])
def test_api_upload_from_url_with_error(source, client, expected_error):
    result = utilatest.apipost(
        client,
        '/documents',
        data={'url': source},
        expected=http.HTTPStatus.BAD_REQUEST,
    )
    assert expected_error in result['message']


def test_api_upload_from_url_too_large_file(client, testdir, httpserver):
    content = b'%PDF-1.5' + b'0' * 1024 * 1024 * 100  # 100 MB
    httpserver.serve_content(content)
    source = httpserver.url
    utilatest.apipost(
        client,
        page='/documents',
        data={'url': source},
        expected=http.HTTPStatus.BAD_REQUEST,
    )


def test_api_upload_file_url(client):
    """Upload one file and check if it is saved at common todo folder"""
    # count files in todo folder
    files_before = link.count_todo()

    utilatest.apiupload(
        client,
        page='/documents',
        field='file',
        path=tests.MINIMAL,
    )
    files_after = link.count_todo()
    # check if file was uploaded
    assert files_after == files_before + 1
