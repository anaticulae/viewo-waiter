# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import utila
import utilasafe

import tests.conftest
import tresor


def test_action_file_new(tresornew):
    content = b'Binary data'
    tresor.insert_file(content)
    assert len(utila.file_list(tresornew)) == 1
    tresor.insert_file(content)
    assert len(utila.file_list(tresornew)) == 2


def test_tresor_encrypt(tresornew):
    content = b'Binary data'
    tresor.insert_file(content)
    loaded = utila.file_read(os.path.join(tresornew, 'space/00000'))
    loaded = int(loaded)
    assert loaded != content
    private = utila.file_read(tests.conftest.PRIVATE)
    decrypted = utilasafe.decrypt_public(str(loaded), private)
    assert decrypted == content
