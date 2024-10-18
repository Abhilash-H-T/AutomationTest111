#Parsing the CSC_Iseposture log using python3

import re
from datetime import datetime

log_file = '/Users/abht/Desktop/Dart logs for parsing/isepostureAbhi.txt'
Output_file='/Users/abht/Desktop/Dart logs for parsing/output_results.txt'

#rdtydfgg Define the regex pattern to match lines with "Checking rqmt"
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

# Open and read the log file
with open(log_file, 'r') as file:
    log_entries = {}
    for line in file:
        # Check for "Checking rqmt" lines
        checking_match = checking_pattern.search(line)
        if checking_match:
            log_entry = checking_match.groupdict()
            timestamp = log_entry['timestamp']
            requirement = log_entry['requirement']
            log_entries[requirement] = {
                'timestamp': timestamp,
                'requirement': requirement,
                'status': 'CHECKING'
            }

        # Check for "check result of rqmt" lines
        result_match = result_pattern.search(line)
        if result_match:
            log_entry = result_match.groupdict()
            timestamp = log_entry['timestamp']
            requirement = log_entry['requirement']
            status = result_match.group('status')
            if requirement in log_entries:
                log_entries[requirement]['status'] = status
            else:
                log_entries[requirement] = {
                    'timestamp': timestamp,
                    'requirement': requirement,
                    'status': status
                }

# Sort the log entries by timestamp in descending order
sorted_log_entries = sorted(log_entries.values(), key=lambda x: parse_timestamp(x['timestamp']), reverse=True)

# Print the extracted information

with open(Output_file, 'w') as output:
    for entry in sorted_log_entries:
        output.write(f"Timestamp: {entry['timestamp']}\n")
        output.write(f"Checking requirement: [{entry['requirement']}]:Mandatory\n")
        output.write(f"Result: [{entry['requirement']}]:{entry['status']}\n")
        output.write("--------------------------------------------------------------------\n")