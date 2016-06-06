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
    url="http://github.com/osechet/conan-qt"
    license="http://doc.qt.io/qt-5/lgpl.html"

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
            # todo:
            # update PATH to contains qtbase\bin and gnuwin32\bin
            # set QMAKESPEC to correct platform

        if self.settings.os == "Windows":
            self.run("cd %s && configure -opensource -confirm-license -silent -opengl dynamic -no-compile-examples -nomake tests -prefix dist" % (self.ZIP_FOLDER_NAME))
        elif self.settings.os == "Linux":
            self.run("cd %s && ./configure -opensource -confirm-license -silent -xcb -no-compile-examples -nomake tests -prefix dist" % (self.ZIP_FOLDER_NAME))
        else:
            self.run("cd %s && ./configure -opensource -confirm-license -silent -no-compile-examples -nomake tests -prefix dist" % (self.ZIP_FOLDER_NAME))
        
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
        
        self.copy("*", dst="include", src="%s/qtbase/dist/include" % (self.ZIP_FOLDER_NAME))
        self.copy(pattern="*", dst="bin", src="%s/qtbase/dist/bin" % (self.ZIP_FOLDER_NAME))
        self.copy(pattern="*", dst="lib", src="%s/qtbase/dist/lib" % (self.ZIP_FOLDER_NAME))
        self.copy(pattern="*", dst="doc", src="%s/qtbase/dist/doc" % (self.ZIP_FOLDER_NAME))
        self.copy(pattern="*", dst="examples", src="%s/qtbase/dist/examples" % (self.ZIP_FOLDER_NAME))
        self.copy(pattern="*", dst="mkspecs", src="%s/qtbase/dist/mkspecs" % (self.ZIP_FOLDER_NAME))
        self.copy(pattern="*", dst="phrasebooks", src="%s/qtbase/dist/phrasebooks" % (self.ZIP_FOLDER_NAME))
        self.copy(pattern="*", dst="plugins", src="%s/qtbase/dist/plugins" % (self.ZIP_FOLDER_NAME))
        self.copy(pattern="*", dst="qml", src="%s/qtbase/dist/qml" % (self.ZIP_FOLDER_NAME))
        self.copy(pattern="*", dst="translations", src="%s/qtbase/dist/translations" % (self.ZIP_FOLDER_NAME))

    def package_info(self):
        if self.settings.os == "Windows":
            if self.settings.build_type == "Debug":
                self.cpp_info.libs = ['Qt53DCored', 'Qt53DInputd', 'Qt53DLogicd',
                'Qt53DQuickInputd', 'Qt53DQuickRenderd', 'Qt53DQuickd',
                'Qt53DRenderd', 'Qt5Bluetoothd', 'Qt5CLucened',
                'Qt5Concurrentd', 'Qt5Cored', 'Qt5DBusd',
                'Qt5DesignerComponentsd', 'Qt5Designerd', 'Qt5Guid',
                'Qt5Helpd', 'Qt5LabsTemplatesd', 'Qt5Locationd',
                'Qt5MultimediaQuick_pd', 'Qt5Multimediad', 'Qt5MultimediaWidgetsd',
                'Qt5Networkd', 'Qt5Nfcd', 'Qt5OpenGLd',
                'Qt5Positioningd', 'Qt5PrintSupportd', 'Qt5Qmld',
                'Qt5QuickParticlesd', 'Qt5Quickd', 'Qt5QuickTestd',
                'Qt5QuickWidgetsd', 'Qt5Scriptd', 'Qt5ScriptToolsd',
                'Qt5Sensorsd', 'Qt5SerialBusd', 'Qt5SerialPortd',
                'Qt5Sqld', 'Qt5Svgd', 'Qt5Testd',
                'Qt5WebChanneld', 'Qt5WebSocketsd', 'Qt5Widgetsd',
                'Qt5X11Extrasd', 'Qt5XcbQpad', 'Qt5XmlPatternsd',
                'Qt5Xmld']
            else:
                self.cpp_info.libs = ['Qt53DCore', 'Qt53DInput', 'Qt53DLogic',
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
        else:
            self.cpp_info.libs = ['Qt53DCore', 'Qt53DInput', 'Qt53DLogic',
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

