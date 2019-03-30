
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/generators'))

from automake_gen import AutoMakeGen
from cmake_gen import CMakeGen
from make_gen import MakeGen
from rule_generator import RuleGenerator
from rule_generator import get_c_rule_generator
from rule_generator import get_cpp_rule_generator
from rule_generator import get_header_rule_generator

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
