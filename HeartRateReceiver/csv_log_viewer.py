import csv
import datetime
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')

SMOOTHING_FACTOR = 0.9

HEART_RATE_THRESHOLD = 130

class HeartRateFetcher:

    def __init__(self, log_file):
        self.log_file = log_file

        self.timestamps = []
        self.heart_rates = []
        self.heart_rates_smoothed = []
        self.time_above_threshold = []

        self.csv_file = open(self.log_file, 'r', encoding='utf-8')
        self.csv_reader = csv.DictReader(self.csv_file)
        self.last_timestamp = 0

    def fetch_data(self):
        extend_timestamps = []
        extend_heart_rates = []
        extend_heart_rates_smoothed = []
        extend_time_above_threshold = []

        for row in self.csv_reader:

            timestamp = float(row['timestamp'])

            if timestamp <= self.last_timestamp:
                continue
            self.last_timestamp = timestamp

            timestamp = datetime.datetime.fromtimestamp(
                timestamp).strftime('%Y-%m-%dT%H:%M:%S%z')
            heart_rate = float(row['heart_rate'])

            self.timestamps.append(timestamp)
            self.heart_rates.append(heart_rate)

            extend_timestamps.append(timestamp)
            extend_heart_rates.append(heart_rate)

            # exponential moving average
            if len(self.heart_rates_smoothed) < 1:
                heart_rate_smoothed = heart_rate
                self.heart_rates_smoothed.append(heart_rate_smoothed)
                extend_heart_rates_smoothed.append(heart_rate_smoothed)
            else:
                weight = SMOOTHING_FACTOR
                heart_rate_smoothed = self.heart_rates_smoothed[-1] * \
                    weight + (1 - weight) * self.heart_rates[-1]
                self.heart_rates_smoothed.append(heart_rate_smoothed)
                extend_heart_rates_smoothed.append(heart_rate_smoothed)

            last_time_above_threshold = self.time_above_threshold[-1] if len(self.time_above_threshold) > 0 else 0.0
            if heart_rate > HEART_RATE_THRESHOLD:
                self.time_above_threshold.append(last_time_above_threshold + (5.0 / 60))
                extend_time_above_threshold.append(last_time_above_threshold + (5.0 / 60))
            else:
                self.time_above_threshold.append(last_time_above_threshold)
                extend_time_above_threshold.append(last_time_above_threshold)

        return extend_timestamps, extend_heart_rates, extend_heart_rates_smoothed, extend_time_above_threshold


class HeartRateMonitor:

    def __init__(self, log_file):
        self.heartRateFetcher = HeartRateFetcher(log_file)
        self.app = None
    
    def run(self):
        self.heartRateFetcher.fetch_data()
        
        self.app = dash.Dash(__name__, title='Heart Rate Monitor', update_title=None)
        self.app.layout = html.Div([
            dcc.Graph(id='graph', figure={
                'data': [
                    {'x': self.heartRateFetcher.timestamps, 'y': self.heartRateFetcher.heart_rates,
                        'type': 'scatter', 'mode': 'lines', 'name': 'Heart Rate'},
                    {'x': self.heartRateFetcher.timestamps, 'y': self.heartRateFetcher.heart_rates_smoothed,
                        'type': 'scatter', 'mode': 'lines', 'name': 'Smoothed Heart Rate'}
                ],
                'layout': {
                    'title': 'Real-time Heart Rate',
                    'xaxis': {'title': 'Time'},
                    'yaxis': {'title': 'Heart Rate'},
                    'showlegend': True,
                }},
                animate=True),
            dcc.Graph(id='graph2', figure={
                'data': [
                    {'x': self.heartRateFetcher.timestamps, 'y': self.heartRateFetcher.time_above_threshold,
                        'type': 'scatter', 'mode': 'lines', 'name': 'Time Above Threshold'},
                ],
                'layout': {
                    'title': f'Estimated Duration Above Threshold ({HEART_RATE_THRESHOLD})',
                    'xaxis': {'title': 'Duration'},
                    'yaxis': {'title': 'Minutes'},
                    'showlegend': True,
                }},
                animate=True),
            dcc.Interval(id="interval")
        ])

        self.app.callback(
            [
                Output('graph', 'extendData'),
                Output('graph2', 'extendData'),
            ],
            [
                Input('interval', 'n_intervals')
            ]
        )(self.update_graphs)

        self.app.run()

    def update_graphs(self, n_intervals):
        _ = n_intervals
        extend_timestamps, extend_heart_rates, extend_heart_rates_smoothed, extend_time_above_threshold = self.heartRateFetcher.fetch_data()
        return ({
            'x': [extend_timestamps, extend_timestamps],
            'y': [extend_heart_rates, extend_heart_rates_smoothed]
        }), ({
            'x': [extend_timestamps],
            'y': [extend_time_above_threshold]
        })


def main():

    # find latest log file
    def parse_timestamp_from_file_path(path):
        try:
            filename = os.path.basename(path)
            return datetime.datetime.strptime(filename, 'log_%Y-%m-%d_%H-%M-%S.csv')
        except ValueError:
            return datetime.datetime.min

    latest_log_file = max([os.path.join(LOG_DIR, filename) for filename in os.listdir(
        LOG_DIR) if filename.endswith('.csv')], key=parse_timestamp_from_file_path)

    print(f'Latest log file: {latest_log_file}')

    heartRateMonitor = HeartRateMonitor(latest_log_file)
    heartRateMonitor.run()


if __name__ == '__main__':
    main()
