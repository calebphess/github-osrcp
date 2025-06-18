# GitHub OSRCP
GitHub Open Source Repository Collection Platform

## About
GitHub OSRCP is a platform designed to collect a list of contributors to open-source repositories hosted on GitHub. The script reads a CSV file of GitHub repositories, fetches all merged pull requests on the `main` branch for each repo, collects unique contributor usernames, and writes them (with profile URLs) to a CSV file.

### How It Works

The main script, `github-osrcp.py`, extracts unique contributors from merged pull requests across multiple GitHub repositories.

# Getting Started
## Prerequisites
- Python 3.12 (tested with python 3.12.11)
- (recommended) Conda/Miniconda
- GitHub Personal Access Token (PAT) with `repo` scope for public repositories
  - [Create GitHub PAT](https://github.com/settings/personal-access-tokens)
  - Make sure it has access to "Public repositories"
- A list of public repositories you want to collect contributors from, stored in a text file 
  - One repository per line, e.g., `username/repo`
  - See `example_repos.csv` for an example

## Installation
1. Clone the repository:
    ```bash
    git clone git@github.com:calebphess/github-osrcp.git
    cd github-osrcp
    ```
2. Create a virtual environment (optional but recommended):
    ```bash
    conda create -n github-osrcp python=3.12
    conda activate github-osrcp
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
```bash
python github-osrcp.py [<csv_file_path>] [-v] [-o <output_path>]
```

- `<csv_file_path>` (optional): Path to a CSV file containing a list of public GitHub repositories (one per line, in `owner/repo` format). If not provided, the script defaults to `repos.csv` in the current directory.
- `-v`: Enable verbose output (prints merged PR details for each repository).
- `-o <output_path>`: Specify output file or directory for the contributors CSV (default: `./contributors.csv`).