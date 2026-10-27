# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import http
import threading
import time

import qvlink
import utilo
import utilotest

import tests
import viewo_waiter.app


def test_api_upload_document_done(client):
    result = utilotest.apiupload(client, '/documents', 'file', tests.MINIMAL)
    assert result['documentid']


def test_api_upload_directory_error(td):
    """Try to upload a windows folder."""
    host, port = 'localhost', 2345
    server = threading.Thread(
        target=viewo_waiter.app.run_app,
        kwargs={
            'host': host,
            'port': port,
            'config': {
                'TESTING': True
            },
        },
        daemon=True,
    )
    server.start()
    # wait for startup
    time.sleep(1)
    api = f'http://{host}:{port}/api/v0/documents'
    filepath = td.tmpdir
    cmd = f'curl -F "file=@{filepath}" {api}'
    # TODO: VERIFY EXPECTED RESULT LATER
    completed = utilo.run(cmd, expect=None)
    linux = '{"error":"bad request","message":"not a pdf file"}' in completed.stdout
    win = 'read function returned funny value' in completed.stderr
    logging = f'{completed.stdout}\n{"="*30}\n{completed.stderr}'
    assert linux or win, logging


def test_api_upload_document_wrong_datatype(client):
    utilotest.apiupload(
        client,
        '/documents',
        'file',
        __file__,
        expected=http.HTTPStatus.BAD_REQUEST,
    )


def test_api_upload_with_wrong_field(client):
    """Upload one file and check if it is saved at common todo folder"""
    # count files in todo folder
    files_before = qvlink.count_todo()

    # Upload with wrong field
    utilotest.apiupload(
        client,
        page='/documents',
        field='o_o',
        path=tests.MINIMAL,
        expected=http.HTTPStatus.BAD_REQUEST,
    )
    files_after = qvlink.count_todo()
    # check that no file was uploaded
    assert files_after == files_before
