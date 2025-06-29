# LogViewer Application Design

## 1. Overview

LogViewer is a web-based application built with Python and Gradio that allows users to upload and inspect log files. It provides dynamic filtering capabilities to help users analyze log data by including or excluding lines based on text or regular expressions.

## 2. Components

The application consists of two main Python files:

### 2.1. `app.py`

This is the main application file that creates the user interface and handles all user interactions.

*   **UI Structure:** The UI is built using `gradio.Blocks` with the `Soft` theme. It includes:
    *   A file upload component (`gr.File`) for loading log files.
    *   A large, non-interactive textbox (`gr.Textbox`) to display the processed log content.
    *   A section for adding new filters, containing:
        *   A dropdown (`gr.Dropdown`) to select the filter type (Include/Exclude Text, Include/Exclude Regex).
        *   A textbox (`gr.Textbox`) to input the filter pattern.
        *   A checkbox (`gr.Checkbox`) to control case sensitivity for the filter.
        *   An "Add Filter" button (`gr.Button`).
        *   "Save Filters" button (`gr.Button`) to download the current filter set as a JSON file.
        *   "Load Filters" button (`gr.UploadButton`) to upload a JSON file and apply saved filters.
    *   A section to display and manage active filters:
        *   A radio button group (`gr.Radio`) that lists the currently applied filters, showing their type, value, and case sensitivity.
        *   A "Remove Selected Filter" button (`gr.Button`).
        *   "Move Up" button (`gr.Button`) to move the selected filter up in the list.
        *   "Move Down" button (`gr.Button`) to move the selected filter down in the list.
    *   A "Save Filtered Log" button (`gr.Button`) to download the currently displayed filtered log content.

*   **State Management:**
    *   A `gr.State` object (`filters_state`) is used to maintain the list of active filters as a list of dictionaries. Each dictionary represents a single filter.

*   **Core Logic:**
    *   **`add_filter()`:** Adds a new filter dictionary to the `filters_state` list.
    *   **`remove_filter()`:** Removes a filter from the `filters_state` list based on the user's selection.
    *   **`move_filter_up()`:** Moves the selected filter up in the `filters_state` list.
    *   **`move_filter_down()`:** Moves the selected filter down in the `filters_state` list.
    *   **`apply_filters()`:** This is the main processing function. It reads the uploaded file and applies the sequence of filters stored in `filters_state` by calling the `filter_lines` utility function for each filter.
    *   **`update_filter_list()`:** Generates a list of strings from the `filters_state` list to display it in the UI.
    *   **`save_filters()`:** Saves the current `filters_state` to a JSON file.
    *   **`load_filters()`:** Loads filters from a JSON file into `filters_state`.
    *   **`save_filtered_log()`:** Saves the current content of the log display to a text file.

*   **Event Handling:**
    *   Uploading a file triggers `apply_filters`.
    *   Clicking "Add Filter" triggers `add_filter`, then `update_filter_list`, and finally `apply_filters`.
    *   Clicking "Remove Selected Filter" triggers `remove_filter`, then `update_filter_list`, and finally `apply_filters`.
    *   Clicking "Move Up" triggers `move_filter_up`, then `update_filter_list`, and finally `apply_filters`.
    *   Clicking "Move Down" triggers `move_filter_down`, then `update_filter_list`, and finally `apply_filters`.
    *   Clicking "Save Filters" triggers `save_filters`.
    *   Uploading a file to "Load Filters" triggers `load_filters`, then `update_filter_list`, and finally `apply_filters`.
    *   Clicking "Save Filtered Log" triggers `save_filtered_log`.

*   **API Endpoints:**
    *   `load_filters`: Exposed via `gr.API` to allow external clients to load filter sets.
    *   `apply_filters`: Exposed via `gr.API` to allow external clients to apply filters to log content.

### 2.2. `filter_utils.py`

This module provides the core filtering logic.

*   **`filter_lines()`:** A pure function that takes a list of text lines and applies a single filtering criterion (e.g., include text, exclude regex). It handles both plain text and regular expression matching, with an option for case sensitivity. It returns a new list of filtered lines.

### 2.3. `timestamp_utils.py`

This module provides utilities for parsing and filtering log lines based on timestamps.

*   **`parse_timestamp()`:** Attempts to parse a timestamp from a log line. Designed to be extensible for various timestamp formats.
*   **`get_timestamp_range()`:** Extracts the earliest and latest timestamps from a list of log lines.
*   **`filter_by_time_range()`:** Filters log lines to include only those within a specified time range, based on parsed timestamps.

### 2.4. `cli_app.py`

This is a command-line interface (CLI) application that interacts with the running `app.py` Gradio service via its API.

*   **Functionality:**
    *   Takes a log file path and a filter JSON file path as arguments.
    *   Optionally takes an output file path; otherwise, it generates one.
    *   Uses `gradio_client` to call the `load_filters` and `apply_filters` API endpoints of the Gradio app.
    *   Saves the filtered log content to the specified output file.

## 3. User Interaction Flow

1.  The user opens the application in their browser.
2.  The user uploads a log file using the file upload component. The log content is immediately displayed.
3.  To filter the log, the user selects a filter type, enters a value, and clicks "Add Filter".
4.  The filter is added to the "Applied Filters" list, and the log view is automatically updated to reflect the new filter.
5.  The user can add multiple filters sequentially. Each new filter is applied to the result of the previous ones.
6.  To remove a filter, the user selects it from the "Applied Filters" radio group.
7.  The user then clicks the "Remove Selected Filter" button.
8.  The filter is removed from the list, and the log view is updated to reflect the change.
9.  The user can reorder filters by selecting a filter and clicking "Move Up" or "Move Down" buttons.
10. The user can save the current set of filters by clicking the "Save Filters" button, which will prompt a file download.
11. The user can load a previously saved set of filters by clicking the "Load Filters" button and selecting a JSON file.
12. The user can save the currently displayed filtered log content by clicking the "Save Filtered Log" button, which will prompt a file download.

This design allows for a flexible and interactive way to analyze log files by building a chain of filters.
