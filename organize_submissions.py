import argparse
from pathlib import Path
import zipfile
import csv

def unzip_file(zip_path, extract_to):
    """Unzip a file to the specified location."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted {zip_path} to {extract_to}")

def organize_submissions(submissions_dir, student_names):
    """Organize and unzip submissions in the given directory."""
    for file in submissions_dir.iterdir():
        if file.is_file():
            name = file.stem.split('_', 1)[0]
            student_names.add(name)
            student_dir = submissions_dir / name
            student_dir.mkdir(exist_ok=True)
            file.rename(student_dir / file.name)

    for student_dir in submissions_dir.iterdir():
        if student_dir.is_dir():
            for file in student_dir.iterdir():
                if file.suffix == '.zip':
                    unzip_file(file, student_dir)
                    file.unlink()

def create_student_list_csv(student_names, output_path):
    """Create a CSV file with a list of student names, each name in a new row."""
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for name in sorted(student_names):
            writer.writerow([name])

def get_unique_dirname(path):
    """Generate a unique directory name if the specified path exists."""
    if not path.exists():
        return path
    version = 1
    while True:
        new_path = Path(f"{path}_{version}")
        if not new_path.exists():
            return new_path
        version += 1

def main(submissions_path, new_location=None):
    """Process submissions, checking if the path is a zip file and handling the output location."""
    submissions_path = Path(submissions_path)
    student_names = set()

    if submissions_path.is_file() and submissions_path.suffix == '.zip':
        if new_location:
            extract_to = get_unique_dirname(Path(new_location))
        else:
            extract_to = get_unique_dirname(submissions_path.parent / submissions_path.stem)
        extract_to.mkdir(exist_ok=True)
        unzip_file(submissions_path, extract_to)
        submissions_dir = extract_to
    elif submissions_path.is_dir():
        submissions_dir = get_unique_dirname(Path(submissions_path))
        submissions_dir.mkdir(exist_ok=True)
    else:
        print(f"The path {submissions_path} is not a valid directory or zip file.")
        return
    
    organize_submissions(submissions_dir, student_names)
    create_student_list_csv(student_names, submissions_dir / 'student_list.csv')
    print(f"All submissions have been processed and student list created in {submissions_dir}.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unzip, organize student submissions, and create a student list CSV, with unique output directory handling.")
    parser.add_argument('submissions_path', type=str, help='Path to the submissions directory or zip file')
    parser.add_argument('new_location', nargs='?', type=str, help='Optional new location and name for the folder, with unique naming to avoid overwrites')
    args = parser.parse_args()

    main(args.submissions_path, args.new_location)
