from conans import ConanFile
import os, sys
from conans.tools import download, unzip, untargz, replace_in_file
from conans import CMake, ConfigureEnvironment


class QtConan(ConanFile):
    name = "Qt"
    version = "5.6.0"
    ZIP_FOLDER_NAME = "qt-everywhere-opensource-src-%s" % version
    generators = "gcc"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url="http://github.com/osechet/conan-qt"
    license="http://doc.qt.io/qt-5/lgpl.html"
    short_paths = True

    def system_requirements(self):
        # TODO: check if jom is available on Windows
        if self.settings.os == "Linux": # Further check for debian based missing
            self.run("sudo apt-get update; sudo apt-get install -y libgl1-mesa-dev libxcb1 libxcb1-dev "
                     "libx11-xcb1 libx11-xcb-dev libxcb-keysyms1 libxcb-keysyms1-dev "
                     "libxcb-image0 libxcb-image0-dev libxcb-shm0 libxcb-shm0-dev "
                     "libxcb-icccm4 libxcb-icccm4-dev libxcb-sync1 libxcb-sync-dev "
                     "libxcb-xfixes0-dev libxrender-dev libxcb-shape0-dev "
                     "libxcb-randr0-dev libxcb-render-util0 libxcb-render-util0-dev "
                     "libxcb-glx0-dev libxcb-xinerama0 libxcb-xinerama0-dev")

    def source(self):
        if self.settings.os == "Windows":
            zip_name = "qt.zip"
            download("http://download.qt.io/official_releases/qt/5.6/5.6.0/single/qt-everywhere-opensource-src-5.6.0.zip", zip_name)
        elif self.settings.os == "Linux":
            zip_name = "qt.tar.gz"
            download("http://download.qt.io/official_releases/qt/5.6/5.6.0/single/qt-everywhere-opensource-src-5.6.0.tar.gz", zip_name)

        unzip(zip_name)
        os.unlink(zip_name)
            
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        if self.settings.os == "Windows":
            env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
            # TODO:
            # update PATH to contains qtbase\bin and gnuwin32\bin
            # set QMAKESPEC to correct platform

        args = ["-opensource", "-confirm-license", "-no-compile-examples", "-nomake", "tests", "-prefix", "_dist"]
        if not self.options.shared:
            args.insert(0, "-static")

        if self.settings.os == "Windows":
            args += ["-opengl", "dynamic"]
            self.run("cd %s && configure %s" % (self.ZIP_FOLDER_NAME, " ".join(args)))
        elif self.settings.os == "Linux":
            args += ["-silent", "-xcb"]
            self.run("cd %s && ./configure %s" % (self.ZIP_FOLDER_NAME, " ".join(args)))
        else:
            args += ["-silent"]
            self.run("cd %s && ./configure %s" % (self.ZIP_FOLDER_NAME, " ".join(args)))
        
        if self.settings.os == "Windows":
            self.run("cd %s && jom" % (self.ZIP_FOLDER_NAME))
            self.run("cd %s && jom install" % (self.ZIP_FOLDER_NAME))
        else:
            concurrency = 1
            try:
                import multiprocessing
                concurrency = multiprocessing.cpu_count()
            except (ImportError, NotImplementedError):
                pass

            self.run("cd %s && make -j %s" % (self.ZIP_FOLDER_NAME, concurrency))
            self.run("cd %s && make install" % (self.ZIP_FOLDER_NAME))

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        
        # TODO: find why the dist directory is not the same
        if self.settings.os == "Windows":
            dirstdir = "%s/qtbase/bin/_dist" % (self.ZIP_FOLDER_NAME)
        else:
            dirstdir = "%s/qtbase/_dist" % (self.ZIP_FOLDER_NAME)
        
        self.copy("*", dst="include", src="%s/include" % (dirstdir))
        self.copy(pattern="*", dst="bin", src="%s/bin" % (dirstdir))
        self.copy(pattern="*", dst="lib", src="%s/lib" % (dirstdir))
        self.copy(pattern="*", dst="doc", src="%s/doc" % (dirstdir))
        self.copy(pattern="*", dst="examples", src="%s/examples" % (dirstdir))
        self.copy(pattern="*", dst="mkspecs", src="%s/mkspecs" % (dirstdir))
        self.copy(pattern="*", dst="phrasebooks", src="%s/phrasebooks" % (dirstdir))
        self.copy(pattern="*", dst="plugins", src="%s/plugins" % (dirstdir))
        self.copy(pattern="*", dst="qml", src="%s/qml" % (dirstdir))
        self.copy(pattern="*", dst="translations", src="%s/translations" % (dirstdir))

    def package_info(self):
        libs = ['Qt53DCore', 'Qt53DInput', 'Qt53DLogic',
                'Qt53DQuickInput', 'Qt53DQuickRender', 'Qt53DQuick',
                'Qt53DRender', 'Qt5Bluetooth', 'Qt5CLucene',
                'Qt5Concurrent', 'Qt5Core', 'Qt5DBus',
                'Qt5DesignerComponents', 'Qt5Designer', 'Qt5Gui',
                'Qt5Help', 'Qt5LabsTemplates', 'Qt5Location',
                'Qt5MultimediaQuick_p', 'Qt5Multimedia', 'Qt5MultimediaWidgets',
                'Qt5Network', 'Qt5Nfc', 'Qt5OpenGL',
                'Qt5Positioning', 'Qt5PrintSupport', 'Qt5Qml',
                'Qt5QuickParticles', 'Qt5Quick', 'Qt5QuickTest',
                'Qt5QuickWidgets', 'Qt5Script', 'Qt5ScriptTools',
                'Qt5Sensors', 'Qt5SerialBus', 'Qt5SerialPort',
                'Qt5Sql', 'Qt5Svg', 'Qt5Test',
                'Qt5WebChannel', 'Qt5WebSockets', 'Qt5Widgets',
                'Qt5X11Extras', 'Qt5XcbQpa', 'Qt5XmlPatterns',
                'Qt5Xml']
        if self.settings.os == "Windows" and self.settings.build_type == "Debug":
            self.cpp_info.libs = ["%sd" % lib for lib in libs]
        else:
            self.cpp_info.libs = libs
