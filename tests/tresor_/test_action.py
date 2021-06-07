# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import tresor


def test_action_file_new(tresornew):
    content = b'Binary data'
    tresor.insert_file(content)
    assert len(utila.file_list(tresornew)) == 1
    tresor.insert_file(content)
    assert len(utila.file_list(tresornew)) == 2
