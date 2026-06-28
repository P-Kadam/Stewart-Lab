import pandas as pd
from pathlib import Path

def combine_data(filepaths, arm):
    
    # Read in all the data files
    data_dfs = []
    skipped_files = []

    for fp in filepaths:
        if Path(fp).exists():
            df = pd.read_csv(fp)

            if df.shape[0] == 13334:
                data_dfs.append(df)
                print(f"✅ Loaded: {fp} ({df.shape[0]} rows)")
            else:
                print(f"❌ ERROR: Invalid length: {fp}")
                print(f"   File length: {df.shape[0]} rows (expected 13334)")
                skipped_files.append(fp)
        else:
            print(f"⚠️ WARNING: File not found, skipping: {fp}")
            skipped_files.append(fp)

    # Check if we have any valid data
    if len(data_dfs) == 0:
        print("❌ ERROR: No valid files found!")
        return None

    print(f"\nINFO: Combining {len(data_dfs)} out of {len(filepaths)} files")

    # Combine all dataframes
    combined_df = pd.concat(data_dfs, ignore_index=True)

    folder = Path(f"/Users/pradnyakadam/Downloads/Riboswitch_Manuscript/data_compilation/{arm}RNC")

    # Create the combined_data folder if it doesn't already exist
    folder.mkdir(parents=True, exist_ok=True)

    combined_df.to_csv(folder / "combined_data.csv", index=False)

    print(f"INFO: Combined data saved to {folder / 'combined_data.csv'}")
    print(f"SKIPPED {len(skipped_files)} FILES: {skipped_files}")

    return combined_df