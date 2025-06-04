def print_dataframe_shape(df, label=""):
    if df.empty:
        print(f"⚠️ {label} - DataFrame is empty.")
    else:
        print(f"✅ {label} - Shape: {df.shape}")
