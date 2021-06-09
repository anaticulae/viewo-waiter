#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
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
    viewo_waiter.app.run_app(host, port)
    return utila.SUCCESS
