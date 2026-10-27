# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configos

MAX_FILE_SIZE = configos.HV_MB(default=16)

FILE_READ_TIMEOUT = configos.HV_SECOND(default=10)

SECRET_KEY = configos.HV_SECRET(default='helmut_max_pr_absIsVe').value
API_PREFIX = configos.HV_API(default='/api/v0').value

DOCUMENT_NAME_LENGTH = configos.HV_INT_PLUS(default=32)
