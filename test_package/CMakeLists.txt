project(helloworld)
cmake_minimum_required(VERSION 2.8.12)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
list(APPEND CMAKE_PREFIX_PATH "${CONAN_QT_ROOT}")

find_package(Qt5Core 5.6)

set(CMAKE_AUTOMOC ON)
set(AUTOMOC_MOC_OPTIONS PROPERTIES FOLDER CMakeAutomocTargets)
set_property(GLOBAL PROPERTY AUTOMOC_FOLDER CMakeAutomocTargets)

add_executable(helloworld main.cpp)
target_include_directories(helloworld
    PRIVATE
    ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(helloworld
    PUBLIC
    Qt5::Core
)
