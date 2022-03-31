cmake_minimum_required(VERSION 3.16)
project(mpi_rma_nb_queue)

set(MPI_CXX_COMPILER "mpicxx")
set(MPI_C_COMPILER "mpicc")

find_package(MPI REQUIRED)

file(GLOB TIMING_SOURCES
        "mpi_rma_nonblocking_queue/mpi_timing/hpctimer.c"
        "mpi_rma_nonblocking_queue/mpi_timing/mpigclock.c"
        "mpi_rma_nonblocking_queue/mpi_timing/utils.c"
)

add_executable(
        enq_deq_multiple_proc
        mpi_rma_nonblocking_queue/rma_nb_queue.cpp
        ${TIMING_SOURCES}
)
target_include_directories(
        enq_deq_multiple_proc
        PUBLIC
        mpi_rma_nonblocking_queue/mpi_timing
        ${MPI_INCLUDE_PATH}
)
target_link_libraries(
        enq_deq_multiple_proc
        ${MPI_CXX_LIBRARIES}
        ${MPI_C_LIBRARIES}
)