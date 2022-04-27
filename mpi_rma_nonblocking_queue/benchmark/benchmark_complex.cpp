#include <sstream>
#include <iostream>

#include "rma_nb_queue/rma_nb_queue.h"
extern "C"
{
    #include "mpi_timing/utils.h"
}

extern std::ostringstream l_str;
extern int myrank;
extern mpi_call_counter_t mpi_call_counter;
extern timings_t timings;


bool benchmark_enq_deq_multiple_proc(int size_per_node, int num_of_ops_per_node, MPI_Comm comm, double* result_thrpt) {
    log_("STARTING TEST_ENQ_DEQ_M_PROC\n");
    l_str << "size_per_node: " << size_per_node
          << "\n\tnum_of_ops_per_node: " << num_of_ops_per_node << std::endl;
    log_(l_str);

    val_t value;
    long long start, end;
    double result_time;
    long long start_own, end_own;
    double result_time_own;

    test_result result;
    result.added = 0;
    result.deleted = 0;

    rma_nb_queue_t* queue;
    rma_nb_queue_init(&queue, size_per_node, comm);

    l_str << "n_proc: " << queue->n_proc
          << "\n\tts_offset: " << queue->ts_offset << std::endl;
    log_(l_str);

    if(myrank == MAIN_RANK) {
        check_using_memory_model(queue);
        l_str << "number of procs " << queue->n_proc << std::endl;
        log_(l_str, LOG_PRINT_CONSOLE);
    }

    MPI_Barrier(queue->comm);
    for (int i = 0; i < num_of_ops_per_node/2; ++i) {
        if (enqueue(queue, get_rand(10000)) == CODE_SUCCESS) ++result.added;

        if(USE_DEBUG) {
            l_str << "added " << result.added << std::endl;
            log_(l_str);
            // g_pause();
        }
    }
    if(USE_DEBUG) {
        l_str << "added " << result.added << std::endl;
        log_(l_str, LOG_PRINT_CONSOLE | LOG_PRINT_FILE);
    }
    MPI_Barrier(queue->comm);

    if (myrank == MAIN_RANK) {
        // log_(print(queue));
        start = clock();
    }

    MPI_Barrier(queue->comm);
    start_own = clock();
    for (int i = 0; i < num_of_ops_per_node; ++i) {
        if (get_rand(2)) {
            if (enqueue(queue, get_rand(10000)) == CODE_SUCCESS) ++result.added;
        } else {
            if (dequeue(queue, &value) == CODE_SUCCESS) ++result.deleted;
        }

        if(USE_DEBUG) {
            l_str << "added " << result.added << "\tdeleted " << result.deleted << std::endl;
            log_(l_str);
        }
    }
    end_own = clock();
    if (USE_DEBUG) log_("finished adding/deleting\n", LOG_PRINT_CONSOLE | LOG_PRINT_FILE);
    MPI_Barrier(queue->comm);

    if (myrank == MAIN_RANK) {
        end = clock();
        result_time = ((double)(end - start)) / CLOCKS_PER_SEC;
        // log_(print(queue));
    }

    result_time_own = ((double)(end_own - start_own)) / CLOCKS_PER_SEC;

    for(int i = 0; i < queue->n_proc; ++i) {
        if (i == myrank) {
            l_str << "total added\t" << result.added << ",\tdeleted\t" << result.deleted << std::endl;
            log_(l_str, LOG_PRINT_CONSOLE | LOG_PRINT_FILE);
        }
        MPI_Barrier(queue->comm);
    }

    bool test_result = check_results(queue, result);

    if (myrank == MAIN_RANK) {
        *result_thrpt = calc_throughput(num_of_ops_per_node, queue->n_proc, result_time);
        l_str << "time taken: " << result_time << " s\tthroughput: " << *result_thrpt << " ops/s" << std::endl;
        log_(l_str, LOG_PRINT_CONSOLE | LOG_PRINT_FILE);
    }

    // l_str << print_attributes(queue) << std::endl;
    l_str << "OWN time taken: " << result_time_own << " s\tthroughput: " << calc_throughput(num_of_ops_per_node, queue->n_proc, result_time_own) << " ops/s" << std::endl;
    log_(l_str);

    calc_and_print_total_mpi_calls(queue, &mpi_call_counter);
    calc_and_print_timings(queue, &timings);

    rma_nb_queue_free(queue);
    log_("EXITING TEST_ENQ_DEQ_M_PROC\n");
    return test_result;
}

void benchmark_complex(int size_per_node, int num_of_ops_per_node) {
    log_("STARTING TEST_COMPEX\n");

    MPI_Comm temp_comm;
    int world_rank;
    int world_size;
    int color;

    MPI_Comm_rank(MPI_COMM_WORLD, &world_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &world_size);

    for(int i = 0; i < world_size; ++i) {
        color = 1;
        if (i >= world_rank) color = 0;

        MPI_Comm_split(MPI_COMM_WORLD, color, world_rank, &temp_comm);
        if (i >= world_rank) benchmark_enq_deq_multiple_proc(size_per_node, num_of_ops_per_node, temp_comm, 0);
        MPI_Comm_free(&temp_comm);

        if(world_rank == MAIN_RANK) std::cout << "--------------------------------------------------" << std::endl;
        log_("--------------------------------------------------\n");
        MPI_Barrier(MPI_COMM_WORLD);
    }
    myrank = world_rank;

    log_("EXITING TEST_COMPLEX\n");
}

int main(int argc, char** argv) {
    int size_per_node = 15000;
    int num_of_ops_per_node = 10000;
    int n_proc;
    int test_calls = 0;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &myrank);
    MPI_Comm_size(MPI_COMM_WORLD, &n_proc);

    // srand(time(0) * myrank);
    log_init(myrank);
    // mpi_call_counter_init(&mpi_call_counter, n_proc);

    submit_hostname(MPI_COMM_WORLD);

    benchmark_complex(size_per_node, num_of_ops_per_node);

    // mpi_call_counter_free(&mpi_call_counter);
    log_close();
    MPI_Finalize();
	return 0;
}
