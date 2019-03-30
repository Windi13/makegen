# Options for Make

class MakeOptions:
    def __init__(self):
        self.project_name = "my_project"
        self.c_compiler = "gcc"
        self.cpp_compiler = "g++"
        self.as_compiler = "as"
        self.sources = []
        self.root_dir = None
        self.output = None
        self.link_libraries = []
        self.defines = []
        self.library_paths = []
        self.include_paths = []
        self.cflags = "-g -O2 -Wall"
        self.cxxflags = "-g -O2 -Wall"
        self.ldflags = ""