import os
import json
import argparse
import requests

def run_log_processing(log_file_path: str, filter_file_path: str, output_file_path: str = None):
    """
    Processes a log file using a running Gradio application's API.

    Args:
        log_file_path (str): Path to the input log file.
        filter_file_path (str): Path to the JSON filter file.
        output_file_path (str, optional): Path to the output file. 
                                          Defaults to a generated name if not provided.
    """
    base_url = "http://localhost:7860"

    print(f"Loading filters from: {filter_file_path}")
    with open(filter_file_path, 'r') as f:
        filters = json.load(f)

    print(f"Applying filters to log file: {log_file_path}")
    with open(log_file_path, 'r') as f:
        log_content = f.read()

    response = requests.post(f"{base_url}/api/apply_filters/", json={
        "data": [
            {"path": log_file_path},
            filters
        ]
    })
    response.raise_for_status()
    filtered_log_content = response.json()['data'][0]
    print("Filters applied.")

    if output_file_path is None:
        log_file_name = os.path.basename(log_file_path)
        filter_file_name = os.path.basename(filter_file_path)
        
        log_base, log_ext = os.path.splitext(log_file_name)
        filter_base, filter_ext = os.path.splitext(filter_file_name)
        
        output_file_path = f"{log_base}_{filter_base}_filtered.txt"

    with open(output_file_path, "w") as f:
        f.write(filtered_log_content)

    print(f"Filtered log saved to: {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process log files using a Gradio API.")
    parser.add_argument("log_file", help="Path to the input log file.")
    parser.add_argument("filter_file", help="Path to the JSON filter file.")
    parser.add_argument("-o", "--output_file", help="Optional: Path to the output file. Defaults to a generated name.")

    args = parser.parse_args()

    run_log_processing(args.log_file, args.filter_file, args.output_file)
