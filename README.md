Conan package for Qt
--------------------------------------------

[![Build Status](https://travis-ci.org/osechet/conan-qt.svg?branch=testing/5.7.0)](https://travis-ci.org/osechet/conan-qt)

[![Build status](https://ci.appveyor.com/api/projects/status/gboj3x82d42eoasw?svg=true)](https://ci.appveyor.com/project/osechet/conan-qt)

Note: Travis an Appveyor builds are not working because the build of Qt is too long and exceed their time limit.

[![badge](https://img.shields.io/badge/conan.io-Qt%2F5.6.2-green.svg?logo=data:image/png;base64%2CiVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAMAAAAolt3jAAAA1VBMVEUAAABhlctjlstkl8tlmMtlmMxlmcxmmcxnmsxpnMxpnM1qnc1sn85voM91oM11oc1xotB2oc56pNF6pNJ2ptJ8ptJ8ptN9ptN8p9N5qNJ9p9N9p9R8qtOBqdSAqtOAqtR%2BrNSCrNJ/rdWDrNWCsNWCsNaJs9eLs9iRvNuVvdyVv9yXwd2Zwt6axN6dxt%2Bfx%2BChyeGiyuGjyuCjyuGly%2BGlzOKmzOGozuKoz%2BKqz%2BOq0OOv1OWw1OWw1eWx1eWy1uay1%2Baz1%2Baz1%2Bez2Oe02Oe12ee22ujUGwH3AAAAAXRSTlMAQObYZgAAAAFiS0dEAIgFHUgAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQfgBQkREyOxFIh/AAAAiklEQVQI12NgAAMbOwY4sLZ2NtQ1coVKWNvoc/Eq8XDr2wB5Ig62ekza9vaOqpK2TpoMzOxaFtwqZua2Bm4makIM7OzMAjoaCqYuxooSUqJALjs7o4yVpbowvzSUy87KqSwmxQfnsrPISyFzWeWAXCkpMaBVIC4bmCsOdgiUKwh3JojLgAQ4ZCE0AMm2D29tZwe6AAAAAElFTkSuQmCC)](http://www.conan.io/source/Qt/5.6.2/osechet/testing)

[Conan.io](https://conan.io) package for [Qt](https://www.qt.io) library. This package includes by default the Qt Base module (Core, Gui, Widgets, Network, ...). Others modules can be added using options.

The packages generated with this **conanfile** can be found in [conan.io](http://www.conan.io/source/Qt/5.6.2/osechet/testing).

## Reuse the package

### Basic setup

```
$ conan install Qt/5.6.2@osechet/testing
```

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
```
    [requires]
    Qt/5.7.0@osechet/testing

    [options]
    Qt:shared=true # false
    # On Windows, you can choose the opengl mode, default is 'desktop'
    Qt:opengl=desktop # dynamic
    # If you need specific Qt modules, you can add them as follow:
    Qt:websockets=true
    Qt:xmlpatterns=true
    
    [generators]
    txt
    cmake
```
Complete the installation of requirements for your project running:
```
    conan install . 
```
Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.

## Develop the package

### Build packages

    $ pip install conan_package_tools
    $ python build.py
    
### Upload packages to server

    $ conan upload Qt/5.7.0@osechet/testing --all
