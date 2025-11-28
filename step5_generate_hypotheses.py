import pandas as pd
import numpy as np

df = pd.read_csv("synthetic_fb_ads_undergarments.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Aggregate
grouped = df.groupby(['campaign_name','date']).agg({
    'spend':'sum',
    'impressions':'sum',
    'clicks':'sum',
    'revenue':'sum'
}).reset_index()

grouped['ctr'] = grouped['clicks'] / grouped['impressions']
grouped['roas'] = grouped['revenue'] / grouped['spend']

campaigns = [
    "Women Cotton Classics",
    "WOMEN | STUDIO SPORTS",
    "MEN Sign-ture Soft",
    "Men  Bold  Colors  Drop",
    "Wom n Fit & Lift"
]

def analyze_campaign(name):
    camp = grouped[grouped['campaign_name']==name].sort_values('date')
    if camp.empty:
        return None

    first, last = camp.iloc[0], camp.iloc[-1]

    insights = []
    
    # ROAS drop
    if pd.notna(first['roas']) and first['roas'] > 0:
        roas_drop = ((last['roas'] - first['roas']) / first['roas']) * 100
        if roas_drop < -20:
            insights.append(f"ROAS dropped sharply from {first['roas']:.2f} to {last['roas']:.2f} ({roas_drop:.1f}%). Possible conversion or targeting issue.")
    
    # CTR drop
    if pd.notna(first['ctr']) and pd.notna(last['ctr']):
        if last['ctr'] < first['ctr'] * 0.8:
            insights.append(f"CTR decreased from {first['ctr']:.4f} to {last['ctr']:.4f}, indicating creative fatigue or reduced engagement.")
    
    # Spend change
    if last['spend'] < first['spend'] * 0.7:
        insights.append("Spend decreased significantly, suggesting budget reduction or reallocation.")
    
    # Impressions high + CTR low
    if last['impressions'] > first['impressions'] and last['ctr'] < first['ctr']:
        insights.append("Higher impressions but lower CTR indicates audience fatigue or saturation.")

    if not insights:
        insights.append("Performance decline due to multiple minor factors. Needs deeper review.")

    return insights

# Run insights
for c in campaigns:
    print("\n====", c, "====")
    result = analyze_campaign(c)
    if result:
        for i in result:
            print("-", i)