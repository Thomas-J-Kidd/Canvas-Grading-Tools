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
            student_names.add(name)  # Add the student's name to the set
            student_dir = submissions_dir / name
            student_dir.mkdir(exist_ok=True)
            file.rename(student_dir / file.name)

    for student_dir in submissions_dir.iterdir():
        if student_dir.is_dir():
            for file in student_dir.iterdir():
                if file.suffix == '.zip':
                    unzip_file(file, student_dir)
                    file.unlink()  # Optionally remove the zip file after extraction

def create_student_list_csv(student_names, output_path):
    """Create a CSV file with a list of student names, each name in a new row."""
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow('')
        # Write student names sorted alphabetically, each in a new row
        for name in sorted(student_names):
            writer.writerow([name])

def main(submissions_path):
    """Process submissions, starting by checking if the path is a zip file."""
    submissions_path = Path(submissions_path)
    student_names = set()
    
    if submissions_path.is_file() and submissions_path.suffix == '.zip':
        extract_to = submissions_path.parent / submissions_path.stem
        unzip_file(submissions_path, extract_to)
        submissions_dir = extract_to
    elif submissions_path.is_dir():
        submissions_dir = submissions_path
    else:
        print(f"The path {submissions_path} is not a valid directory or zip file.")
        return
    
    organize_submissions(submissions_dir, student_names)
    create_student_list_csv(student_names, submissions_dir / 'student_list.csv')
    print("All submissions have been processed and student list created.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unzip and organize student submissions and create a student list CSV.")
    parser.add_argument('submissions_path', type=str, help='Path to the submissions directory or zip file')
    args = parser.parse_args()

    main(args.submissions_path)
