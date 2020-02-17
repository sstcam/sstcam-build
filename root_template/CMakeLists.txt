cmake_minimum_required(VERSION 3.10...3.16)
#Just to get some pretty colors
if(NOT WIN32)
  string(ASCII 27 Esc)
  set(ColourReset "${Esc}[m")
  set(ColourBold  "${Esc}[1m")
  set(Red         "${Esc}[31m")
  set(Green       "${Esc}[32m")
  set(Yellow      "${Esc}[33m")
  set(Blue        "${Esc}[34m")
  set(Magenta     "${Esc}[35m")
  set(Cyan        "${Esc}[36m")
  set(White       "${Esc}[37m")
  set(BoldRed     "${Esc}[1;31m")
  set(BoldGreen   "${Esc}[1;32m")
  set(BoldYellow  "${Esc}[1;33m")
  set(BoldBlue    "${Esc}[1;34m")
  set(BoldMagenta "${Esc}[1;35m")
  set(BoldCyan    "${Esc}[1;36m")
  set(BoldWhite   "${Esc}[1;37m")
endif()

project(SSTCameraSoftware)
include(cmake/python_setup.cmake)
# option(PYTHON "Build the Python wrapper" ON)
# option(UNITTEST "Enable unit test" OFF)
# option(COMPILER_WARNINGS "Turn compiler warnings on" OFF)
# option(NUMPY "Enable returning NumPy arrays in a few methods" ON)

# message(STATUS "${BoldGreen} pybind11 ${ColourReset}")
# add_subdirectory(pybind11)

# TODO: Should make testing optional
enable_testing()


# Python stuff
find_package(Python3 COMPONENTS Interpreter)
set(PYTHON_PACKAGE_PATH "${CMAKE_BINARY_DIR}/python/sstcam/")
set(PYTHON_EXTENSIONS_PATH "${CMAKE_BINARY_DIR}/python/sstcam/_ext")
set(PYTHON_TESTS_PATH "${CMAKE_BINARY_DIR}/python/tests")
file(MAKE_DIRECTORY ${PYTHON_PACKAGE_PATH})
file(MAKE_DIRECTORY ${PYTHON_EXTENSIONS_PATH})
file(MAKE_DIRECTORY ${PYTHON_TESTS_PATH})
file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/python/__init__.py" DESTINATION ${PYTHON_PACKAGE_PATH})
file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/setup.py" DESTINATION "python/${CMAKE_BINARY_DIR}")


message(STATUS "${BoldBlue}sstcam-base${ColourReset}")
add_subdirectory(sstcam-base)
message(STATUS "${BoldBlue}sstcam-template${ColourReset}")
add_subdirectory(sstcam-template)
message(STATUS "${BoldBlue}sstcam-common${ColourReset}")
add_subdirectory(sstcam-common)

