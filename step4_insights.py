import pandas as pd

df = pd.read_csv("synthetic_fb_ads_undergarments.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

grouped = df.groupby(['campaign_name', 'date']).agg({
    'spend': 'sum',
    'impressions': 'sum',
    'clicks': 'sum',
    'revenue': 'sum'
}).reset_index()

grouped['ctr'] = grouped['clicks'] / grouped['impressions']
grouped['roas'] = grouped['revenue'] / grouped['spend']

campaigns_to_check = [
    "Women Cotton Classics",
    "WOMEN | STUDIO SPORTS",
    "MEN Sign-ture Soft",
    "Men  Bold  Colors  Drop",
    "Wom n Fit & Lift",
]

for camp in campaigns_to_check:
    camp_df = grouped[grouped['campaign_name'] == camp].sort_values('date')
    
    if camp_df.empty:
        continue
    
    ctr_first = camp_df['ctr'].iloc[0]
    ctr_last = camp_df['ctr'].iloc[-1]
    
    spend_first = camp_df['spend'].iloc[0]
    spend_last = camp_df['spend'].iloc[-1]
    
    impr_first = camp_df['impressions'].iloc[0]
    impr_last = camp_df['impressions'].iloc[-1]
    
    print("\n===== Campaign:", camp, "=====")
    print("CTR first:", ctr_first, "| CTR last:", ctr_last)
    print("Spend first:", spend_first, "| Spend last:", spend_last)
    print("Impressions first:", impr_first, "| Impressions last:", impr_last)