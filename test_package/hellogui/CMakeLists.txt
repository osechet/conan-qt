

find_package(Qt5Widgets REQUIRED)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_INCLUDE_CURRENT_DIR ON)
set(AUTOMOC_MOC_OPTIONS PROPERTIES FOLDER CMakeAutomocTargets)
set_property(GLOBAL PROPERTY AUTOMOC_FOLDER CMakeAutomocTargets)

add_executable(hellogui main.cpp mainwindow.cpp)
target_include_directories(helloworld
    PRIVATE
    ${CMAKE_CURRENT_BINARY_DIR}
)
target_link_libraries(hellogui
    PUBLIC
    Qt5::Widgets
)

