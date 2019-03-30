#!/usr/bin/env python
# quickly generate makefile for c/c++ source files

import sys
import os
import argparse


from make_options import MakeOptions
from generators import list_generators
from generators import GENERATORS

def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Generate makefile from source files.")
    parser.add_argument("file", type=str, nargs="+",
                        help="source files")
    parser.add_argument("-o", "--output", type=str, default=None,
                        help="the name of the output executable or library")
    parser.add_argument("-f", "--format", default="make",
                        help="format of the output makefile.")
    parser.add_argument("-l", action="append", dest="link_libraries",
                        help="link to a library")
    parser.add_argument("-D", action="append", dest="defines",
                        help="add a preprocessor definition")
    parser.add_argument("-L", action="append", dest="library_paths",
                        help="add a library path")
    parser.add_argument("-I", action="append", dest="include_paths",
                        help="add a include path")
    parser.add_argument("-n", "--name", type=str, default="my_project",
                        help="name of the project")
    parser.add_argument("--cflags", type=str, default=None,
                        help="c compiler flags")
    parser.add_argument("--cxxflags", type=str, default=None,
                        help="c++ compiler flags")
    parser.add_argument("--ldflags", type=str, default=None,
                        help="linker flags")
    return parser

def build_make_options(arg):
    options = MakeOptions()
    options.project_name = arg.name
    options.sources = arg.file
    options.output = "a.out"
    if arg.output:
        options.output = arg.output
    if arg.link_libraries:
        options.link_libraries = arg.link_libraries
    if arg.defines:
        options.defines = arg.defines
    if arg.library_paths:
        options.library_paths = arg.library_paths
    if arg.include_paths:
        options.include_paths = arg.include_paths
    if arg.cflags:
        options.cflags = arg.cflags
    if arg.cxxflags:
        options.cxxflags = arg.cxxflags
    if arg.ldflags:
        options.ldflags = arg.ldflags
    return options

if __name__ == "__main__":
    parser = build_argument_parser()
    arg = parser.parse_args()
    options = build_make_options(arg)

    if arg.format in GENERATORS:
        generator = GENERATORS[arg.format]
        generator.generate(options)
    else:
        print("error: unknown format %1s" % arg.format)
        print("supported formats are: %1s" % list_generators())
