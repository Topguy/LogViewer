# LogViewer

LogViewer is a versatile tool designed for efficient viewing and filtering of log files. It offers both a user-friendly web interface built with Gradio and a powerful command-line interface (CLI) for automated processing.

## Features

*   **Web Interface (Gradio):**
    *   Upload and display log files.
    *   Apply multiple filters (include/exclude text, include/exclude regex).
    *   Case-sensitive filtering option.
    *   Reorder applied filters to control processing order.
    *   Save and load filter configurations (JSON format).
    *   Download filtered log content.
*   **Command-Line Interface (CLI):**
    *   Process log files using pre-defined filter configurations.
    *   Automate log analysis workflows.

## Installation

To set up LogViewer on your local machine, follow these steps:

### Prerequisites

*   Python 3.8 or higher
*   pip (Python package installer)
*   `venv` (Python's built-in virtual environment module)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/LogViewer.git
    cd LogViewer
    ```
    *(Note: Replace `your-username` with the actual GitHub username once the repository is created.)*

2.  **Create and activate a virtual environment:**
    It's highly recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    # On Linux/macOS:
    source venv/bin/activate
    # On Windows:
    .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running with Docker Compose

Docker Compose provides an easy way to set up and run the LogViewer application in a containerized environment.

#### Prerequisites

*   Docker and Docker Compose installed on your system.

#### Steps

1.  **Build and run the services:**
    Navigate to the root directory of the cloned repository and run:
    ```bash
    docker compose up --build -d
    ```
    This command builds the Docker image (if not already built) and starts the LogViewer service in detached mode.

2.  **Access the Web UI:**
    Open your web browser and navigate to `http://localhost:7860`.

3.  **Using the CLI with Docker Compose:**
    If you are running the web interface via Docker Compose, the CLI tool (`cli_app.py`) needs to connect to the Dockerized service. You will need to modify the `Client` URL in `cli_app.py` to point to the Docker container's exposed port (which is `http://localhost:7860` by default).

    Locate the line `client = Client("http://localhost:7860/")` in `cli_app.py` and ensure it points to the correct address where your Docker container is accessible.

    Then, you can run the CLI as usual:
    ```bash
    python cli_app.py <log_file_path> <filter_file_path> [-o <output_file_path>]
    ```

4.  **Stopping the services:**
    To stop the running Docker containers, use:
    ```bash
    docker compose down
    ```

### Web Interface (Gradio App)

To launch the interactive web interface:

1.  **Start the application:**
    Ensure your virtual environment is activated.
    ```bash
    python app.py
    ```
2.  **Access the UI:**
    Open your web browser and navigate to the URL displayed in your terminal (usually `http://127.0.0.1:7860`).

**How to use:**
*   **Upload Log File:** Click the "Upload Log File" button to select your log file.
*   **Add Filters:** Choose a "Filter Type" (e.g., "Include Text", "Exclude Regex"), enter a "Filter Value", and check "Case Sensitive" if needed. Click "Add Filter".
*   **Manage Filters:** Applied filters will appear in the "Applied Filters" list. You can select a filter and use "Remove Selected Filter", "Move Up", or "Move Down" to adjust them.
*   **Save/Load Filters:** Use "Save Filters" to download your current filter configuration as a JSON file, or "Load Filters (.json)" to upload a previously saved configuration.
*   **Save Filtered Log:** After applying filters, click "Save Filtered Log" to download the processed log content.

### Command-Line Interface (CLI)

To process log files using the CLI, the Gradio web application (`app.py`) **must be running** in the background, as the CLI interacts with its API.

1.  **Ensure the Gradio app is running:**
    Open a separate terminal, activate your virtual environment, and run:
    ```bash
    python app.py
    ```
    Keep this terminal open.

2.  **Run the CLI tool:**
    In a new terminal, activate your virtual environment and use `cli_app.py`:
    ```bash
    python cli_app.py <log_file_path> <filter_file_path> [-o <output_file_path>]
    ```
    *   `<log_file_path>`: The path to the input log file you want to process.
    *   `<filter_file_path>`: The path to a JSON file containing your filter configurations (e.g., `filters.json` saved from the web UI).
    *   `-o <output_file_path>` (optional): The path where the filtered log content will be saved. If not provided, a default name will be generated (e.g., `your_log_filters_filtered.txt`).

**Example:**

```bash
python cli_app.py my_application.log my_filters.json -o processed_log.txt
```

## Filter File Format

Filter configurations are saved and loaded as JSON files. Each filter is an object within a list, with the following structure:

```json
[
  {
    "type": "Include Text",
    "value": "ERROR",
    "case_sensitive": true
  },
  {
    "type": "Exclude Regex",
    "value": "DEBUG|INFO",
    "case_sensitive": false
  }
]
```

*   `type`: Can be "Include Text", "Exclude Text", "Include Regex", or "Exclude Regex".
*   `value`: The string or regex pattern for the filter.
*   `case_sensitive`: A boolean (`true` or `false`) indicating whether the filter should be case-sensitive.