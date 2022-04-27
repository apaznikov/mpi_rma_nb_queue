cmake_minimum_required(VERSION 3.19)
project(mpi_rma_nb_queue)

set(MPI_CXX_COMPILER "mpicxx")
set(MPI_C_COMPILER "mpicc")

find_package(MPI REQUIRED)

add_subdirectory(libs)
add_subdirectory(benchmark)