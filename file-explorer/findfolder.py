"""
STEP-BY-STEP PROJECT FOLDER EXPLORER (pathlib version)

This script demonstrates:
1) How to correctly locate the project root from a scripts/ folder
2) How to explore a target folder (SelfLearning)
3) How to check for file existence
4) How to search recursively for a file anywhere inside SelfLearning
5) pathlib vs os.path best practices
"""

from pathlib import Path

# --------------------------------------------------
# 1. FILE CHECK FUNCTION (pathlib)
# --------------------------------------------------


def check_file_exists(folder: Path, filename: str) -> bool:
    """Check if a specific file exists directly inside the given folder."""
    return (folder / filename).is_file()


# --------------------------------------------------
# 2. RECURSIVE FILE SEARCH FUNCTION
# --------------------------------------------------


def find_file_recursively(folder: Path, filename: str) -> list[Path]:
    """Find a file anywhere inside the folder (recursive search)."""
    return list(folder.rglob(filename))


# --------------------------------------------------
# 3. MAIN EXPLORATION FUNCTION
# --------------------------------------------------


def explore_projectfolder(project_dir: Path) -> None:
    """Explore the 'SelfLearning' folder inside the project directory."""

    print(f"\nCurrent Project Directory: {project_dir.resolve()}\n")

    # Path to SelfLearning folder
    selflearning_dir = project_dir / "SelfLearning"

    if not selflearning_dir.exists():
        print("Error: 'SelfLearning' folder does NOT exist in this project directory.")
        return

    print("Exploring folder:", selflearning_dir, "\n")

    # Separate files and directories
    files = [p for p in selflearning_dir.iterdir() if p.is_file()]
    directories = [p for p in selflearning_dir.iterdir() if p.is_dir()]

    # Print directories
    print("Directories inside 'SelfLearning':")
    for d in directories:
        print("  -", d.name)

    # Print files
    print("\nFiles inside 'SelfLearning':")
    for f in files:
        print("  -", f.name)

    # Summary
    print("\nSummary:")
    print("  Total items:", len(files) + len(directories))
    print("  Total files:", len(files))
    print("  Total directories:", len(directories))

    # Categorize files by extension
    file_types = {}
    for f in files:
        ext = f.suffix.lower() or "no_extension"
        file_types.setdefault(ext, []).append(f.name)

    print("\nFiles categorized by type:")
    for ext, names in file_types.items():
        label = ext if ext != "no_extension" else "no extension"
        print(f" {label} ({len(names)}):")
        for name in names:
            print("    -", name)

    # File existence check
    filename = input("\nEnter a filename to search for: ")

    if check_file_exists(selflearning_dir, filename):
        print(f"\n✔ '{filename}' exists directly inside 'SelfLearning'.")
    else:
        print(f"\n✘ '{filename}' NOT found directly inside 'SelfLearning'.")

    # Recursive search
    matches = find_file_recursively(selflearning_dir, filename)

    if matches:
        print("\nFound recursively at:")
        for match in matches:
            print("  -", match)
    else:
        print("\nNo recursive matches found.")


# --------------------------------------------------
# 4. ENTRY POINT (pathlib only, no os)
# --------------------------------------------------

if __name__ == "__main__":
    # Get the folder where this script is located (scripts/)
    script_dir = Path(__file__).resolve().parent

    # Get the project root (one level up)
    project_dir = script_dir.parent

    # Explore SelfLearning folder
    explore_projectfolder(project_dir)
