#!/usr/bin/python
# -*- coding: utf-8 -*-

#Libraries
import os
import sys
import platform
import logging
import core.log

from cli.arguments.parser import DEFAULT_PARSER
from cli.arguments.constants import *

#Constants
LOGGER = logging.getLogger(__name__)

# variables
"""
Arguments namespace
"""
args = None

#Functions
"""
Takes the system arguments vector and tries to parse the arguments in it given
the argument parser specified and returns the namespace generated

@param 	parser 	the ArgumentParser objects to use to parse the arguments
@param 	args 	arguments to parse (default is sys.argv)
@return namespace of parsed arguments
"""
def parseArguments(parser, args=None):
	return parser.parse_args(args)

if __name__ == "__main__":
	# Prepare coding
	if platform.system() == "Windows":
		os.system("chcp 65001")
	args = parseArguments(DEFAULT_PARSER)
	# Switching log level
	root_logger = logging.getLogger()
	root_logger.setLevel(LOGS_LEVELS[LOGS.index(args.log_level)])
	#Welcome
	LOGGER.info("Welcome !")
	LOGGER.info("Bye !")
