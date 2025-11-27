import pandas as pd
import os
from tkinter import Tk, filedialog

# Function to select a folder using a popup dialog
def select_folder():
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    folder_path = filedialog.askdirectory(title="Select Folder Containing MASTER.txt and ACFTREF.txt")
    if not folder_path:
        print("No folder selected. Exiting.")
        exit()
    return folder_path

# Main processing function
def main():
    # Use a popup dialog to select the folder
    folder_path = select_folder()

    # Construct file paths
    master_file = os.path.join(folder_path, "MASTER.txt")
    acftref_file = os.path.join(folder_path, "ACFTREF.txt")

    # Verify files exist
    if not os.path.isfile(master_file):
        print(f"MASTER.txt not found in {folder_path}. Exiting.")
        exit()
    if not os.path.isfile(acftref_file):
        print(f"ACFTREF.txt not found in {folder_path}. Exiting.")
        exit()

    # Parse MASTER.txt with fixed-width fields
    master_columns = [
        ("N-NUMBER", 1, 5),
        ("SERIAL NUMBER", 7, 36),
        ("MFR MDL CODE", 38, 44),
        ("ENGINE MFR MDL CODE", 46, 50),
        ("YEAR MFR", 52, 55),
        ("TYPE REGISTRANT", 57, 57),
        ("NAME", 59, 108),
        # Add more columns if needed
    ]
    master = pd.read_fwf(
        master_file,
        colspecs=[(start - 1, end) for _, start, end in master_columns],
        names=[name for name, _, _ in master_columns],
        encoding="latin1",
    )

    # Parse ACFTREF.txt with fixed-width fields
    acftref_columns = [
        ("CODE", 1, 7),
        ("MFR", 9, 38),
        ("MODEL", 40, 59),
        ("TYPE AIRCRAFT", 61, 61),
        ("TYPE ENGINE", 63, 64),
        # Add more columns if needed
    ]
    acftref = pd.read_fwf(
        acftref_file,
        colspecs=[(start - 1, end) for _, start, end in acftref_columns],
        names=[name for name, _, _ in acftref_columns],
        encoding="latin1",
    )

    # Count occurrences of each MFR MDL CODE in MASTER.txt
    code_counts = master["MFR MDL CODE"].value_counts().reset_index()
    code_counts.columns = ["CODE", "COUNT"]

    # Join with ACFTREF.txt to decode Make and Model
    priority_data = pd.merge(code_counts, acftref, how="left", on="CODE")

    # Filter columns for the final priority table
    priority_data = priority_data[["CODE", "MFR", "MODEL", "COUNT"]]

    # Sort by COUNT in descending order for priority
    priority_data = priority_data.sort_values(by="COUNT", ascending=False)

    # Save the priority table to a file
    output_file = os.path.join(folder_path, "priority_table.csv")
    priority_data.to_csv(output_file, index=False)
    print(f"Priority table generated and saved to '{output_file}'")

if __name__ == "__main__":
    main()
