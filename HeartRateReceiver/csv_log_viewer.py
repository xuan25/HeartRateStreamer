
import csv
import datetime
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')


class HeartRateMonitor:
    def __init__(self, log_file):
        self.log_file = log_file
        self.timestamps = []
        self.heart_rates = []
        self.csv_file = open(self.log_file, 'r', encoding='utf-8')
        self.csv_reader = csv.DictReader(self.csv_file)
        self.ani = None

    def show(self):
        self.fetch_data()
        self.update_plot()

        self.ani = FuncAnimation(
            plt.gcf(), self.animate, interval=5000, cache_frame_data=False)
        plt.show()

    def fetch_data(self):
        for row in self.csv_reader:
            self.timestamps.append(float(row['timestamp']))
            self.heart_rates.append(float(row['heart_rate']))

    def update_plot(self):
        plt.cla()

        plt.plot(self.timestamps, self.heart_rates)

        plt.xlabel('Time')
        plt.ylabel('Heart Rate')
        plt.title('Heart Rate Monitor')

        plt.xticks(None)
        plt.yticks(None)

        def format_fn(x, pos):
            _ = pos
            return datetime.datetime.fromtimestamp(x).strftime('%H:%M:%S')

        ax = plt.gca()
        ax.xaxis.set_major_formatter(plt.FuncFormatter(format_fn))

        plt.grid(True)

        plt.tight_layout()

    def animate(self, i):
        _ = i

        self.fetch_data()
        self.update_plot()


def main():

    def parse_timestamp_from_file_path(path):
        filename = os.path.basename(path)
        return datetime.datetime.strptime(filename, 'log_%Y-%m-%d_%H-%M-%S.csv')

    latest_log_file = max([os.path.join(LOG_DIR, filename) for filename in os.listdir(
        LOG_DIR) if filename.endswith('.csv')], key=parse_timestamp_from_file_path)

    print(f'Latest log file: {latest_log_file}')

    heartRateMonitor = HeartRateMonitor(latest_log_file)
    heartRateMonitor.show()


if __name__ == '__main__':
    main()
