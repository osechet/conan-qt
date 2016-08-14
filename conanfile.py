from conans import ConanFile
import os, sys
from conans.tools import download, unzip, untargz, replace_in_file, vcvars_command, os_info, SystemPackageTool
from conans import CMake, ConfigureEnvironment


class QtConan(ConanFile):
    name = "Qt"
    version = "5.6.1-1"
    ZIP_FOLDER_NAME = "qt-everywhere-opensource-src-5.6.1"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    url="http://github.com/osechet/conan-qt"
    license="http://doc.qt.io/qt-5/lgpl.html"
    short_paths = True

    def system_requirements(self):
        pack_name = None
        if os_info.linux_distro == "ubuntu":
            pack_name = ("libgl1-mesa-dev libxcb1 libxcb1-dev "
                         "libx11-xcb1 libx11-xcb-dev libxcb-keysyms1 libxcb-keysyms1-dev "
                         "libxcb-image0 libxcb-image0-dev libxcb-shm0 libxcb-shm0-dev "
                         "libxcb-icccm4 libxcb-icccm4-dev libxcb-sync1 libxcb-sync-dev "
                         "libxcb-xfixes0-dev libxrender-dev libxcb-shape0-dev "
                         "libxcb-randr0-dev libxcb-render-util0 libxcb-render-util0-dev "
                         "libxcb-glx0-dev libxcb-xinerama0 libxcb-xinerama0-dev")
        if pack_name:
            installer = SystemPackageTool()
            installer.update() # Update the package database
            installer.install(pack_name) # Install the package

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

        args = ["-opensource", "-confirm-license", "-no-compile-examples", "-nomake tests", "-prefix _dist"]
        if not self.options.shared:
            args.insert(0, "-static")
        if self.settings.build_type == "Debug":
            args.append("-debug")
        else:
            args.append("-release")

        if self.settings.os == "Windows":
            vcvars = vcvars_command(self.settings)
            set_env = 'SET PATH={dir}/qtbase/bin;{dir}/gnuwin32/bin;%PATH%'.format(dir=self.conanfile_directory)
            args += ["-opengl dynamic"]
            # it seems not enough to set the vcvars for older versions, it works fine with MSVC2015 without -platform
            if self.settings.compiler == "Visual Studio":
                if self.settings.compiler.version == "12":
                    args += ["-platform win32-msvc2013"]
                if self.settings.compiler.version == "11":
                    args += ["-platform win32-msvc2012"]
                if self.settings.compiler.version == "10":
                    args += ["-platform win32-msvc2010"]

            self.run("cd %s && %s && %s && configure %s" % (self.ZIP_FOLDER_NAME, set_env, vcvars, " ".join(args)))
            self.run("cd %s && %s && nmake" % (self.ZIP_FOLDER_NAME, vcvars))
            self.run("cd %s && %s && nmake install" % (self.ZIP_FOLDER_NAME, vcvars))
        else:
            if self.settings.os == "Linux":
                args += ["-silent", "-xcb"]
            else:
                args += ["-silent"]

            concurrency = 1
            try:
                import multiprocessing
                concurrency = multiprocessing.cpu_count()
            except (ImportError, NotImplementedError):
                pass

            self.run("cd %s && ./configure %s" % (self.ZIP_FOLDER_NAME, " ".join(args)))
            self.run("cd %s && make -j %s" % (self.ZIP_FOLDER_NAME, concurrency))
            self.run("cd %s && make install" % (self.ZIP_FOLDER_NAME))

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        src = "%s/qtbase/_dist" % (self.ZIP_FOLDER_NAME)
        if self.settings.os == "Windows":
            src = "%s/qtbase/bin/_dist" % (self.ZIP_FOLDER_NAME)
        self.copy(pattern="*", src=src)

    def package_info(self):
        libs = ['3DCore', '3DInput', '3DLogic',
                '3DQuickInput', '3DQuickRender', '3DQuick',
                '3DRender', 'Bluetooth', 'CLucene',
                'Concurrent', 'Core', 'DBus',
                'DesignerComponents', 'Designer', 'Gui',
                'Help', 'LabsTemplates', 'Location',
                'MultimediaQuick_p', 'Multimedia', 'MultimediaWidgets',
                'Network', 'Nfc', 'OpenGL',
                'Positioning', 'PrintSupport', 'Qml',
                'QuickParticles', 'Quick', 'QuickTest',
                'QuickWidgets', 'Script', 'ScriptTools',
                'Sensors', 'SerialBus', 'SerialPort',
                'Sql', 'Svg', 'Test',
                'WebChannel', 'WebSockets', 'Widgets',
                'XmlPatterns', 'Xml']
        if self.settings.os != "Windows":
            libs += ['X11Extras', 'XcbQpa']

        self.cpp_info.libs = []
        self.cpp_info.includedirs = ["include"]
        for lib in libs:
            if self.settings.os == "Windows" and self.settings.build_type == "Debug":
                suffix = "d"
            else:
                suffix = ""
            self.cpp_info.libs += ["Qt5%s%s" % (lib, suffix)]
            self.cpp_info.includedirs += ["include/Qt%s" % lib]

        if self.settings.os == "Windows":
            # Some missing shared libs inside QML and others, but for the test it works
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
