
import re

class AutoMakeGen:

    def generate(self, options):
        with open("Makefile.am", "w") as output_file:
            bin_filename = re.sub(r"[ \t-+.]", "_", options.output)
            output_file.write("AUTOMAKE_OPTIONS = foreign\n\n")
            output_file.write("bin_PROGRAMS = %s\n" % (bin_filename))
            self.__write_sources(output_file, options, bin_filename)
            if self.__contains_c(options):
                self.__write_cflags(output_file, options, bin_filename)
            if self.__contains_cpp(options):
                self.__write_cxxflags(output_file, options, bin_filename)
            if options.ldflags:
                self.__write_ldflags(output_file, options, bin_filename)
            if options.link_libraries:
                self.__write_ldadd(output_file, options, bin_filename)

    def __contains_cpp(self, options):
        for source in options.sources:
            if source.endswith(".cpp"):
                return True
        return False

    def __contains_c(self, options):
        for source in options.sources:
            if source.endswith(".c"):
                return True
        return False

    def __write_flags(self, output_file, options,
                      bin_filename, flagname, flags):
        output_file.write("%1s_%2s = " % (bin_filename, flagname))
        output_file.write(flags)
        for define in options.defines:
            output_file.write(" -D%s" % (define))
        output_file.write("\n")

    def __write_cflags(self, output_file, options, bin_filename):
        self.__write_flags(output_file, options, bin_filename, "CFLAGS",
                           options.cflags)

    def __write_cxxflags(self, output_file, options, bin_filename):
        self.__write_flags(output_file, options, bin_filename, "CXXFLAGS",
                           options.cxxflags)

    def __write_ldflags(self, output_file, options, bin_filename):
        self.__write_flags(output_file, options, bin_filename, "LDFLAGS",
                           options.ldflags)

    def __write_sources(self, output_file, options, bin_filename):
        output_file.write("%s_SOURCES = \\\n" % (bin_filename))
        files = list(C_DependencyFinder().find_dependencies(options.sources))
        last_index = len(files) - 1
        for i in range(0, last_index):
            source = files[i]
            if os.path.exists(source):
                output_file.write("\t%s \\\n" % (source))
        if last_index >= 0:
            source = files[last_index]
            if os.path.exists(source):
                output_file.write("\t%s\n" % (source))

    def __write_ldadd(self, output_file, options, bin_filename):
        output_file.write("%s_LDADD =" % (bin_filename))
        for lib in options.link_libraries:
            output_file.write(" -l%s" % (lib))
        output_file.write("\n")