
import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))

from rule_generator import RULE_GENERATORS
from rule_generator import get_c_rule_generator
from rule_generator import get_cpp_rule_generator
from rule_generator import get_header_rule_generator

class MakeGen:

    def __init__(self):
        self.rule_generator = {}
        for generator in RULE_GENERATORS:
            for ext in generator.handled_extensions():
                self.rule_generator[ext] = generator

    def generate(self, options):
        c_compiler = None
        cpp_compiler = None
        object_files = []
        link_libraries = options.link_libraries
        compiler_flags = self.__compiler_flags(options)

        for f in options.sources:
            base, ext = self.__split_extension(f)
            if ext in get_c_rule_generator().handled_extensions():
                c_compiler = options.c_compiler
                object_files.append(base + ".o")
            elif ext in get_cpp_rule_generator().handled_extensions():
                cpp_compiler = options.cpp_compiler
                object_files.append(base + ".o")

        with open("Makefile", "w") as output_file:
            # variables
            if c_compiler:
                output_file.write("CC=%s\n" % (c_compiler))
                output_file.write("CFLAGS=%(CFLAGS)s %(FLAGS)s\n"
                                  % {"FLAGS": compiler_flags,
                                     "CFLAGS": options.cflags})
            if cpp_compiler:
                output_file.write("CXX=%s\n" % (cpp_compiler))
                output_file.write("CXXFLAGS=%(CXXFLAGS)s %(FLAGS)s\n"
                                  % {"FLAGS": compiler_flags,
                                     "CXXFLAGS": options.cxxflags})
            if object_files:
                output_file.write("OBJS=%s\n" % (' '.join(object_files)))
                output_file.write("LDFLAGS=%(LDFLAGS)s %(FLAGS)s\n"
                                  % {"FLAGS": self.__linker_flags(options),
                                     "LDFLAGS": options.ldflags})
            output_file.write("\n")

            # all
            if object_files:
                output_file.write("all: %1s\n\n" % options.output)
            else:
                output_file.write("all:\n\n")

            # executable
            if object_files:
                output_file.write("%1s: $(OBJS)\n" % (options.output))
                linker = "$(CC)"
                if cpp_compiler:
                    linker = "$(CXX)"
                output_file.write("\t%1s -o %2s $(LDFLAGS) $(OBJS)\n\n"
                                  % (linker, options.output))

            # object files
            for f in options.sources:
                self.__generate_rule(f, output_file)

            # clean
            output_file.write("clean:\n")
            for f in object_files:
                output_file.write("\trm -f %s\n" % (f)) # remove *.o
            if object_files:
                output_file.write("\trm -f %s\n" % (options.output))

    def __linker_flags(self, options):
        flags = []
        for lib in options.link_libraries:
            flags.append("-l%s" % (lib))
        for path in options.library_paths:
            flags.append("-L%s" % (path))
        return ' '.join(flags)

    def __compiler_flags(self, options):
        flags = []
        for d in options.defines:
            flags.append("-D%s" % (d))
        for path in options.include_paths:
            flags.append("-I%s" % (path))
        return ' '.join(flags)

    def __split_extension(self, filename):
        name, ext = os.path.splitext(filename)
        ext = ext[1:] # remove leading '.'
        return (name, ext)

    def __generate_rule(self, filename, output_file):
        name, ext = self.__split_extension(filename)
        if ext not in self.rule_generator:
            print("warning: don't know how to generate rule for \"%s\"" % (filename))
            return
        generator = self.rule_generator[ext]
        rule = generator.generate_rule(filename)
        output_file.write(rule)
