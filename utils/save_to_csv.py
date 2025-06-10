import pandas as pd
from tabulate import tabulate

def save_to_csv(data, filename):
    """Save structured data to CSV file with proper error handling."""
    df = pd.DataFrame(data)

    # Ensure timestamp column exists
    if "Timestamp" not in df.columns:
        df["Timestamp"] = pd.Timestamp.now()

    # Sort data by timestamp for consistency
    df.sort_values(by="Timestamp", ascending=False, inplace=True)

    try:
        df.to_csv(filename, index=False, mode='w', encoding='utf-8', errors='replace')
        print(f"\n✅ Data saved in '{filename}'\n")
    except PermissionError:
        print(f"\n❌ Permission denied: Unable to write to '{filename}'. Close the file if it's open and check permissions.\n")
    except Exception as e:
        print(f"\n❌ Error saving data to '{filename}': {e}\n")

def show_sample_data(data, sample_size=5):
    """Print sample data in a tabulated format."""
    df = pd.DataFrame(data).head(sample_size)
    print(tabulate(df, headers="keys", tablefmt="grid"))
