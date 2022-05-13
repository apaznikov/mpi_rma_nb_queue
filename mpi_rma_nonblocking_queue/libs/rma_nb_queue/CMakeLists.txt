get_filename_component(lib_dir ${CMAKE_CURRENT_LIST_DIR} NAME)

file(GLOB SOURCES "*.cpp" "*.c")

add_library(${lib_dir} SHARED ${SOURCES})
add_library(sub::${lib_dir} ALIAS ${lib_dir})
target_include_directories(
        ${lib_dir}
        PUBLIC
        ..
)
target_link_libraries(
        ${lib_dir}
        sub::mpi_timing
        ${MPI_CXX_LIBRARIES}
        ${MPI_C_LIBRARIES}
)