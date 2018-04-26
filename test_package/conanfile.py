from conans.model.conan_file import ConanFile
from conans import CMake
import os

############### CONFIGURE THESE VALUES ##################
default_user = "osechet"
default_channel = "stable"
#########################################################

channel = os.getenv("CONAN_CHANNEL", default_channel)
username = os.getenv("CONAN_USERNAME", default_user)

class QtTestConan(ConanFile):
    """ Qt Conan package test """
    name = "DefaultName"
    version = "0.1"
    requires = "Qt/5.9.2@%s/%s" % (username, channel)
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake", "virtualenv"

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def test(self):
        if self.settings.os == "Windows":
            self.run("activate && %s %s" % (os.sep.join([".", "bin", "helloworld"]), "conan"))
            self.run("activate && %s %s" % (os.sep.join([".", "bin", "helloworld2"]), "conan"))
            #self.run("activate && %s %s" % (os.sep.join([".", "bin", "hellogui"]), "conan"))
        else:
            self.run("%s %s" % (os.sep.join([".", "bin", "helloworld"]), "conan"))
            self.run("%s %s" % (os.sep.join([".", "bin", "helloworld2"]), "conan"))
            #self.run("%s %s" % (os.sep.join([".", "bin", "hellogui"]), "conan"))
