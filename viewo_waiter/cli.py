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
    argv = parser.parse_args()
    host, port = argv.host, int(argv.port)
    viewo_waiter.app.run_app(host, port)
    return utila.SUCCESS
