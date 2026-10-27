# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import multiprocessing
import os

import utilo
import utilosafe

import tresor
import tresor.config


def insert_file(data: bytes, wait: bool = True):
    assert data, 'empty data'
    path = filepath_new()
    # create file to avoid threading side effects
    utilo.file_create(path, '')
    if wait:
        async_insert(path, data)
    else:
        multiprocessing.Process(target=async_insert, args=(path, data)).start()
    return path


def async_insert(path, data):
    if tresor.tresor_use():
        encrypted = utilosafe.encrypt_password(data)
    else:
        encrypted = data
    utilo.debug(f'write to tresor: {path}')
    utilo.file_replace_binary(path, encrypted)


def filepath_new():
    spacepath = tresor.tresor_space()
    filecount = len(utilo.file_list(spacepath))
    filename = f'{filecount}'.zfill(5)
    result = os.path.join(spacepath, filename)
    return result
