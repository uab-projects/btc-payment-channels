#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BTC Payment Channels application.

This software allows to create a payment channel between two
parties by generating transactions with special scripts using the Bitcoin
scripting language.

The software just creates the transactions from the keys introduced and does
not check their validity against the blockchain. Use it at your own risk.
"""
# Libraries
import os
import platform
import logging
import core.log

from cli.arguments.parser import DEFAULT_PARSER
from cli.arguments.constants import LOGS_LEVELS, LOGS

# Constants
LOGGER = logging.getLogger(__name__)

# Variables
args = None


# Functions
def parseArguments(parser, args=None):
    """
    Parse arguments.

    Takes the system arguments vector and tries to parse the arguments in it
    given the argument parser specified and returns the namespace generated.

    Args:
        parser(object): 	the ArgumentParser object to use to
                            parse the arguments.
        args(array):        arguments to parse (default is sys.argv)
    Returns:
        A namespace with the parsed arguments and its values
    """
    return parser.parse_args(args)


if __name__ == "__main__":
    # Prepare coding
    if platform.system() == "Windows":
        os.system("chcp 65001")
    args = parseArguments(DEFAULT_PARSER)
    # Switching log level
    root_logger = logging.getLogger()
    root_logger.setLevel(LOGS_LEVELS[LOGS.index(args.log_level)])
    # Welcome
    LOGGER.info("Welcome !")
    LOGGER.info("Bye !")
