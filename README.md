# Grading Tool Assistant
## Overview

The Grading Tool Assistant is a Python script designed to help educators and teaching assistants manage and organize student submissions efficiently. It processes a specified directory containing student submissions, organizing each student's files into individual directories named after each student. Additionally, it automatically unzips any .zip files found within these directories, streamlining the preparation for grading.
Requirements

    Python 3.4 or higher
    Access to a command-line interface (CLI)

## Setup

    Ensure Python 3.4 or higher is installed on your system.
    Download the organize_submissions.py script and place it in a directory separate from the student submissions.
    (Optional) If your student submissions are not yet downloaded, place them in a single directory.

## Usage

    Open a terminal or command prompt.
    Navigate to the directory containing the organize_submissions.py script.
    Run the script with the path to the submissions directory as an argument:

```bash

python organize_submissions.py /path/to/submissions
```
Replace `/path/to/submissions` with the actual path to your directory containing the student submissions.
## Script Features

    Automatic Organization: Moves each student's files into a directory named after the student, based on the name extracted from the file name.
    Zip File Handling: Automatically unzips all .zip files within each student's directory.
    Self-Preservation: The script is designed to ignore and preserve itself, avoiding accidental deletion or movement.

## Notes

    The script assumes the student's name is the first part of the file name, up to the first underscore (_).
    The script is designed to handle .zip files. If other file formats require extraction, additional functionality will need to be added.
    It is recommended to backup your data before running the script as a precaution.

## Contributing

Feedback and contributions are welcome! Please feel free to submit pull requests or open issues with suggestions for improvements.


