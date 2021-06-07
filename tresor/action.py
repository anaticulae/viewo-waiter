# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila
import utilasafe

import tresor


def insert_file(data: bytes):
    assert data, 'empty data'
    encrypted = str(utilasafe.encrypt_public(data))
    path = filepath_new()
    utila.file_create(path, encrypted)
    return path


def filepath_new():
    spacepath = tresor.tresor_space()
    filecount = len(utila.file_list(spacepath))
    filename = f'{filecount}'.zfill(5)
    result = os.path.join(spacepath, filename)
    return result
