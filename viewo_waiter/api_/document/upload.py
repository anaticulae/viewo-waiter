# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import urllib.error
import urllib.request

import utila
import viewo_api
import werkzeug.utils

import viewo_waiter.config

HEADER_READ_SIZE = 1024
EXPECTED_PDFSTART = b'%PDF-1.'

Loaded = collections.namedtuple('Loaded', 'pdf filename')


def receive_resource(request) -> Loaded:  # pylint:disable=R0911,R0912
    # TODO: SECURITY: VERIFY THIS METHOD
    if 'url' in request.form:
        # provide resource via link as url-field
        posturl = request.form['url']
        try:
            pdf = curlpdf(posturl)
            filename = 'cloud.pdf'
        except FileTooLarge:
            return viewo_api.bad('file too large')
        except InvalidResource:
            return viewo_api.bad('require pdf file')
        except InvalidUrl:
            return viewo_api.bad('invalid url')
    else:
        # upload resource via upload-file dialog
        if not request.files:
            return viewo_api.bad('missing `file` field')
        pdf = request.files['file']
        if not pdf.filename:
            # if user does not select file, browser also submit an empty
            # part without filename
            return viewo_api.bad('empty `file` field')
        filename = utila.file_name(pdf.filename)
        filename = secure_document_name(filename)
        header = pdf.stream.read(HEADER_READ_SIZE)
        if not valid_pdf(header):
            return viewo_api.bad('not a pdf file')
        # reset stream
        pdf.stream.seek(0)
    return Loaded(pdf, filename)


def secure_document_name(name: str) -> str:
    name = werkzeug.utils.secure_filename(name)
    # shorten document name
    name = name[0:viewo_waiter.config.DOCUMENT_NAME_LENGTH]
    return name


def curlpdf(url: str) -> 'TmpFile':
    try:
        with urllib.request.urlopen(  # nosec
                url,
                timeout=viewo_waiter.config.FILE_READ_TIMEOUT,
        ) as webfile:
            header = webfile.read(HEADER_READ_SIZE)
            # %PDF-1.5 for example
            if not valid_pdf(header):
                utila.error(f'no pdf file: {url}')
                raise InvalidResource(url)
            todo = viewo_waiter.config.MAX_FILE_SIZE - HEADER_READ_SIZE
            content = webfile.read(todo)
            if webfile.read(1) != b'':
                # there are some bytes left
                utila.error(f'file too large: {url}')
                raise FileTooLarge(url)
    except urllib.error.URLError as error:
        utila.error(f'invalid url: {url}')
        raise InvalidUrl(url) from error

    filecontent = header + content
    return TmpFile(filecontent)


class CurlError(ValueError):

    def __init__(self, url):
        super().__init__()
        self.url = url


class FileTooLarge(CurlError):
    pass


class InvalidResource(CurlError):
    pass


class InvalidUrl(CurlError):
    pass


class TmpFile:

    def __init__(self, content):
        self.content = content

    def save(self, path: str):
        utila.file_replace_binary(path, self.content)


def valid_pdf(data):
    typedef = data[0:len(EXPECTED_PDFSTART)]
    return typedef == EXPECTED_PDFSTART
