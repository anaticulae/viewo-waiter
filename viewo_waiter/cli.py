#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import argparse

import utila

import viewo_waiter.app


@utila.saveme
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', default=5001)
    parser.add_argument(
        '--safe',
        default=False,
        action='store_true',
        help='store resource in encryption container',
    )
    parser.add_argument(
        '--verbose',
        '-V',
        default=0,
        action='count',
        help='increase verbosity of logging',
    )
    argv = parser.parse_args()
    host, port = argv.host, int(argv.port)
    # set verbose level
    utila.level_setup(argv.verbose)
    config = dict(safe=argv.safe,)
    viewo_waiter.app.run_app(
        host,
        port,
        config,
    )
    return utila.SUCCESS
