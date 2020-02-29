macro(sstcam_python_module)
    set( _OPTIONS_ARGS )
    set( _ONE_VALUE_ARGS MODULE_NAME)
    set( _MULTI_VALUE_ARGS LIBTARGETS SRC_FILES INCLUDE_DIRS)

    cmake_parse_arguments( _PYTHON_MODULE "${_OPTIONS_ARGS}" "${_ONE_VALUE_ARGS}" "${_MULTI_VALUE_ARGS}" ${ARGN} )
    #Checking that we have required arguments
    if(NOT _PYTHON_MODULE_MODULE_NAME)
      message( FATAL_ERROR "sstcam_python_module: 'MODULE_NAME' argument required." )
    endif()
    if(NOT _PYTHON_MODULE_LIBTARGETS)
      message( FATAL_ERROR "sstcam_python_module: 'LIBTARGETS' argument required." )
    endif()
    if(NOT _PYTHON_MODULE_SRC_FILES)
      message( FATAL_ERROR "sstcam_python_module: 'SRC_FILES' argument required." )
    endif()

    message(STATUS "Adding python bindings")
    set(PYTARGET ${PROJECT_NAME})

    # pybind
    pybind11_add_module(${PYTARGET} ${_PYTHON_MODULE_SRC_FILES})
    target_link_libraries(${PYTARGET} PRIVATE ${_PYTHON_MODULE_LIBTARGETS})
    # Python stuff
    # Creating a symlink to the python package
    add_custom_command(TARGET ${PYTARGET} POST_BUILD
                      COMMAND ${CMAKE_COMMAND} -E create_symlink "${PROJECT_SOURCE_DIR}/python/" "${PYTHON_PACKAGE_PATH}/${_PYTHON_MODULE_MODULE_NAME}")
    set_target_properties(${PYTARGET}
    PROPERTIES
      PREFIX ""
      LIBRARY_OUTPUT_DIRECTORY ${PYTHON_EXTENSIONS_PATH}
    )

    if(_PYTHON_MODULE_INCLUDE_DIRS)
      target_include_directories(${PYTARGET} PRIVATE ${_PYTHON_MODULE_INCLUDE_DIRS})
    endif()

    # Creating a symlink to the python extension in the main python package directory tree
    add_custom_command(TARGET ${PYTARGET} POST_BUILD COMMAND ${CMAKE_COMMAND} -E create_symlink "$<TARGET_FILE:${PYTARGET}>" "${PYTHON_EXTENSIONS_PATH}/${PYTARGET}")
    # Creating a symlink to python tests and add the folder to the ctest test runner
    if(EXISTS "${PROJECT_SOURCE_DIR}/pytests/")
        message(STATUS "Adding python tests")
        add_custom_command(TARGET ${PYTARGET} POST_BUILD
                      COMMAND ${CMAKE_COMMAND} -E create_symlink "${PROJECT_SOURCE_DIR}/pytests/" "${CMAKE_BINARY_DIR}/python/tests/${_PYTHON_MODULE_MODULE_NAME}")
        if(PYTHONINTERP_FOUND)
          add_test(NAME "${PROJECT_NAME}_pytests" COMMAND python3 -m pytest --suppress-no-test-exit-code -r a -v  WORKING_DIRECTORY "${CMAKE_BINARY_DIR}/python/tests/${_PYTHON_MODULE_MODULE_NAME}")
        endif()
    endif()
endmacro()