from gradio_client import Client
import os
import json
import argparse

def run_log_processing(log_file_path: str, filter_file_path: str, output_file_path: str = None):
    """
    Processes a log file using a running Gradio application's API.

    Args:
        log_file_path (str): Path to the input log file.
        filter_file_path (str): Path to the JSON filter file.
        output_file_path (str, optional): Path to the output file. 
                                          Defaults to a generated name if not provided.
    """
    # Assuming your Gradio app is running on localhost:7860
    # You might need to change this URL if your app is hosted elsewhere.
    client = Client("http://localhost:7860/")

    print(f"Loading filters from: {filter_file_path}")
    # Call the load_filters function in your Gradio app
    # Gradio client handles file uploads by passing the file path directly.
    loaded_filters = client.predict(
        fn_name="/load_filters", 
        inputs=[filter_file_path]
    )
    print(f"Loaded {len(loaded_filters)} filters.")

    print(f"Applying filters to log file: {log_file_path}")
    # Call the apply_filters function in your Gradio app
    filtered_log_content = client.predict(
        fn_name="/apply_filters",
        inputs=[log_file_path, loaded_filters]
    )
    print("Filters applied.")

    # Determine output file name if not provided
    if output_file_path is None:
        log_file_name = os.path.basename(log_file_path)
        filter_file_name = os.path.basename(filter_file_path)
        
        log_base, log_ext = os.path.splitext(log_file_name)
        filter_base, filter_ext = os.path.splitext(filter_file_name)
        
        output_file_path = f"{log_base}_{filter_base}_filtered.txt"

    # Save the result to the output file
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
