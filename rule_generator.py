
# Rule Generator
# Generates rules for building source files using make

import os
from dependency_finder import DependencyFinder

def __generate_source_to_object_rule(filename, compiler, flags):
    dep_finder = DependencyFinder()
    dependencies = dep_finder.find_dependency(filename)
    base, ext = os.path.splitext(filename)
    rule = "%1s.o: %2s\n" % (base, ' '.join(dependencies))
    rule += "\t%(CC)s -o %(BASE)s.o -c %(FLAGS)s %(FILE)s\n\n" % {
        "CC": compiler,
        "BASE": base,
        "FLAGS": flags,
        "FILE": filename }
    return rule

class RuleGenerator:

    def __init__(self, generate_source_to_object_rule=None, extensions = [], compiler = "", flags = ""):
        self.__generate = generate_source_to_object_rule
        self.__extensions = extensions
        self.__compiler = compiler
        self.__flags = flags

    def handled_extensions(self):
        return set(self.__extensions)
    
    def generate_rule(self, filename):
        if self.__generate:
            return self.__generate(filename, self.__compiler, self.__flags)
        else:
            return ""

__OPTIONS = {
    "C" : {
        "compiler"  : "$(CC)",
        "flags"     : "$(CFLAGS)",
        "extensions": ["c"],
        "generate"  : __generate_source_to_object_rule
    },
    "CPP" : {
        "compiler"  : "$(CXX)",
        "flags"     : "$(CXXFLAGS)",
        "extensions": ["cpp", "cxx",  "cc"],
        "generate"  : __generate_source_to_object_rule
    },
    "H" : {
        "extensions": ["h", "hpp"],
        "compiler"  : "",
        "flags"     : "",
        "generate"  : None
    }
}

def get_c_rule_generator():
    return RuleGenerator(extensions = __OPTIONS["C"]["extensions"],
                            compiler = __OPTIONS["C"]["compiler"],
                            flags = __OPTIONS["C"]["flags"],
                            generate_source_to_object_rule = __OPTIONS["C"]["generate"])


def get_cpp_rule_generator():
    return RuleGenerator(extensions = __OPTIONS["CPP"]["extensions"],
                            compiler = __OPTIONS["CPP"]["compiler"],
                            flags = __OPTIONS["CPP"]["flags"],
                            generate_source_to_object_rule = __OPTIONS["C"]["generate"])


def get_header_rule_generator():
    return RuleGenerator(extensions = __OPTIONS["H"]["extensions"])


RULE_GENERATORS = [
    get_c_rule_generator(),
    get_cpp_rule_generator(),
    get_header_rule_generator()
]
