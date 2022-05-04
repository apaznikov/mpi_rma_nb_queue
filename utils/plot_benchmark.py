import os
import re
import shutil

import numpy as np
from string import Template
from matplotlib import pyplot as plt

BENCHMARK_LOGS_DIR = './benchmark_enq_deq_multiple_proc_logs'
BENCHMARK_PLOTS_OUT_DIR = './benchmark_enq_deq_multiple_proc_plots'


class BenchmarkLogsParser:
    log_proc_0_file = 'log_proc_0.txt'

    def __init__(self, benchmark_logs_out_dir: str):
        self.ys_metrics_dict = {}
        self.max_n_procs = None
        self.benchmark_logs_out_dir = benchmark_logs_out_dir

    def parse(self):
        self.max_n_procs = len([dir_name for dir_name in os.listdir(self.benchmark_logs_out_dir)])
        self.ys_metrics_dict = {metric: np.zeros(self.max_n_procs) for metric in
                                ['throughput', 'enq_overall', 'enq_hopping', 'deq_overall', 'deq_hopping', 'bcast_overall']}

        for n_proc in range(1, self.max_n_procs + 1):
            self.__parse_n_proc_log_dir(n_proc)

    def __parse_n_proc_log_dir(self, n_proc: int):
        n_proc_0_file_path = os.path.join(self.benchmark_logs_out_dir, str(n_proc), BenchmarkLogsParser.log_proc_0_file)
        with open(n_proc_0_file_path, 'r', encoding='ISO-8859-1') as f:
            n_proc_0_file_data = f.read()

        n_proc_0_file_throughput = n_proc_0_file_data[n_proc_0_file_data.find('rank 0: time taken'):]
        pattern = 'throughput\:\s(\d+)\sops'
        metric_value = int(re.findall(pattern, n_proc_0_file_throughput)[0])
        self.ys_metrics_dict['throughput'][n_proc - 1] = metric_value

        n_proc_0_file_metrics = n_proc_0_file_data[n_proc_0_file_data.find('rank 0: total timings avg'):]
        for metric_name, metric_ys in self.ys_metrics_dict.items():
            if metric_name != 'throughput':
                pattern = f'{metric_name}\:\s(\d+\.\d+)\sms'
                metric_value = float(re.findall(pattern, n_proc_0_file_metrics)[0])
                metric_ys[n_proc - 1] = metric_value


