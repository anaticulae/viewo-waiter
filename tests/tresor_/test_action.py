# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utilo
import utilosafe

import tresor


def test_action_file_new(tresornew):
    content = b'Binary data'
    tresor.insert_file(content)
    assert len(utilo.file_list(tresornew)) == 1
    tresor.insert_file(content)
    assert len(utilo.file_list(tresornew)) == 2


def test_tresor_encrypt(tresornew):
    content = b'Binary data'
    tresor.insert_file(content)
    loaded = utilo.file_read_binary(os.path.join(tresornew, 'space/00000'))
    assert loaded != content
    decrypted = utilosafe.decrypt_password(loaded)
    assert decrypted == content
