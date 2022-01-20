# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import multiprocessing
import os

import utila
import utilasafe

import tresor


def insert_file(data: bytes, wait: bool = True):
    assert data, 'empty data'
    path = filepath_new()
    # create file to avoid threading side effects
    utila.file_create(path, '')
    if wait:
        async_insert(path, data)
    else:
        multiprocessing.Process(target=async_insert, args=(path, data)).start()
    return path


def async_insert(path, data):
    encrypted = str(utilasafe.encrypt_public(data))
    utila.debug(f'write to tresor: {path}')
    utila.file_replace(path, encrypted)


def filepath_new():
    spacepath = tresor.tresor_space()
    filecount = len(utila.file_list(spacepath))
    filename = f'{filecount}'.zfill(5)
    result = os.path.join(spacepath, filename)
    return result
