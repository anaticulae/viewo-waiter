# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http
import threading
import time

import link
import utila
import utilatest

import tests
import viewo_waiter.app


def test_api_upload_document_done(client):
    result = utilatest.apiupload(client, '/documents', 'file', tests.MINIMAL)
    assert result['documentid']


def test_api_upload_directory_error(td):
    """Try to upload a windows folder."""
    host, port = 'localhost', 2345
    server = threading.Thread(
        target=viewo_waiter.app.run_app,
        kwargs=dict(
            host=host,
            port=port,
            config=dict(TESTING=True),
        ),
        daemon=True,
    )
    server.start()
    # wait for startup
    time.sleep(1)
    api = f'http://{host}:{port}/api/v0/documents'
    filepath = td.tmpdir
    cmd = f'curl -F "file=@{filepath}" {api}'
    # TODO: VERIFY EXPECTED RESULT LATER
    completed = utila.run(cmd, expect=None)
    linux = '{"error":"bad request","message":"not a pdf file"}' in completed.stdout
    win = 'read function returned funny value' in completed.stderr
    assert linux or win


def test_api_upload_document_wrong_datatype(client):
    utilatest.apiupload(
        client,
        '/documents',
        'file',
        __file__,
        expected=http.HTTPStatus.BAD_REQUEST,
    )


def test_api_upload_with_wrong_field(client):
    """Upload one file and check if it is saved at common todo folder"""
    # count files in todo folder
    files_before = link.count_todo()

    # Upload with wrong field
    utilatest.apiupload(
        client,
        page='/documents',
        field='o_o',
        path=tests.MINIMAL,
        expected=http.HTTPStatus.BAD_REQUEST,
    )
    files_after = link.count_todo()
    # check that no file was uploaded
    assert files_after == files_before
