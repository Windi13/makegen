
import sys
import os

from automake_gen import AutoMakeGen
from cmake_gen import CMakeGen
from make_gen import MakeGen

GENERATORS = {
    "make": MakeGen(),
    "cmake": CMakeGen(),
    "automake": AutoMakeGen()
}

def list_generators():
    generators = []
    for gen in GENERATORS:
        generators.append(gen)
    return ', '.join(generators)
