# type: ignore
# isort: skip_file
# fmt: off
# pylint: skip-file
from conans import ConanFile, CMake


class ImguiOpencvDemo(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "libde265/1.0.8",\
               "opencv/2.4.13.7",\
               "poco/1.10.1"

    tool_requires = ["pkg_a/4.5.1",
                     ("libtiff/3.9.0@user/testing"),
                     ("glew/2.1.0@dummy/stable", "override"),]

    def build_requirements(self):
        self.tool_requires("tool_win/0.1@user/stable")

    def requirements(self):
        envir = "prod"
        self.requires("opencv/2.2@drl/stable")
        if envir == "prod":
            self.requires(
                "closecv/4.2@drl/stable",
                private=False,
                override=False,
            )
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")
        self.copy("imgui_impl_glfw.cpp", dst="../src", src="./res/bindings")
        self.copy("imgui_impl_opengl3.cpp", dst="../src", src="./res/bindings")
        self.copy("imgui_impl_glfw.h*", dst="../include", src="./res/bindings")
# fmt: on
