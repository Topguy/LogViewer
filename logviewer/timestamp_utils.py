import datetime
import re

def parse_timestamp(log_line: str) -> datetime.datetime | None:
    """
    Attempts to parse a timestamp from the beginning of a log line.
    This is a placeholder and should be extended to handle various timestamp formats.
    """
    # Example: YYYY-MM-DD HH:MM:SS.milliseconds or YYYY-MM-DDTHH:MM:SS,SSS
    # This regex is a starting point and might need to be adjusted for specific log formats.
    match = re.match(r'^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[.,]\d{3})', log_line)
    if match:
        try:
            # Try parsing with milliseconds
            return datetime.datetime.strptime(match.group(1).replace('T', ' ').replace(',', '.'), '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            pass
    
    # Add more parsing attempts for other common formats here
    # Example: "MMM DD HH:MM:SS" (e.g., "Jun 28 10:30:00")
    match = re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}', log_line)
    if match:
        try:
            # For this format, we might need to assume the current year or pass it in
            # For simplicity, let's just return None for now if it's not a full datetime
            pass
        except ValueError:
            pass

    return None

def get_timestamp_range(log_lines: list[str]) -> tuple[datetime.datetime | None, datetime.datetime | None]:
    """
    Parses timestamps from a list of log lines and returns the earliest and latest timestamps found.
    """
    min_ts = None
    max_ts = None
    for line in log_lines:
        ts = parse_timestamp(line)
        if ts:
            if min_ts is None or ts < min_ts:
                min_ts = ts
            if max_ts is None or ts > max_ts:
                max_ts = ts
    return min_ts, max_ts

def filter_by_time_range(log_lines: list[str], start_time: datetime.datetime | None, end_time: datetime.datetime | None) -> list[str]:
    """
    Filters log lines to include only those within a specified time range.
    Lines without a parseable timestamp are excluded.
    """
    filtered_lines = []
    for line in log_lines:
        ts = parse_timestamp(line)
        if ts:
            if (start_time is None or ts >= start_time) and \
               (end_time is None or ts <= end_time):
                filtered_lines.append(line)
    return filtered_lines
