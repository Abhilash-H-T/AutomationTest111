#Parsing the CSC_Iseposture log using python3

import re
from datetime import datetime

# Define the regex pattern to match lines with "Checking rqmt"
checking_pattern = re.compile(
    r'\[(?P<timestamp>[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{3} \d{4})\].+Checking rqmt, \[(?P<requirement>[\w-]+)\]:Mandatory'
)

# Define the regex pattern to match lines with "check result of rqmt"
result_pattern = re.compile(
    r'\[(?P<timestamp>[A-Za-z]{3} [A-Za-z]{3} \d{2} \d{2}:\d{2}:\d{2}\.\d{3} \d{4})\].+check result of rqmt, \[(?P<requirement>[\w-]+)\]:(?P<status>PASSED|FAILED)'
)

# Helper function to parse timestamp
def parse_timestamp(timestamp_str):
    return datetime.strptime(timestamp_str, '%a %b %d %H:%M:%S.%f %Y')


def parse_log(filepath):
    # Open and read the log file
    with open(filepath, 'r') as file:
        log_entries = {}
        for line in file:
            # Check for "Checking rqmt" lines
            checking_match = checking_pattern.search(line)
            if checking_match:
                log_entry = checking_match.groupdict()
                timestamp = log_entry['timestamp']
                requirement = log_entry['requirement']
                log_entries[requirement] = {
                    'timestamp': parse_timestamp(timestamp),
                    'requirement': requirement,
                    'status': 'CHECKING'
                }

            # Check for "check result of rqmt" lines
            result_match = result_pattern.search(line)
            if result_match:
                log_entry = result_match.groupdict()
                timestamp = log_entry['timestamp']
                requirement = log_entry['requirement']
                status = log_entry['status']

                if requirement in log_entries:
                    log_entries[requirement]['status'] = status
                else:
                    log_entries[requirement] = {
                        'timestamp': parse_timestamp(timestamp),
                        'requirement': requirement,
                        'status': status
                    }

    # Sort the log entries by timestamp in descending order
    sorted_log_entries = sorted(log_entries.values(), key=lambda x: x['timestamp'], reverse=True)

    return sorted_log_entries






