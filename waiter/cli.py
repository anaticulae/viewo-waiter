#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import utila
import utila.cli

import waiter

COMMANDS = []  # add additional commands here


@utila.saveme
def main():
    parser = utila.cli.create_parser(
        COMMANDS,
        config=utila.ParserConfiguration(
            outputparameter=False,
            inputparameter=False,
            pages=False,
            cacheflag=False,
            waitingflag=False,
        ),
        prog='waiter',
        version=waiter.__version__,
    )
    args = utila.parse(parser)  # pylint:disable=W0613
    return utila.SUCCESS
