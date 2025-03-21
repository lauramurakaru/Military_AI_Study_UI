import pandas as pd

def build_mappings_from_csv(csv_path: str):
    # 1) Read the CSV
    df = pd.read_csv(csv_path)

    # 2) List all columns
    all_cols = df.columns.tolist()
    print("All columns in dataset:")
    print(all_cols)

    # We'll store all mappings in a dict of dicts.
    # For example, mappings["Target_Category"] = { "Artillery Unit": 3, "Chapel": -1, ... }
    mappings = {}

    # 3) Identify pairs of columns: e.g. "Target_Category" and "Target_Category_Score"
    #    We'll do that by looking for columns that end with "_Score" and see if
    #    the base name (minus "_Score") is also a column.
    for col in all_cols:
        if col.endswith("_Score"):
            base_col = col.replace("_Score", "")  # e.g. "Target_Category_Score" -> "Target_Category"
            if base_col in all_cols:
                # We found a pair: base_col + "_Score"
                print(f"\nBuilding mapping for: {base_col} -> {col}")
                # For each raw value in base_col, find the mode of col
                # If a raw value has multiple modes, we'll pick the first.
                # (Adjust if you want a different behavior.)
                grouped = df.groupby(base_col)[col].agg(lambda x: x.mode()[0]).to_dict()
                mappings[base_col] = grouped

    return mappings

if __name__ == "__main__":
    csv_file = "dataset_with_all_category_scores.csv"  # Adjust if needed
    all_mappings = build_mappings_from_csv(csv_file)

    # 4) Print the resulting mappings
    print("\nGenerated Mappings:")
    for raw_col, mapping_dict in all_mappings.items():
        print(f"\n{raw_col} Map = {{")
        for raw_val, numeric_score in mapping_dict.items():
            print(f"  '{raw_val}': {numeric_score},")
        print("}")
