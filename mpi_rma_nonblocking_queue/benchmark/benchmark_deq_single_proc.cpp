#include <sstream>

#include "rma_nb_queue/rma_nb_queue.h"
extern "C"
{
#include "mpi_timing/utils.h"
}

extern std::ostringstream l_str;
extern int myrank;

void benchmark_deq_single_proc(int argc, char** argv) {
	int op_res;
	int size_per_node = 50;
	int num_of_enqs = 10;
	int num_of_deqs = 10;
	int max_value = 1000;
	int value;

	rma_nb_queue_t* queue;
	rma_nb_queue_init(&queue, size_per_node, MPI_COMM_WORLD);

	log_(print_attributes(queue));

	MPI_Barrier(queue->comm);
	for (int i = 0; i < num_of_enqs; ++i) {
		// value = rand() % max_value;
		value = get_rand(max_value);
		op_res = enqueue(queue, value);
		if (op_res == CODE_SUCCESS) {
			l_str << "added " << value << std::endl;
		} else {
			l_str << "failed to add " << value << ", code " << op_res << std::endl;
		}
		log_(l_str);
	}
	MPI_Barrier(queue->comm);

	log_(print(queue));
	log_(print_attributes(queue));

	MPI_Barrier(queue->comm);
	for (int i = 0; i < num_of_deqs; ++i) {
		op_res = dequeue(queue, &value);
		if (op_res == CODE_SUCCESS) {
			l_str << "deleted " << value << std::endl;
		} else {
			l_str << "failed to delete, code " << op_res << std::endl;
		}
		log_(l_str);
	}
	MPI_Barrier(queue->comm);

	log_(print(queue));
	log_(print_attributes(queue));

	rma_nb_queue_free(queue);
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

    benchmark_deq_single_proc(argc, argv);

    log_close();
    MPI_Finalize();
	return 0;
}
