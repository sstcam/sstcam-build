include( CMakeParseArguments )
macro(sstcam_library )
    set( _OPTIONS_ARGS )
    set( _ONE_VALUE_ARGS )
    set( _MULTI_VALUE_ARGS TARGET_SRCS HEADER_LIST ADD_INCLUDE_DIRS LINK_LIBRARIES)

    cmake_parse_arguments( _SSTCAM_LIBRARY "${_OPTIONS_ARGS}" "${_ONE_VALUE_ARGS}" "${_MULTI_VALUE_ARGS}" ${ARGN} )


    set(LIBTARGET ${PROJECT_NAME}_c)

    #Dealing with optional arguments
    set(_ADD_INCLUDE_DIRS)
    if(_SSTCAM_LIBRARY_ADD_INCLUDE_DIRS)
        set(_ADD_INCLUDE_DIRS ${_SSTCAM_LIBRARY_ADD_INCLUDE_DIRS})
    endif()



    #These are required arguments
    if(_SSTCAM_LIBRARY_TARGET_SRCS AND _SSTCAM_LIBRARY_HEADER_LIST)

        add_library(${LIBTARGET} SHARED ${_SSTCAM_LIBRARY_TARGET_SRCS} ${_SSTCAM_LIBRARY_HEADER_LIST})
        target_include_directories(${LIBTARGET} PUBLIC
            $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include/>
            $<INSTALL_INTERFACE:include/>
            ${_ADD_INCLUDE_DIRS}
            )
        if(_SSTCAM_LIBRARY_LINK_LIBRARIES)
            target_link_libraries(${LIBTARGET} ${_SSTCAM_LIBRARY_LINK_LIBRARIES})
        endif()
        install (TARGETS ${LIBTARGET} EXPORT ${PROJECT_TARGETS} LIBRARY DESTINATION lib)
    else()
        message( FATAL_ERROR "sstcam_library: 'TARGET_SRCS' and 'HEADER_LIST' arguments required." )
    endif()


endmacro()
