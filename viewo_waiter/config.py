# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

MAX_FILE_SIZE = configo.HV_MB(default=16)

FILE_READ_TIMEOUT = configo.HV_SECOND(default=10)

SECRET_KEY = configo.HV_SECRET(default='helmut_max_pr_absIsVe').value
API_PREFIX = configo.HV_API(default='/api/v0').value

DOCUMENT_NAME_LENGTH = configo.HV_INT_PLUS(default=32)
