# LogViewer Application Design

## 1. Overview

LogViewer is a web-based application built with Python, Gradio, and Pandas that allows users to upload and inspect multiple log files. It provides a merged, time-sorted view of all logs and allows for dynamic filtering with separate filter sets for each file. This helps users analyze log data by including or excluding lines based on text or regular expressions.

## 2. Components

The application consists of three main Python files:

### 2.1. `app.py`

This is the main application file that creates the user interface and handles all user interactions.

*   **UI Structure:** The UI is built using `gradio.Blocks` with the `Soft` theme. It includes:
    *   A file upload component (`gr.File`) for loading multiple log files.
    *   A dropdown (`gr.Dropdown`) to select the log file whose filters you want to manage.
    *   A `gr.DataFrame` to display the merged, filtered, and time-sorted log content in a table with columns for "File", "Timestamp", and "Log Entry".
    *   A section for adding new filters, containing:
        *   A dropdown (`gr.Dropdown`) to select the filter type (Include/Exclude Text, Include/Exclude Regex).
        *   A textbox (`gr.Textbox`) to input the filter pattern, accompanied by a help button (`gr.Button`) that provides a popup with a regex guide.
        *   A checkbox (`gr.Checkbox`) to control case sensitivity for the filter.
        *   An "Add Filter" button (`gr.Button`).
        *   "Save Filters" button (`gr.Button`) to download the current filter set for the selected file as a JSON file.
        *   "Load Filters" button (`gr.UploadButton`) to upload a JSON file and apply saved filters to the selected file.
    *   A section to display and manage active filters for the selected file:
        *   A radio button group (`gr.Radio`) that lists the currently applied filters.
        *   A "Remove Selected Filter" button (`gr.Button`).
        *   "Move Up" and "Move Down" buttons to reorder filters.
    *   A "Save Filtered Log" button (`gr.Button`) to download the currently displayed merged log content.

*   **State Management:**
    *   A `gr.State` object (`files_state`) maintains the application's state. It's a dictionary where keys are filenames and values are dictionaries containing:
        *   `lines`: A list of objects, where each object represents a line and stores its parsed timestamp, the raw content, and the source filename.
        *   `filters`: A list of active filter dictionaries for that file.

*   **Core Logic:**
    *   **`add_file()`:** Handles file uploads. For each line in a new file, it calls `timestamp_utils.parse_timestamp` and stores the result along with the line content in `files_state`.
    *   **`select_file()`:** Triggered when a user selects a file from the dropdown. It updates the UI to show the filters for the selected file.
    *   **`add_filter()`, `remove_filter()`, `move_filter_up()`, `move_filter_down()`:** These functions manage the filter list for the currently selected file.
    *   **`generate_merged_view()`:** This is the main processing function. It iterates through all files in `files_state`, applies the respective filters to each file's lines, combines the filtered lines into a single list, sorts them by timestamp, and returns a Pandas DataFrame for display.
    *   **`update_filter_list()`:** Generates a list of strings from the filter list of the selected file to display it in the UI.
    *   **`save_filters()` & `load_filters()`:** Handle saving and loading of filter sets.
    *   **`save_filtered_log()`:** Saves the content of the DataFrame to a text file.
    *   **`show_regex_help()`:** Displays an informational popup with a guide to using regular expressions.

*   **Event Handling:**
    *   Uploading a file triggers `add_file` and then `generate_merged_view`.
    *   Changing the file selection in the dropdown triggers `select_file` to update the displayed filter list.
    *   Any action that modifies filters (add, remove, move, load) triggers `generate_merged_view` to refresh the log table.

### 2.2. `filter_utils.py`

This module provides the core filtering logic.

*   **`filter_lines()`:** A pure function that takes a list of text lines and applies a single filtering criterion.

### 2.3. `timestamp_utils.py`

This module provides utilities for parsing timestamps from log lines.

*   **`parse_timestamp()`:** Attempts to parse a timestamp from a log line, supporting multiple formats.

### 2.4. `cli_app.py`

This is a command-line interface (CLI) application that interacts with the running `app.py` Gradio service via its API.

*   **Functionality:**
    *   Takes a log file path and a filter JSON file path as arguments.
    *   Uses the `requests` library to send POST requests to the Gradio app's API endpoints.
    *   Saves the filtered log content to an output file.

## 3. User Interaction Flow

1.  The user opens the application in their browser.
2.  The user uploads one or more log files. The application immediately processes them, parses timestamps, and displays a merged, time-sorted view of all log entries in a table.
3.  The filenames appear in a dropdown. The user can select a file from this dropdown to manage its specific filters.
4.  When a file is selected, its associated filters are displayed in the "Applied Filters" list.
5.  To filter a log, the user selects the corresponding file, defines a filter (e.g., "Include Text", "Exclude Regex"), and clicks "Add Filter".
6.  The filter is added to the selected file's filter list, and the main log table automatically updates to reflect the change.
7.  The user can add multiple filters to each file. Filters are applied sequentially.
8.  The user can reorder or remove filters for the selected file, and the view will update accordingly.
9.  The user can save the filter set for a selected file to a JSON file for later use.
10. The user can load a saved filter set and apply it to the selected file.
11. The user can click the "?" button for help with writing regular expressions.
12. The user can save the currently displayed merged and filtered log content to a text file at any time.

This design provides a powerful and interactive way to analyze multiple log files simultaneously in a unified, time-ordered view.
