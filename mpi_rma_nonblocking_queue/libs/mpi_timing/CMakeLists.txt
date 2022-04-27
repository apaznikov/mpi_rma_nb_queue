get_filename_component(lib_dir ${CMAKE_CURRENT_LIST_DIR} NAME)

file(GLOB SOURCES hpctimer.c mpigclock.c utils.c)

set_source_files_properties(${SOURCES} PROPERTIES LANGUAGE C)

add_library(${lib_dir} SHARED ${SOURCES})
add_library(sub::${lib_dir} ALIAS ${lib_dir})
target_link_libraries(
        ${lib_dir}
        ${MPI_CXX_LIBRARIES}
        ${MPI_C_LIBRARIES}
)