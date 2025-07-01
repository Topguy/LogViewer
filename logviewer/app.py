import gradio as gr
import json
import os
import pandas as pd
from filter_utils import filter_lines
from timestamp_utils import parse_timestamp

def add_file(files, state):
    if files:
        for file in files:
            filename = os.path.basename(file.name)
            if filename not in state:
                with open(file.name) as f:
                    lines = f.readlines()
                
                parsed_lines = []
                for line in lines:
                    parsed_lines.append({
                        "timestamp": parse_timestamp(line),
                        "content": line,
                        "source": filename
                    })
                state[filename] = {"lines": parsed_lines, "filters": []}
    
    file_selector_update = gr.update(choices=list(state.keys()), value=list(state.keys())[0] if state else None)
    selected_file = list(state.keys())[0] if state else None
    
    table_output_update = generate_merged_view(state)
    filter_list_update = update_filter_list(selected_file, state)

    return state, file_selector_update, table_output_update, filter_list_update

def select_file(selected_file, state):
    if selected_file and selected_file in state:
        filter_list_update = update_filter_list(selected_file, state)
        return filter_list_update
    return gr.update(choices=[])

def add_filter(state, selected_file, filter_type, filter_value, case_sensitive):
    if selected_file and filter_value:
        state[selected_file]["filters"].append({"type": filter_type, "value": filter_value, "case_sensitive": case_sensitive})
    return state, ""

def remove_filter(state, selected_file, selected_filter):
    if selected_file and selected_filter:
        parts = selected_filter.split(" - ")
        if len(parts) == 3:
            filter_type, filter_value, case_str = parts
            case_sensitive = case_str == "Case Sensitive: True"
            filters = state[selected_file]["filters"]
            for i, f in enumerate(filters):
                if f["type"] == filter_type and f["value"] == filter_value and f["case_sensitive"] == case_sensitive:
                    filters.pop(i)
                    break
    return state, None

def move_filter_up(state, selected_file, selected_filter):
    if selected_file and selected_filter:
        parts = selected_filter.split(" - ")
        if len(parts) == 3:
            filter_type, filter_value, case_str = parts
            case_sensitive = case_str == "Case Sensitive: True"
            filters = state[selected_file]["filters"]
            for i, f in enumerate(filters):
                if f["type"] == filter_type and f["value"] == filter_value and f["case_sensitive"] == case_sensitive:
                    if i > 0:
                        filters[i], filters[i-1] = filters[i-1], filters[i]
                    break
    return state, selected_filter

def move_filter_down(state, selected_file, selected_filter):
    if selected_file and selected_filter:
        parts = selected_filter.split(" - ")
        if len(parts) == 3:
            filter_type, filter_value, case_str = parts
            case_sensitive = case_str == "Case Sensitive: True"
            filters = state[selected_file]["filters"]
            for i, f in enumerate(filters):
                if f["type"] == filter_type and f["value"] == filter_value and f["case_sensitive"] == case_sensitive:
                    if i < len(filters) - 1:
                        filters[i], filters[i+1] = filters[i+1], filters[i]
                    break
    return state, selected_filter

def generate_merged_view(state):
    all_lines = []
    for filename, data in state.items():
        lines = data["lines"]
        filters = data["filters"]

        processed_lines = lines
        for f in filters:
            filter_type = f["type"]
            value = f["value"]
            case = f["case_sensitive"]
            
            content_lines = [line["content"] for line in processed_lines]

            if filter_type == "Include Text":
                filtered_content = filter_lines(content_lines, include_text=value, case_sensitive=case)
            elif filter_type == "Exclude Text":
                filtered_content = filter_lines(content_lines, exclude_text=value, case_sensitive=case)
            elif filter_type == "Include Regex":
                filtered_content = filter_lines(content_lines, include_regex=value, case_sensitive=case)
            elif filter_type == "Exclude Regex":
                filtered_content = filter_lines(content_lines, exclude_regex=value, case_sensitive=case)
            
            processed_lines = [line for line in processed_lines if line["content"] in filtered_content]

        all_lines.extend(processed_lines)

    if not all_lines:
        return pd.DataFrame(columns=["File", "Timestamp", "Log Entry"])

    # Sort lines by timestamp
    all_lines.sort(key=lambda x: x["timestamp"] if x["timestamp"] is not None else pd.Timestamp.min)

    df = pd.DataFrame(all_lines)
    df["Timestamp"] = df["timestamp"].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(x) else "")
    df = df.rename(columns={"source": "File", "content": "Log Entry"})
    
    return df[["File", "Timestamp", "Log Entry"]]

def update_filter_list(selected_file, state):
    if selected_file and selected_file in state:
        filters = state[selected_file]["filters"]
        filter_strings = [f'{f["type"]} - {f["value"]} - Case Sensitive: {f["case_sensitive"]}' for f in filters]
        return gr.update(choices=filter_strings)
    return gr.update(choices=[])

def save_filters(selected_file, state):
    if selected_file and selected_file in state:
        filters = state[selected_file]["filters"]
        with open(f"{selected_file}_filters.json", "w") as f:
            json.dump(filters, f)
        return f"{selected_file}_filters.json"
    return None

