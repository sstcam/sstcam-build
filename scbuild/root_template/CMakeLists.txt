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


IF(EXISTS "${CMAKE_SOURCE_DIR}/sstcam-control")
  set(SSTCAM_FULL ON)
  message("${Magenta}###################################")
  message("${Magenta}#######Setting up SSTCam FULL######")
  message("${Magenta}###################################${ColourReset}")
else()
  set(SSTCAM_FULL OFF)
  message("${Yellow}###################################")
  message("${Yellow}#######Setting up SSTCam Lite######")
  message("${Yellow}###################################${ColourReset}")
endif()


set_property(GLOBAL PROPERTY USE_FOLDERS ON)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
include(cmake/python_setup.cmake)
include(cmake/sstcam_test.cmake)
include(cmake/sstcam_library.cmake)
# option(UNITTEST "Enable unit test" OFF)
# option(COMPILER_WARNINGS "Turn compiler warnings on" OFF)

# TODO: Should make testing optional
enable_testing()
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
# Save executables to bin directory
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

if((APPLE) OR (EXISTS $ENV{CONDA_PREFIX}))
  # The following settings were copied from
  # https://cmake.org/Wiki/CMake_RPATH_handling
  # to avoid the rpath issue (issue #11998) that appears on OS X El Capitan
  # https://forge.in2p3.fr/issues/11998

  # use, i.e. don't skip the full RPATH for the build tree
  set(CMAKE_SKIP_BUILD_RPATH  FALSE)

  # when building, don't use the install RPATH already
  # (but later on when installing)
  set(CMAKE_BUILD_WITH_INSTALL_RPATH FALSE)

  set(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}/lib")

  # add the automatically determined parts of the RPATH
  # which point to directories outside the build tree to the install RPATH
  set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
endif()

find_package(Git QUIET)

# This function helps to quite verbose includes
function(message)
    if (NOT MESSAGE_QUIET)
        _message(${ARGN})
    endif()
endfunction()

# Finding the python interpreter and setting up the python package directory structure in build
find_package(PythonInterp)
set(PYTHON_PACKAGE_PATH "${CMAKE_BINARY_DIR}/python/sstcam/")
set(PYTHON_EXTENSIONS_PATH "${CMAKE_BINARY_DIR}/python/sstcam/_ext")
set(PYTHON_TESTS_PATH "${CMAKE_BINARY_DIR}/python/tests")
file(MAKE_DIRECTORY ${PYTHON_PACKAGE_PATH})
file(MAKE_DIRECTORY ${PYTHON_EXTENSIONS_PATH})
file(MAKE_DIRECTORY ${PYTHON_TESTS_PATH})
file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/python/__init__.py" DESTINATION ${PYTHON_PACKAGE_PATH})
file(COPY "${CMAKE_CURRENT_SOURCE_DIR}/setup.py" DESTINATION "${CMAKE_BINARY_DIR}/python")


###############################################################################
#                              DEPENDENCIES
###############################################################################
# Here we pull down dependencies directly into the build
message(STATUS "${BoldCyan}Pulling dependencies${ColourReset}")
message(STATUS "${Cyan}pybind11${ColourReset}")
include(FetchContent)
FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11
    GIT_TAG        v2.4.3
    GIT_SHALLOW TRUE
)

FetchContent_GetProperties(pybind11)
if(NOT pybind11_POPULATED)
    FetchContent_Populate(pybind11)
    add_subdirectory(${pybind11_SOURCE_DIR} ${pybind11_BINARY_DIR})
endif()


message(STATUS "${Cyan}doctest${ColourReset}")
FetchContent_Declare(
    doctest
    GIT_REPOSITORY https://github.com/onqtam/doctest
    GIT_TAG        2.3.6
    GIT_SHALLOW TRUE
)
FetchContent_GetProperties(doctest)
if(NOT doctest_POPULATED)
    FetchContent_Populate(doctest)
    add_subdirectory(${doctest_SOURCE_DIR} ${doctest_BINARY_DIR})
endif()
set(DOCTEST_INCLUDE_DIR ${doctest_SOURCE_DIR}/doctest CACHE INTERNAL "Path to include folder for doctest")

if(SSTCAM_FULL)
  message(STATUS "${Cyan}open62541${ColourReset}")
  FetchContent_Declare(
      open62541proj
      GIT_REPOSITORY https://github.com/open62541/open62541
      GIT_TAG         v1.0.1
      GIT_SHALLOW TRUE
  )
  FetchContent_GetProperties(open62541proj)
  if(NOT open62541proj_POPULATED)
      FetchContent_Populate(open62541proj)
      set(MESSAGE_QUIET ON)
      add_subdirectory(${open62541proj_SOURCE_DIR} ${open62541proj_BINARY_DIR})
      unset(MESSAGE_QUIET)
  endif()

  # set protobuf include dir to null
  set(Protobuf_IMPORT_DIR )
endif()

###############################################################################
#                      Adding subprojects and repos
###############################################################################


message(STATUS "${BoldBlue}sstcam-common${ColourReset}")
add_subdirectory(sstcam-common)

if(SSTCAM_FULL)
  message(STATUS "${BoldBlue}sstcam-control${ColourReset}")
  add_subdirectory(sstcam-control)
endif()

###############################################################################
#                      Adding custom utility targets
###############################################################################

find_program(DOT_EXE "dot")
if(DOT_EXE)
    message(STATUS "dot found: ${DOT_EXE}")
else()
    message(STATUS "dot not found!")
endif()

set(DOT_OUTPUT_TYPE "png" CACHE STRING "Build a dependency graph. Options are dot output types: ps, png, pdf..." )

if(DOT_EXE)
    add_custom_target(dependency-graph
        COMMAND ${CMAKE_COMMAND} ${CMAKE_SOURCE_DIR} --graphviz=${CMAKE_BINARY_DIR}/graphviz/${PROJECT_NAME}.dot
        COMMAND ${DOT_EXE} -T${DOT_OUTPUT_TYPE} ${CMAKE_BINARY_DIR}/graphviz/${PROJECT_NAME}.dot -o ${CMAKE_BINARY_DIR}/${PROJECT_NAME}.${DOT_OUTPUT_TYPE}
    )

    add_custom_command(
        TARGET dependency-graph POST_BUILD
        COMMAND ;
        COMMENT
        "Dependency graph generated and located at ${CMAKE_BINARY_DIR}/${PROJECT_NAME}.${DOT_OUTPUT_TYPE}"
    )
endif()