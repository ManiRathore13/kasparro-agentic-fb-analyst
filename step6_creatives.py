import pandas as pd
import re
from collections import Counter

df = pd.read_csv("synthetic_fb_ads_undergarments.csv")

# simple stopwords list
stopwords = set(["the","and","for","with","your","you","our","buy","new","now","get","free","in","on","to","of","a","an"])

def extract_keywords(texts, n=8):
    words = []
    for msg in texts.dropna():
        tokens = re.findall(r"[A-Za-z]{3,}", msg.lower())
        tokens = [t for t in tokens if t not in stopwords]
        words.extend(tokens)
    common = [w for w, _ in Counter(words).most_common(n)]
    return common

campaigns = [
    "Women Cotton Classics",
    "WOMEN | STUDIO SPORTS",
    "MEN Sign-ture Soft",
    "Men  Bold  Colors  Drop",
    "Wom n Fit & Lift"
]

templates = [
    "Experience {kw1} comfort designed for everyday wear.",
    "Feel the {kw1} difference — made for movement and confidence.",
    "Our new {kw1} pieces combine {kw2} feel with perfect fit.",
]

for camp in campaigns:
    print("\n====", camp, "====")

    camp_df = df[df['campaign_name'] == camp]
    if camp_df.empty:
        print("No creative messages found.")
        continue
    
    keywords = extract_keywords(camp_df['creative_message'])
    if not keywords:
        keywords = ["comfort", "soft", "breathable"]

    suggestions = []
    for i, temp in enumerate(templates):
        kw1 = keywords[i % len(keywords)]
        kw2 = keywords[(i+1) % len(keywords)]
        msg = temp.format(kw1=kw1.capitalize(), kw2=kw2.capitalize())
        suggestions.append(msg)

    for s in suggestions:
        print("-", s)