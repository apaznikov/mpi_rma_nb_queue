import os
import shutil
from string import Template

MAX_N_PROCS = 12
PROGRAM_FULL_PATH = '/media/denis/Seagate/Projects/mpi_rma_nb_queue/mpi_rma_nonblocking_queue/cmake-build-release/benchmark/benchmark_enq_deq_multiple_proc'
BENCHMARK_LOGS_OUT_DIR = './benchmark_enq_deq_multiple_proc_logs'


class BenchmarkCollector:
    mpi_cmd_template = Template('mpirun -np $n_procs $program_path')

    def __init__(self, max_n_procs: int, program_path: str, benchmark_logs_out_dir: str):
        self.max_n_procs = max_n_procs
        self.program_path = program_path
        self.benchmark_logs_out_dir = benchmark_logs_out_dir

    def __prepare_benchmark_logs_dir(self):
        if os.path.isdir(self.benchmark_logs_out_dir):
            shutil.rmtree(self.benchmark_logs_out_dir)
        os.mkdir(self.benchmark_logs_out_dir)

    def __run_mpi_program(self, n_procs: int) -> int:
        mpi_cmd = BenchmarkCollector.mpi_cmd_template.substitute(n_procs=n_procs, program_path=self.program_path)
        return_code = os.system(mpi_cmd)
        return return_code

    def __collect_benchmark_logs(self):
        os.chdir(self.benchmark_logs_out_dir)
        for n_procs in range(1, self.max_n_procs + 1):
            n_procs_dir = f'{n_procs}'
            os.mkdir(n_procs_dir)
            os.chdir(n_procs_dir)
            return_code = self.__run_mpi_program(n_procs)
            if return_code != 0:
                print(f'WARNING! mpi program with procs={n_procs} returned {return_code}')
            os.chdir('..')

    def run(self):
        self.__prepare_benchmark_logs_dir()
        self.__collect_benchmark_logs()


if __name__ == '__main__':
    benchmark_collector = BenchmarkCollector(MAX_N_PROCS, PROGRAM_FULL_PATH, BENCHMARK_LOGS_OUT_DIR)
    benchmark_collector.run()