class BenchmarkPlotter:
    linestyle_tuple = [
        ('densely dotted', (0, (1, 1))),

        ('dashed', (0, (5, 5))),
        ('densely dashed', (0, (5, 1))),

        ('dashdotted', (0, (3, 5, 1, 5))),
        ('densely dashdotted', (0, (3, 1, 1, 1)))]

    def __init__(self, max_n_procs: int, ys_metrics_dict: dict, benchmark_plots_out_dir:str):
        self.xs = np.arange(1, max_n_procs + 1, 1)
        self.ys_metrics_dict = ys_metrics_dict
        self.benchmark_plots_out_dir = benchmark_plots_out_dir

        if os.path.isdir(self.benchmark_plots_out_dir):
            shutil.rmtree(self.benchmark_plots_out_dir)
        os.mkdir(self.benchmark_plots_out_dir)

    def save_throughput_plot(self):
        ys = self.ys_metrics_dict['throughput']
        plt.plot(self.xs, ys)
        plt.grid()
        plt.subplots_adjust(left=0.2)
        plt.xticks(self.xs)
        plt.xlabel("Количество процессов")
        plt.ylabel("Пропускная способность (опер/с)")
        plot_path = os.path.join(self.benchmark_plots_out_dir, 'throughput.png')
        plt.savefig(plot_path)
        plt.clf()

    def save_enq_overall_plot(self):
        ys = self.ys_metrics_dict['enq_overall']
        plt.plot(self.xs, ys)
        plt.grid()
        plt.subplots_adjust(left=0.2)
        plt.xticks(self.xs)
        plt.xlabel("Количество процессов")
        plt.ylabel("Время, мс")
        plot_path = os.path.join(self.benchmark_plots_out_dir, 'enq_overall.png')
        plt.savefig(plot_path)
        plt.clf()

    def save_enq_hopping_plot(self):
        ys = self.ys_metrics_dict['enq_hopping']
        plt.plot(self.xs, ys)
        plt.grid()
        plt.subplots_adjust(left=0.2)
        plt.xticks(self.xs)
        plt.xlabel("Количество процессов")
        plt.ylabel("Время, мс")
        plot_path = os.path.join(self.benchmark_plots_out_dir, 'enq_hopping.png')
        plt.savefig(plot_path)
        plt.clf()

    def save_deq_overall_plot(self):
        ys = self.ys_metrics_dict['deq_overall']
        plt.plot(self.xs, ys)
        plt.grid()
        plt.subplots_adjust(left=0.2)
        plt.xticks(self.xs)
        plt.xlabel("Количество процессов")
        plt.ylabel("Время, мс")
        plot_path = os.path.join(self.benchmark_plots_out_dir, 'deq_overall.png')
        plt.savefig(plot_path)
        plt.clf()

    def save_deq_hopping_plot(self):
        ys = self.ys_metrics_dict['deq_hopping']
        plt.plot(self.xs, ys)
        plt.grid()
        plt.subplots_adjust(left=0.2)
        plt.xticks(self.xs)
        plt.xlabel("Количество процессов")
        plt.ylabel("Время, мс")
        plot_path = os.path.join(self.benchmark_plots_out_dir, 'deq_hopping.png')
        plt.savefig(plot_path)
        plt.clf()

    def save_bcast_overall_plot(self):
        ys = self.ys_metrics_dict['bcast_overall']
        plt.plot(self.xs, ys)
        plt.grid()
        plt.subplots_adjust(left=0.2)
        plt.xticks(self.xs)
        plt.xlabel("Количество процессов")
        plt.ylabel("Время, мс")
        plot_path = os.path.join(self.benchmark_plots_out_dir, 'bcast_overall.png')
        plt.savefig(plot_path)
        plt.clf()

    def save_plot_enq_overall_enq_hopping_deq_overall_deq_hopping_bcast_overall(self):
        markers = ["o", "d", "v", "s", "x"]
        i = 0
        for metric_name, metric_ys in self.ys_metrics_dict.items():
            if metric_name != 'throughput':
                plt.plot(self.xs, metric_ys, marker=markers[i], linestyle=BenchmarkPlotter.linestyle_tuple[i][1])
                i += 1
        plt.grid()
        plt.subplots_adjust(left=0.2)
        plt.xticks(self.xs)
        plt.xlabel("Количество процессов")
        plt.ylabel("Время, мс")
        plot_path = os.path.join(self.benchmark_plots_out_dir, 'enq_overall_enq_hopping_deq_overall_deq_hopping_bcast_overall.png')
        plt.legend(loc='upper left')
        plt.savefig(plot_path)
        plt.clf()

    def save_all_plots(self):
        self.save_throughput_plot()
        self.save_enq_overall_plot()
        self.save_enq_hopping_plot()
        self.save_deq_overall_plot()
        self.save_deq_hopping_plot()
        self.save_bcast_overall_plot()
        self.save_plot_enq_overall_enq_hopping_deq_overall_deq_hopping_bcast_overall()


if __name__ == '__main__':
    benchmark_logs_parser = BenchmarkLogsParser(BENCHMARK_LOGS_DIR)
    benchmark_logs_parser.parse()

    max_n_procs = benchmark_logs_parser.max_n_procs
    ys_metrics_dict = benchmark_logs_parser.ys_metrics_dict

    benchmark_plotter = BenchmarkPlotter(max_n_procs, ys_metrics_dict, BENCHMARK_PLOTS_OUT_DIR)
    benchmark_plotter.save_all_plots()
