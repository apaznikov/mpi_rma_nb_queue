#include "../libs/rma_nb_queue/rma_nb_queue.h"

void benchmark_queue_init(int argc, char** argv) {
	int data_size_per_node = 7;

	rma_nb_queue_t* queue;
	rma_nb_queue_init(&queue, data_size_per_node, MPI_COMM_WORLD);

	MPI_Barrier(queue->comm);
	for (int i = 0; i < queue->n_proc; ++i) {
		if (i == myrank) {
			log_(print_attributes(queue));
		}
		MPI_Barrier(queue->comm);
	}
	MPI_Barrier(queue->comm);

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

	 benchmark_queue_init(argc, argv);

    // mpi_call_counter_free(&mpi_call_counter);
    log_close();
    MPI_Finalize();
	return 0;
}
