# Easier_Contest

Easier_Contest is a Python script designed to streamline your Codeforces contest experience. It automatically organizes your files by creating a directory named after the contest and generating `.cpp` (by default) files for each problem.

## Features

- Automatic directory and file creation: Just pass the link of the contest after the `-l` flag and Easier_Contest will handle the rest.

- Customizable code snippets: You can add your own default code snippet to all the created files by including it in the `snippet.txt` file.

## Getting Started

1. Clone this repository: `git clone https://github.com/Abdulrhman-shaheen/Easier_Contest.git`
2. Navigate to the cloned repository: `cd Easier_Contest`
3. Install the required Python packages: `pip install -r requirements.txt`
4. change the `DIR` variable to the directory where the folder will be created.
5. (Optional) Add your default code snippet to the `snippet.txt` file or delete existing content if not needed.
6. For the first run do `python main.py -c 1` to configure your login credentials.

## Command-Line Arguments

The tool supports several command-line arguments to customize its behavior. Below is a detailed explanation of each:

- `--link` or `-l`: passes link for the contest.

- `--config` or `-c`: Save or edit credentials.

- `--extension` or `-ex`: extension for the files.

## Contributing

This is just a working prototype, if you have any features you would like to add feel free to reach out at abdelrhman.shaheen@ejust.edu.eg