def load_filters(selected_file, state, filter_file):
    if selected_file and filter_file is not None:
        with open(filter_file.name) as f:
            state[selected_file]["filters"] = json.load(f)
    return state

def save_filtered_log(log_data):
    if not log_data.empty:
        log_content = ""
        for index, row in log_data.iterrows():
            log_content += f"[{row['File']}] [{row['Timestamp']}] {row['Log Entry']}"
        
        with open("filtered_log.txt", "w") as f:
            f.write(log_content)
        return "filtered_log.txt"
    return None

def show_regex_help():
    gr.Info("""
    **Regular Expression Quick Guide**

    - `.` : Matches any single character.
    - `*` : Matches the preceding character zero or more times.
    - `+` : Matches the preceding character one or more times.
    - `^` : Matches the start of a line.

 : Matches the end of a line.
    - `|` : Acts as an OR operator (e.g., `error|warn`).
    - `[...]`: Matches any single character within the brackets (e.g., `[aeiou]`).
    - `(...)`: Groups expressions.

    **Example:** `^ERROR.*database` will find lines starting with "ERROR" that also contain "database".
    """)

with gr.Blocks(theme=gr.themes.Soft(), css="#log_content .gr-dataframe { font-family: monospace; } .gradio-toast { max-width: 500px !important; }") as demo:
    files_state = gr.State({})

    gr.Markdown("## Log File Viewer")

    with gr.Row():
        file_input = gr.File(label="Upload Log File(s)", file_count="multiple")
        file_selector = gr.Dropdown(label="Select Log File")

    gr.Markdown("### Filters")

    with gr.Row(elem_id="filter_row"):
        filter_type = gr.Dropdown([
            "Include Text", "Exclude Text", "Include Regex", "Exclude Regex"
        ], label="Filter Type")
        filter_value = gr.Textbox(label="Filter Value", scale=4)
        with gr.Column(scale=0, min_width=50):
            help_button = gr.Button("?", scale=0)
        case_sensitive_checkbox = gr.Checkbox(label="Case Sensitive", value=True)
        with gr.Column(scale=0):
            add_filter_button = gr.Button("Add Filter")
            save_filters_button = gr.Button("Save Filters")
            load_filters_file = gr.UploadButton("Load Filters (.json)", file_types=[".json"])

    with gr.Row():
        applied_filters_list = gr.Radio(label="Applied Filters", interactive=True)
        remove_filter_button = gr.Button("Remove Selected Filter")
        move_up_button = gr.Button("Move Up")
        move_down_button = gr.Button("Move Down")

    with gr.Row():
        save_filtered_log_button = gr.Button("Save Filtered Log")
    
    log_table = gr.DataFrame(headers=["File", "Timestamp", "Log Entry"], interactive=False, elem_id="log_content")

    # Event Handlers
    help_button.click(show_regex_help, inputs=None, outputs=None)
    
    file_input.upload(
        add_file,
        inputs=[file_input, files_state],
        outputs=[files_state, file_selector, log_table, applied_filters_list]
    )

    file_selector.change(
        select_file,
        inputs=[file_selector, files_state],
        outputs=[applied_filters_list]
    ).then(
        generate_merged_view,
        inputs=files_state,
        outputs=log_table
    )

    add_filter_button.click(
        add_filter,
        inputs=[files_state, file_selector, filter_type, filter_value, case_sensitive_checkbox],
        outputs=[files_state, filter_value]
    ).then(
        update_filter_list,
        inputs=[file_selector, files_state],
        outputs=applied_filters_list
    ).then(
        generate_merged_view,
        inputs=files_state,
        outputs=log_table
    )

    remove_filter_button.click(
        remove_filter,
        inputs=[files_state, file_selector, applied_filters_list],
        outputs=[files_state, applied_filters_list]
    ).then(
        update_filter_list,
        inputs=[file_selector, files_state],
        outputs=applied_filters_list
    ).then(
        generate_merged_view,
        inputs=files_state,
        outputs=log_table
    )

    move_up_button.click(
        move_filter_up,
        inputs=[files_state, file_selector, applied_filters_list],
        outputs=[files_state, applied_filters_list]
    ).then(
        update_filter_list,
        inputs=[file_selector, files_state],
        outputs=applied_filters_list
    ).then(
        generate_merged_view,
        inputs=files_state,
        outputs=log_table
    )

    move_down_button.click(
        move_filter_down,
        inputs=[files_state, file_selector, applied_filters_list],
        outputs=[files_state, applied_filters_list]
    ).then(
        update_filter_list,
        inputs=[file_selector, files_state],
        outputs=applied_filters_list
    ).then(
        generate_merged_view,
        inputs=files_state,
        outputs=log_table
    )

    save_filters_button.click(
        save_filters,
        inputs=[file_selector, files_state],
        outputs=gr.File(label="Download Filter File")
    )

    load_filters_file.upload(
        load_filters,
        inputs=[file_selector, files_state, load_filters_file],
        outputs=files_state
    ).then(
        update_filter_list,
        inputs=[file_selector, files_state],
        outputs=applied_filters_list
    ).then(
        generate_merged_view,
        inputs=files_state,
        outputs=log_table
    )

    save_filtered_log_button.click(
        save_filtered_log,
        inputs=log_table,
        outputs=gr.File(label="Download Filtered Log")
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)