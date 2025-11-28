import pandas as pd

df = pd.read_csv("synthetic_fb_ads_undergarments.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# group by campaign and date
grouped = df.groupby(['campaign_name', 'date']).agg({
    'spend': 'sum',
    'impressions': 'sum',
    'clicks': 'sum',
    'revenue': 'sum'
}).reset_index()

# calculate metrics again
grouped['ctr'] = grouped['clicks'] / grouped['impressions']
grouped['roas'] = grouped['revenue'] / grouped['spend']

results = []

for campaign, camp_df in grouped.groupby('campaign_name'):
    camp_df = camp_df.sort_values('date')
    
    first = camp_df.iloc[0]
    last = camp_df.iloc[-1]
    
    roas_first = first['roas']
    roas_last = last['roas']
    
    if pd.notna(roas_first) and roas_first != 0:
        pct_change = ((roas_last - roas_first) / abs(roas_first)) * 100
    else:
        pct_change = None
    
    results.append([campaign, roas_first, roas_last, pct_change])

results_df = pd.DataFrame(results, columns=['campaign_name', 'roas_first', 'roas_last', 'pct_change'])

# show worst 10 campaigns
print(results_df.sort_values('pct_change').head(10))