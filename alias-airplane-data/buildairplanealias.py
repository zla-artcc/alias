import pandas as pd
from tkinter import Tk, filedialog

# Function to load data from a CSV file
def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None

# Function to determine TEC based on Engine Type
def determine_tec(engine_type):
    if engine_type == "Piston":
        return "PQ"
    elif engine_type in ["Turboprop", "Turboshaft"]:
        return "M"
    elif engine_type == "Jet":
        return "J"
    else:
        return "n/a"

# Function to validate and extract SRS category
def validate_srs(srs_value):
    valid_values = ["III", "II", "I"]
    if srs_value in valid_values:
        return srs_value
    return ""

# Function to create commands for .type output
# Ensures only the first occurrence of each Type is used
def create_commands(df):
    if df is None:
        return []
    commands = []
    seen_types = set()

    # Define relevant columns
    relevant_columns = ['Manufacturer', 'Model', 'Type', 'Class', 'Engine Type', 'Engine Number', 
                        'FAA Weight', 'CWT', 'SRS Category', 'ADG']
    
    # Ensure only available columns are used
    available_columns = [col for col in relevant_columns if col in df.columns]
    missing_columns = set(relevant_columns) - set(available_columns)
    
    if missing_columns:
        print(f"Warning: Missing columns: {', '.join(missing_columns)}")
    
    df = df[available_columns]

    for _, row in df.iterrows():
        if row['Type'] in seen_types:
            continue
        seen_types.add(row['Type'])
        tec_value = determine_tec(row.get('Engine Type', 'n/a'))
        srsvalue = validate_srs(row.get('SRS Category', ''))
        adgvalue = row['ADG'] if 'ADG' in df.columns and pd.notna(row['ADG']) else ''
        command = (f".{row.get('Type', 'n/a')} .MSG ZLA_ISR *** "
                   f"MFR: {row.get('Manufacturer', 'n/a')} | "
                   f"MDL: {row.get('Model', 'n/a')} | "
                   f"FAA Wake: {row.get('FAA Weight', 'n/a')} | "
                   f"CWT: {row.get('CWT', 'n/a')} | "
                   f"SRS: {srsvalue} | "
                   f"ADG: {adgvalue} | "
                   f"TEC: {tec_value} | "
                   f"ENG NUM: {row.get('Engine Number', 'n/a')} | "
                   f"Class: {row.get('Class', 'n/a')}")
        commands.append(command)
    return commands

# Main function to load CSV and generate commands
def main():
    # Create a Tkinter root window and hide it
    root = Tk()
    root.withdraw()

    # Open file dialog to select CSV file
    print("Select the CSV file to load:")
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        print("No file selected. Exiting.")
        return

    df = load_csv(file_path)
    commands = create_commands(df)

    # Open file dialog to save the output file
    print("Select where to save the commands file:")
    output_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not output_file:
        print("No save location selected. Exiting.")
        return

    # Save commands to the selected file
    try:
        with open(output_file, "w", encoding="utf-8") as file:
            file.write("\n".join(commands))
        print(f"Commands generated and saved to {output_file}")
    except Exception as e:
        print(f"Error saving commands: {e}")

if __name__ == "__main__":
    main()
