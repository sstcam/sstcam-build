macro(sstcam_add_test EXE SRC TARGET LIBTARGET)
    add_executable(${EXE} ${SRC} $<TARGET_OBJECTS:${TARGET}>)
    add_test(NAME ${EXE} COMMAND ${EXE})
    target_link_libraries(${EXE} ${LIBTARGET})
    target_include_directories(${EXE} PUBLIC ctests ${DOCTEST_INCLUDE_DIR})
    target_compile_features(${EXE} PRIVATE cxx_std_11)
endmacro()

macro(sstcam_tests )
    set( _OPTIONS_ARGS )
    set( _ONE_VALUE_ARGS)
    set( _MULTI_VALUE_ARGS TESTS LIBTARGETS INCLUDE_DIRS)

    cmake_parse_arguments( _SSTCAM_TESTS "${_OPTIONS_ARGS}" "${_ONE_VALUE_ARGS}" "${_MULTI_VALUE_ARGS}" ${ARGN} )
    add_library(test_main_${PROJECT_NAME} OBJECT ctests/test_main.cc)
    target_include_directories("test_main_${PROJECT_NAME}" PUBLIC ctests ${DOCTEST_INCLUDE_DIR})
    if(_SSTCAM_TESTS_TESTS)
        foreach(item ${_SSTCAM_TESTS_TESTS})
            add_executable(${item} "ctests/${item}.cc" $<TARGET_OBJECTS:test_main_${PROJECT_NAME}>)
            add_test(NAME ${item} COMMAND ${item})
            target_link_libraries(${item} ${_SSTCAM_TESTS_LIBTARGETS})
            target_include_directories(${item} PUBLIC ctests ${DOCTEST_INCLUDE_DIR})
        endforeach(item)
    endif()
endmacro()