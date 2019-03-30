
class CMakeGen:

    def generate(self, options):
        with open("CMakeLists.txt", "w") as output_file:
            output_file.write("project(%1s)\n" % (options.project_name))
            self.__write_defines(output_file, options)
            self.__write_link_libraries(output_file, options)
            self.__write_add_executable(output_file, options)

    def __write_add_executable(self, output_file, options):
        output_file.write("add_executable(%1s\n" % (options.output))
        dep_map = C_DependencyFinder().find_dependencies(options.sources)
        for f in dep_map:
            if os.path.exists(f): # exclude non-existing files
                output_file.write("\t%1s\n" % (f))
        output_file.write(")\n")

    def __write_link_libraries(self, output_file, options):
        if options.link_libraries:
            output_file.write("link_libraries(%1s\n" % (options.output))
            for lib in options.link_libraries:
                output_file.write("\t%1s\n" % (lib))
            output_file.write(")\n")

    def __write_defines(self, output_file, options):
        if options.defines:
            output_file.write("add_definitions(\n")
            for d in options.defines:
                output_file.write("\t-D%1s\n" % (d))
            output_file.write(")\n")