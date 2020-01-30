macro(python_module PYTARGET LIBTARGET MODULE_NAME SRC_FILES)
    # pybind
    pybind11_add_module(${PYTARGET} ${SRC_FILES})
    target_link_libraries(${PYTARGET} PRIVATE ${LIBTARGET})
    # Python stuff
    # Creating a symlink to the python package
    add_custom_command(TARGET ${PYTARGET} POST_BUILD
                      COMMAND ${CMAKE_COMMAND} -E create_symlink "${PROJECT_SOURCE_DIR}/python/" "${PYTHON_PACKAGE_PATH}/${MODULE_NAME}")
    # Creating a symlink to the python extension in the main python package directory tree
    add_custom_command(TARGET ${PYTARGET} POST_BUILD COMMAND ${CMAKE_COMMAND} -E create_symlink "$<TARGET_FILE:${PYTARGET}>" "${PYTHON_EXTENSIONS_PATH}/${PYTARGET}")
endmacro()