import gradio as gr
import json
from filter_utils import filter_lines

def add_filter(filters, filter_type, filter_value, case_sensitive):
    if filter_value:
        filters.append({"type": filter_type, "value": filter_value, "case_sensitive": case_sensitive})
    return filters, ""

def remove_filter(filters, selected_filter):
    if selected_filter:
        parts = selected_filter.split(" - ")
        if len(parts) == 3:
            filter_type, filter_value, case_str = parts
            case_sensitive = case_str == "Case Sensitive: True"
            for i, f in enumerate(filters):
                if f["type"] == filter_type and f["value"] == filter_value and f["case_sensitive"] == case_sensitive:
                    filters.pop(i)
                    break
    return filters, None

def move_filter_up(filters, selected_filter):
    if selected_filter:
        parts = selected_filter.split(" - ")
        if len(parts) == 3:
            filter_type, filter_value, case_str = parts
            case_sensitive = case_str == "Case Sensitive: True"
            for i, f in enumerate(filters):
                if f["type"] == filter_type and f["value"] == filter_value and f["case_sensitive"] == case_sensitive:
                    if i > 0:
                        filters[i], filters[i-1] = filters[i-1], filters[i]
                    break
    return filters, selected_filter

def move_filter_down(filters, selected_filter):
    if selected_filter:
        parts = selected_filter.split(" - ")
        if len(parts) == 3:
            filter_type, filter_value, case_str = parts
            case_sensitive = case_str == "Case Sensitive: True"
            for i, f in enumerate(filters):
                if f["type"] == filter_type and f["value"] == filter_value and f["case_sensitive"] == case_sensitive:
                    if i < len(filters) - 1:
                        filters[i], filters[i+1] = filters[i+1], filters[i]
                    break
    return filters, selected_filter

def apply_filters(file, filters):
    if file is not None:
        with open(file.name) as f:
            lines = f.readlines()

        if not filters:
            return "".join(lines)

        processed_lines = lines
        for f in filters:
            filter_type = f["type"]
            value = f["value"]
            case = f["case_sensitive"]

            if filter_type == "Include Text":
                processed_lines = filter_lines(processed_lines, include_text=value, case_sensitive=case)
            elif filter_type == "Exclude Text":
                processed_lines = filter_lines(processed_lines, exclude_text=value, case_sensitive=case)
            elif filter_type == "Include Regex":
                processed_lines = filter_lines(processed_lines, include_regex=value, case_sensitive=case)
            elif filter_type == "Exclude Regex":
                processed_lines = filter_lines(processed_lines, exclude_regex=value, case_sensitive=case)

        return "".join(processed_lines)
    return ""

def update_filter_list(filters):
    filter_strings = [f'{f["type"]} - {f["value"]} - Case Sensitive: {f["case_sensitive"]}' for f in filters]
    return gr.update(choices=filter_strings)

def save_filters(filters):
    with open("filters.json", "w") as f:
        json.dump(filters, f)
    return "filters.json"

def load_filters(filter_file):
    if filter_file is not None:
        with open(filter_file.name) as f:
            return json.load(f)
    return []

def save_filtered_log(log_content):
    if log_content:
        with open("filtered_log.txt", "w") as f:
            f.write(log_content)
        return "filtered_log.txt"
    return None

with gr.Blocks(theme=gr.themes.Soft(), css="#log_content textarea { font-family: monospace; }") as demo:
    filters_state = gr.State([])

    gr.Markdown("## Log File Viewer")

    with gr.Row():
        file_input = gr.File(label="Upload Log File")

    gr.Markdown("### Filters")

    with gr.Row():
        filter_type = gr.Dropdown([
            "Include Text", "Exclude Text", "Include Regex", "Exclude Regex"
        ], label="Filter Type")
        filter_value = gr.Textbox(label="Filter Value")
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
    text_output = gr.Textbox(label="Log Content", lines=20, max_lines=1000, interactive=False, elem_id="log_content")

    # Event Handlers
    add_filter_button.click(
        add_filter,
        inputs=[filters_state, filter_type, filter_value, case_sensitive_checkbox],
        outputs=[filters_state, filter_value]
    ).then(
        update_filter_list,
        inputs=filters_state,
        outputs=applied_filters_list
    ).then(
        apply_filters,
        inputs=[file_input, filters_state],
        outputs=text_output
    )

    remove_filter_button.click(
        remove_filter,
        inputs=[filters_state, applied_filters_list],
        outputs=[filters_state, applied_filters_list]
    ).then(
        update_filter_list,
        inputs=filters_state,
        outputs=applied_filters_list
    ).then(
        apply_filters,
        inputs=[file_input, filters_state],
        outputs=text_output
    )

    move_up_button.click(
        move_filter_up,
        inputs=[filters_state, applied_filters_list],
        outputs=[filters_state, applied_filters_list]
    ).then(
        update_filter_list,
        inputs=filters_state,
        outputs=applied_filters_list
    ).then(
        apply_filters,
        inputs=[file_input, filters_state],
        outputs=text_output
    )

    move_down_button.click(
        move_filter_down,
        inputs=[filters_state, applied_filters_list],
        outputs=[filters_state, applied_filters_list]
    ).then(
        update_filter_list,
        inputs=filters_state,
        outputs=applied_filters_list
    ).then(
        apply_filters,
        inputs=[file_input, filters_state],
        outputs=text_output
    )

    save_filters_button.click(
        save_filters,
        inputs=filters_state,
        outputs=gr.File(label="Download Filter File")
    )

    load_filters_file.upload(
        load_filters,
        inputs=load_filters_file,
        outputs=filters_state
    ).then(
        update_filter_list,
        inputs=filters_state,
        outputs=applied_filters_list
    ).then(
        apply_filters,
        inputs=[file_input, filters_state],
        outputs=text_output
    )

    file_input.upload(
        apply_filters,
        inputs=[file_input, filters_state],
        outputs=text_output
    )

    save_filtered_log_button.click(
        save_filtered_log,
        inputs=text_output,
        outputs=gr.File(label="Download Filtered Log")
    )

    # Expose functions as API endpoints for external clients
    demo.api_open(fn=load_filters, api_name="load_filters")
    demo.api_open(fn=apply_filters, api_name="apply_filters")

if __name__ == "__main__":
    demo.launch()
    demo.launch()