import datetime
import re

def parse_timestamp(log_line: str) -> datetime.datetime | None:
    """
    Attempts to parse a timestamp from the beginning of a log line.
    This function supports multiple timestamp formats.
    """
    # Format 1: YYYY-MM-DD HH:MM:SS.milliseconds or YYYY-MM-DDTHH:MM:SS,SSS
    match = re.match(r'^(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}[.,]\d{3})', log_line)
    if match:
        try:
            return datetime.datetime.strptime(match.group(1).replace('T', ' ').replace(',', '.'), '%Y-%m-%d %H:%M:%S.%f')
        except ValueError:
            pass

    # Format 2: "MMM DD HH:MM:SS" (e.g., "Jun 29 14:22:27")
    match = re.match(r'^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}', log_line)
    if match:
        try:
            # This format doesn't have a year, so we assume the current year.
            current_year = datetime.datetime.now().year
            timestamp_str = f"{current_year} {match.group(0)}"
            return datetime.datetime.strptime(timestamp_str, '%Y %b %d %H:%M:%S')
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
