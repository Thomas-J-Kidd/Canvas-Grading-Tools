import argparse
from pathlib import Path
import zipfile

# Set up argument parsing
parser = argparse.ArgumentParser(description="Unzip and organize student submissions.")
parser.add_argument('submissions_dir', type=str, help='Path to the directory containing the student submissions')

# Parse command line arguments
args = parser.parse_args()

# Convert the submissions directory path from string to Path object
submissions_dir = Path(args.submissions_dir)

# Ensure the submissions directory exists
if not submissions_dir.exists():
    print(f"Directory {submissions_dir} does not exist.")
    exit()

# Iterate over all files in the submissions directory
for file in submissions_dir.iterdir():
    if file.is_file():
        # Extract the student's name (everything before the first underscore)
        name = file.stem.split('_', 1)[0]
        
        # Create a directory for the student if it doesn't exist
        student_dir = submissions_dir / name
        student_dir.mkdir(exist_ok=True)
        
        # Move the file to the student's directory
        file.rename(student_dir / file.name)

# Now, loop through each student directory to unzip files
for student_dir in submissions_dir.iterdir():
    if student_dir.is_dir():
        for file in student_dir.iterdir():
            # Check if the file is a zip file
            if file.suffix == '.zip':
                # Unzip the file
                with zipfile.ZipFile(file, 'r') as zip_ref:
                    zip_ref.extractall(student_dir)
                # Optionally, remove the zip file after extraction
                file.unlink()

print("All files processed.")

