from conans import ConanFile
import os, sys
from conans.tools import download, unzip, untargz, replace_in_file, vcvars_command
from conans import CMake, ConfigureEnvironment


class QtConan(ConanFile):
    name = "Qt"
    version = "5.6.1-1"
    ZIP_FOLDER_NAME = "qt-everywhere-opensource-src-5.6.1"
    settings = "os", "arch", "compiler", "build_type"
    url="http://github.com/osechet/conan-qt"
    license="http://doc.qt.io/qt-5/lgpl.html"
    short_paths = True

    def system_requirements(self):
        if self.settings.os == "Linux": # Further check for debian based missing
            self.run("sudo apt-get install -y libgl1-mesa-dev libxcb1 libxcb1-dev "
                     "libx11-xcb1 libx11-xcb-dev libxcb-keysyms1 libxcb-keysyms1-dev "
                     "libxcb-image0 libxcb-image0-dev libxcb-shm0 libxcb-shm0-dev "
                     "libxcb-icccm4 libxcb-icccm4-dev libxcb-sync1 libxcb-sync-dev "
                     "libxcb-xfixes0-dev libxrender-dev libxcb-shape0-dev "
                     "libxcb-randr0-dev libxcb-render-util0 libxcb-render-util0-dev "
                     "libxcb-glx0-dev libxcb-xinerama0 libxcb-xinerama0-dev")

    def source(self):
        major = ".".join(self.version.split(".")[:2])
        url = "http://download.qt.io/official_releases/qt/{major}/{v}/single/qt-everywhere-opensource-src-{v}".format(major=major, v=self.version)
        if self.settings.os == "Windows":
            zip_name = "qt.zip"
            url += ".zip"
        else:
            zip_name = "qt.tar.gz"
            url += ".tar.gz"

        download(url, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)
            
        if self.settings.os != "Windows":
            self.run("chmod +x ./%s/configure" % self.ZIP_FOLDER_NAME)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        debug = "-debug" if self.settings.build_type == "Debug" else "-release"
        base_command = "configure -opensource -confirm-license -nomake examples -nomake tests -prefix dist %s" % debug

        if self.settings.os == "Windows":
            vcvars = vcvars_command(self.settings)
            set_env = 'SET PATH={dir}/qtbase/bin;{dir}/gnuwin32/bin;%PATH%'.format(dir=self.conanfile_directory)
            command = base_command + " -opengl dynamic"
            # it seems not enough to set the vcvars for older versions, it works fine with MSVC2015 without -platform
            if self.settings.compiler == "Visual Studio":
                if self.settings.compiler.version == "12":
                    command += " -platform win32-msvc2013"
                if self.settings.compiler.version == "11":
                    command += " -platform win32-msvc2012"
                if self.settings.compiler.version == "10":
                    command += " -platform win32-msvc2010"

            self.run("cd %s && %s && %s && %s" % (self.ZIP_FOLDER_NAME, set_env, vcvars, command))
            self.run("cd %s && %s && nmake" % (self.ZIP_FOLDER_NAME, vcvars))
            self.run("cd %s && %s && nmake install" % (self.ZIP_FOLDER_NAME, vcvars))
        else:
            command = base_command + " -silent"
            if self.settings.os == "Linux":
                command += " -xcb"
  
            concurrency = 1
            try:
                import multiprocessing
                concurrency = multiprocessing.cpu_count()
            except (ImportError, NotImplementedError):
                pass

            self.run("cd %s && ./%s" % (self.ZIP_FOLDER_NAME, command))
            self.run("cd %s && make -j %s" % (self.ZIP_FOLDER_NAME, concurrency))
            self.run("cd %s && make install" % (self.ZIP_FOLDER_NAME))

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        src = "%s/qtbase/dist" % (self.ZIP_FOLDER_NAME)
        if self.settings.os == "Windows":
            src = "%s/qtbase/bin/dist" % (self.ZIP_FOLDER_NAME)
        self.copy(pattern="*", src=src)

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

        if self.settings.os == "Windows":
            # Some missing shared libs inside QML and others, but for the test it works
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
