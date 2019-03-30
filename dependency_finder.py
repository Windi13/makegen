
import os
import re

# Dependency Finder
# Is responsible for identifying all dependencies (header files, etc)
# for the given files

class DependencyFinder:

    def handled_extensions(self):
        return set(["c", "cpp", "cxx", "cc", "h", "hpp"])

    # ------ multiple files ------

    def find_dependencies(self, files):
        dep_map = {}
        for f in files:
            self.__find_dependency_for_file(f, dep_map)
        return dep_map

    def __find_dependency_for_file(self, filename, dep_map):
        if filename in dep_map:
            return dep_map[filename]
        deps = set([filename])
        directory = os.path.dirname(filename)
        try:
            with open(filename, "r") as input_file:
                for line in input_file:
                    include_file = self.__extract_include_file(line)
                    if include_file:
                        include_file = os.path.join(directory, include_file)
                        incdeps = self.__find_dependency_for_file(
                                                       include_file, dep_map)
                        deps = deps.union(incdeps)
        except:
            pass
        dep_map[filename] = deps
        return deps

    # ------ single file ------

    def find_dependency(self, filename):
        dep_set = set()
        try:
            self.__find_dependency(filename, dep_set)
        except IOError:
            print("error: failed to open file: %s" % filename)
        return [filename] + list(dep_set)

    def __find_dependency(self, filename, dep_set):
        with open(filename, "r") as input_file:
            for line in input_file:
                self.__process_line(os.path.dirname(filename), line, dep_set)

    def __process_line(self, directory, line, dep_set):
        dependent_file = self.__extract_include_file(line)
        if dependent_file:
            dependent_file = os.path.join(directory, dependent_file)
        if dependent_file != None and dependent_file not in dep_set:
            dep_set.add(dependent_file)
            try:
                self.__find_dependency(dependent_file, dep_set)
            except:
                pass

    def __extract_include_file(self, line):
        # match `#include "file"` but not `#include <file>`
        match = re.match(r'^[ \t]*#[ \t]*include[ \t]*"([^"]*)"', line)
        if match:
            return match.group(1) # filename
        else:
            return None
