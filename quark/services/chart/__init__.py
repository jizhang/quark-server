from datetime import datetime


def get_time_range(start_date: datetime, end_date: datetime):
    return {
        'start_time': start_date.strftime('%Y-%m-%d 00:00:00'),
        'end_time': end_date.strftime('%Y-%m-%d 23:59:59'),
    }
