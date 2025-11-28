import pandas as pd

df = pd.read_csv("synthetic_fb_ads_undergarments.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

df['ctr_calc'] = df['clicks'] / df['impressions']
df['roas_calc'] = df['revenue'] / df['spend']

print(df[['campaign_name', 'date', 'impressions', 'clicks', 'ctr', 'ctr_calc', 'roas', 'roas_calc']].head(10))