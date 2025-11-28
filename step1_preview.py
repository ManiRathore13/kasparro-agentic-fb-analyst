import pandas as pd

# Load your CSV
df = pd.read_csv("synthetic_fb_ads_undergarments.csv")

# Show basic info
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())

# Show first 5 rows
print(df.head(5))