import csv
import os
import datetime

CSV_LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')

class CSVLogger:

    def __init__(self, log_file):
        self.log_file = log_file

        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        with open(self.log_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'heart_rate'])

    def write(self, timestamp, heart_rate):
        with open(self.log_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, heart_rate])

    @staticmethod
    def create_logger_from_date_time(date_time: datetime.datetime):
        date_time_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')
        log_file = os.path.join(CSV_LOG_DIR, f'log_{date_time_str}.csv')
        return CSVLogger(log_file)
