
import os
from conans import ConanFile, CMake

# This easily allows to copy the package in other user or channel
CHANNEL = os.getenv("CONAN_CHANNEL", "stable")
USERNAME = os.getenv("CONAN_USERNAME", "osechet")

class QtTestConan(ConanFile):
    """ Qt Conan package test """

    requires = "Qt/5.8.0@%s/%s" % (USERNAME, CHANNEL)
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "virtualenv"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake "%s" %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def test(self):
        if self.settings.os == "Windows":
            self.run("activate && %s %s" % (os.sep.join([".", "bin", "helloworld"]), "conan"))
            self.run("activate && %s %s" % (os.sep.join([".", "bin", "helloworld2"]), "conan"))
            #self.run("activate && %s %s" % (os.sep.join([".", "bin", "hellogui"]), "conan"))
        else:
            self.run("%s %s" % (os.sep.join([".", "bin", "helloworld"]), "conan"))
            self.run("%s %s" % (os.sep.join([".", "bin", "helloworld2"]), "conan"))
            #self.run("%s %s" % (os.sep.join([".", "bin", "hellogui"]), "conan"))
