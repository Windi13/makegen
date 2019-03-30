#!/usr/bin/env python
# quickly generate makefile for c/c++ source files

import sys
import os
import json
import argparse


from make_options import MakeOptions
from generators import list_generators
from generators import GENERATORS
from rule_generator import RULE_GENERATORS

def build_argument_parser():
    parser = argparse.ArgumentParser(
        description="Generate makefile from source files.")
    parser.add_argument("--files", type=str, nargs="+",
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
    options.sources = arg.files
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

def load_files_from_path(path):
    extensions = []
    sources = []
    for gen in RULE_GENERATORS:
        for ext in gen.handled_extensions():
            extensions.append(ext)

    for root, subdirs, files in os.walk(path):
        for f in files:
            filename, ext = os.path.splitext(f)
            if ext[1:] in extensions:
                sources.append(f)

    return sources

def check_for_makegen_file(arg, options):
    if not os.path.isfile('makegen.json'):
        print('No makegen.json found')
        return 
    
    with open('makegen.json', 'r') as config:
        raw = json.loads(config.read())
        data = {k.upper():v for k,v in raw.items()}

        if "CC" in data:
            options.c_compiler = data["CC"]
        if "CXX" in data:
            options.cpp_compiler = data["CXX"]
        if "AS" in data:
            options.as_compiler = data["AS"]
        if "ASFLAGS" in data:
            options.asflags = data["ASFLAGS"]
        if "CFLAGS" in data:
            options.cflags = data["CFLAGS"]
        if "LDFLAGS" in data:
            options.ldflags = data["LDFLAGS"]
        if "OUTPUT" in data:
            options.output = data["OUTPUT"]
        if "LINK_LIBS" in data:
            options.link_libraries = data["LINK_LIBS"]
        if "PATH_LIBS" in data:
            options.library_paths = data["PATH_LIBS"]
        if "INCLUDE_PATHS" in data:
            options.include_paths = data["INCLUDE_PATHS"]
        if "CXXFLAGS" in data:
            options.cxxflags = data["CXXFLAGS"]
        if "DEFINES" in data:
            options.defines = data["DEFINES"]
        if "ROOT_DIR" in data:
            options.root_dir = data["ROOT_DIR"]
            options.sources = load_files_from_path(options.root_dir)
        if "PROJECT_NAME" in data:
            options.project_name = data["PROJECT_NAME"]
        if "OUTPUT" in data:
            options.output = data["OUTPUT"]

if __name__ == "__main__":
    parser = build_argument_parser()
    arg = parser.parse_args()

    options = build_make_options(arg)

    check_for_makegen_file(arg, options)

    print(vars(options))

    if not options.root_dir and not options.sources:
        print("error: specify files on the command line or supply them with \"ROOT_DIR\" in the makegen.json file")
        exit(1)

    if arg.format in GENERATORS:
        generator = GENERATORS[arg.format]
        generator.generate(options)
    else:
        print("error: unknown format %1s" % arg.format)
        print("supported formats are: %1s" % list_generators())
