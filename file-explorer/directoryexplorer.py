import os

# --------------------------------------------------
# 1. FILE CHECK FUNCTION (os.path version)
# --------------------------------------------------


def check_file_exists(path, filename):
    """Check if a specific file exists inside the given directory."""
    full_path = os.path.join(path, filename)  # combine folder path and filename
    return os.path.isfile(full_path)  # returns True if file exists, False otherwise


# --------------------------------------------------
# 2. PROJECT DIRECTORY EXPLORATION FUNCTION
# --------------------------------------------------


def project_directory(path):
    """Explore the directory and display files, directories, and categorized files."""

    # Absolute path
    abs_path = os.path.abspath(path)
    print(f"\nCurrent Project Directory: {abs_path}\n")

    # Lists to store files and directories
    files = []
    directories = []

    # Get all items in the directory
    items = os.listdir(path)

    # Separate files and directories
    for item in items:
        full_path = os.path.join(path, item)
        if os.path.isfile(full_path):
            files.append(item)
        elif os.path.isdir(full_path):
            directories.append(item)

    # Print directories
    print("Directories:")
    for d in directories:
        print("  -", d)

    # Print files
    print("\nFiles:")
    for f in files:
        print("  -", f)

    # Summary
    print("\nSummary:")
    print("  Total items:", len(items))
    print("  Total files:", len(files))
    print("  Total directories:", len(directories))

    # Categorize files by extension using a simple dictionary
    file_types = {}
    for f in files:
        if "." in f:
            ext = f.split(".")[-1].lower()
        else:
            ext = "no_extension"

        if ext not in file_types:
            file_types[ext] = []
        file_types[ext].append(f)

    # Display categorized files
    print("\nFiles categorized by type:")
    for ext in file_types:
        print(f" .{ext} ({len(file_types[ext])} file(s)):")
        for f in file_types[ext]:
            print("     -", f)

    # Ask user to check if a file exists
    print("\nFile Existence Checker")
    filename = input("Enter a filename with file type to check: ")
    if check_file_exists(path, filename):
        print(f"'{filename}' exists in this directory.")
    else:
        print(f"'{filename}' does NOT exist in this directory.")


# --------------------------------------------------
# 3. RUN THE PROGRAM
# --------------------------------------------------
if __name__ == "__main__":
    # Get project root directory (parent of scripts/)
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    project_directory(project_dir)
