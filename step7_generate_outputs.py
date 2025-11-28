import pandas as pd
import numpy as np
import re
import json
from collections import Counter

df = pd.read_csv("synthetic_fb_ads_undergarments.csv")
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Aggregation
grouped = df.groupby(['campaign_name','date']).agg({
    'spend':'sum',
    'impressions':'sum',
    'clicks':'sum',
    'revenue':'sum'
}).reset_index()

grouped['ctr'] = grouped['clicks'] / grouped['impressions']
grouped['roas'] = grouped['revenue'] / grouped['spend']

# campaigns we are analyzing
campaigns = [
    "Women Cotton Classics",
    "WOMEN | STUDIO SPORTS",
    "MEN Sign-ture Soft",
    "Men  Bold  Colors  Drop",
    "Wom n Fit & Lift"
]


# ----- INSIGHT GENERATION (from Step 5) -----

def get_insights(name):
    camp = grouped[grouped['campaign_name']==name].sort_values('date')
    if camp.empty:
        return []

    first, last = camp.iloc[0], camp.iloc[-1]

    insights = []
    
    # ROAS drop
    if pd.notna(first['roas']) and first['roas'] > 0:
        roas_drop = ((last['roas'] - first['roas']) / first['roas']) * 100
        if roas_drop < -20:
            insights.append({
                "type": "roas_drop",
                "message": f"ROAS dropped from {first['roas']:.2f} to {last['roas']:.2f} ({roas_drop:.1f}%). Possible conversion or targeting issue.",
            })
    
    # CTR drop
    if pd.notna(first['ctr']) and pd.notna(last['ctr']):
        if last['ctr'] < first['ctr'] * 0.8:
            insights.append({
                "type": "ctr_drop",
                "message": f"CTR dropped from {first['ctr']:.4f} to {last['ctr']:.4f}. Likely creative fatigue or weaker engagement.",
            })
    
    # Spend drop
    if last['spend'] < first['spend'] * 0.7:
        insights.append({
            "type": "spend_cut",
            "message": "Spend reduced by over 30%. Suggests scaling down or budget reallocation.",
        })

    # Impressions vs CTR
    if last['impressions'] > first['impressions'] and last['ctr'] < first['ctr']:
        insights.append({
            "type": "audience_fatigue",
            "message": "Impressions increased but CTR fell — classic audience fatigue.",
        })

    if not insights:
        insights.append({
            "type": "general_issue",
            "message": "Performance decline due to multiple minor factors.",
        })

    return insights


# ----- CREATIVE GENERATION (from Step 6) -----

stopwords = set(["the","and","for","with","your","you","our","buy","new","now","get","free","in","on","to","of","a","an"])

def extract_keywords(texts, n=8):
    words = []
    for msg in texts.dropna():
        tokens = re.findall(r"[A-Za-z]{3,}", msg.lower())
        tokens = [t for t in tokens if t not in stopwords]
        words.extend(tokens)
    common = [w for w, _ in Counter(words).most_common(n)]
    return common

templates = [
    "Experience {kw1} comfort designed for everyday wear.",
    "Feel the {kw1} difference — made for movement and confidence.",
    "Our new {kw1} pieces combine {kw2} feel with perfect fit.",
]

def get_creatives(name):
    camp_df = df[df['campaign_name']==name]
    if camp_df.empty:
        return []

    keywords = extract_keywords(camp_df['creative_message'])
    if not keywords:
        keywords = ["comfort", "soft", "breathable"]

    messages = []
    for i, temp in enumerate(templates):
        kw1 = keywords[i % len(keywords)]
        kw2 = keywords[(i+1) % len(keywords)]
        msg = temp.format(kw1=kw1.capitalize(), kw2=kw2.capitalize())
        messages.append(msg)

    return messages


# ----- Final JSON Output -----

all_insights = {}
all_creatives = {}

for camp in campaigns:
    all_insights[camp] = get_insights(camp)
    all_creatives[camp] = get_creatives(camp)

# Save JSON files
with open("insights.json", "w") as f:
    json.dump(all_insights, f, indent=4)

with open("creatives.json", "w") as f:
    json.dump(all_creatives, f, indent=4)

print("JSON files created successfully!")