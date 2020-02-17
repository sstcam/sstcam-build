macro(python_module PYTARGET LIBTARGET MODULE_NAME SRC_FILES)
    message("Adding python bindings")
    # pybind
    pybind11_add_module(${PYTARGET} ${SRC_FILES})
    target_link_libraries(${PYTARGET} PRIVATE ${LIBTARGET})
    # Python stuff
    # Creating a symlink to the python package
    add_custom_command(TARGET ${PYTARGET} POST_BUILD
                      COMMAND ${CMAKE_COMMAND} -E create_symlink "${PROJECT_SOURCE_DIR}/python/" "${PYTHON_PACKAGE_PATH}/${MODULE_NAME}")
   set_target_properties(${PYTARGET}
    PROPERTIES
      PREFIX ""
      LIBRARY_OUTPUT_DIRECTORY ${PYTHON_EXTENSIONS_PATH}
    )
    # # Creating a symlink to the python extension in the main python package directory tree
    add_custom_command(TARGET ${PYTARGET} POST_BUILD COMMAND ${CMAKE_COMMAND} -E create_symlink "$<TARGET_FILE:${PYTARGET}>" "${PYTHON_EXTENSIONS_PATH}/${PYTARGET}")
    # Creating a symlink to python tests and add the folder to the ctest test runner
    if(EXISTS "${PROJECT_SOURCE_DIR}/pytests/")
        message("Adding python tests")
        add_custom_command(TARGET ${PYTARGET} POST_BUILD
                      COMMAND ${CMAKE_COMMAND} -E create_symlink "${PROJECT_SOURCE_DIR}/pytests/" "${CMAKE_BINARY_DIR}/python/tests/${MODULE_NAME}")
        if(PYTHONINTERP_FOUND)
          add_test(NAME "${PROJECT_NAME}_pytests" COMMAND python3 -m pytest -r a -v WORKING_DIRECTORY "${CMAKE_BINARY_DIR}/python/tests/${MODULE_NAME}")
        endif()
    endif()
endmacro()