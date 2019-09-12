#!/usr/bin/env python3
# coding: utf8

"""
Script to allow printing using different colors
Author: Jonathan Armas - jarmas@fluidattacks.com
"""

import sys
from termcolor import colored

def print_info(msg, color=''):
    """
    Main function
    """
    if color == '':
        sys.stdout.write(msg)
    else:
        sys.stdout.write(colored(msg, color))

def print_success(msg, color='green'):
    """
    Sucess (green) messages
    """
    print_info(msg, color)

def print_failure(msg, color='red'):
    """
    Failure (red) messages
    """
    print_info(msg, color)

def print_warning(msg, color='yellow'):
    """
    Warning (yellow) messages
    """
    print_info(msg, color)

def print_unknown(msg, color=''):
    """
    Default (white) messages
    """
    print_info(msg, color)

def error_print(path, out, message):
    """
    Print custom error msgs
    """
    print_failure("Issue found in "+path+"\n")
    if out != '':
        print_failure(out)
    print_warning(message+"\n\n")
