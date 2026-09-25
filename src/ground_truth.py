"""Independent evaluator calculations. Never import into the model/tool runtime."""
from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from study import ROOT, DATASET, clean, digest

UNANSWERABLE_REASONS = {
    'A01_profit': 'Unit sales contain neither sale prices/revenue nor costs needed for net profit.',
    'A02_reviews': 'There is no critic review score column.',
    'A03_distribution': 'There is no digital/physical distribution-channel breakdown.',
    'A04_causality': 'Marketing spending, treatment/exposure, timing and causal identification are absent.',
    'A05_transaction_year': 'Year is release year, and the sales columns do not identify when sales transactions occurred.',
    'A06_population': 'The coverage excludes unlisted and low-selling games; a sample cannot identify the complete worldwide title population.',
}

def derive(df):
    top = df.sort_values(['Global_Sales','Rank'], ascending=[False,True], kind='stable').head(5)
    annual = df[df.Year.notna()].groupby('Year', sort=True).Global_Sales.sum().reset_index()
    peak = annual.sort_values(['Global_Sales','Year'], ascending=[False,True]).iloc[0]
    regional = df.groupby('Genre', sort=True)[['NA_Sales','EU_Sales','JP_Sales']].sum().reset_index()
    subset = df[(df.Publisher=='Nintendo') & (df.Platform=='DS') & df.Year.between(2005,2010)]
    publishers = (df[df.Year.between(2000,2009) & df.Publisher.notna()]
        .groupby('Publisher').Global_Sales.sum().reset_index()
        .sort_values(['Global_Sales','Publisher'], ascending=[False,True]).head(5))
    truth = {
        'Q01_quality': {'missing_year_rows': int(df.Year.isna().sum()),
                        'out_of_range_year_rows': int((df.Year.notna() & ~df.Year.between(1980,2016)).sum()),
                        'missing_publisher_rows': int(df.Publisher.isna().sum())},
        'Q02_top_games': {'top_game_name': top.iloc[0].Name, 'top_game_platform': top.iloc[0].Platform,
                         'top_game_global_sales': top.iloc[0].Global_Sales,
                         'second_game_name': top.iloc[1].Name, 'second_game_global_sales': top.iloc[1].Global_Sales},
        'Q03_release_year': {'peak_release_year': int(peak.Year), 'peak_release_year_global_sales': peak.Global_Sales},
        'Q04_regions': {},
        'Q05_filtered': {'matching_rows': len(subset), 'global_sales_total': subset.Global_Sales.sum()},
        'Q06_publishers': {'top_publisher': publishers.iloc[0].Publisher,
                           'top_publisher_global_sales': publishers.iloc[0].Global_Sales},
    }
    for region,col in [('na','NA_Sales'),('eu','EU_Sales'),('jp','JP_Sales')]:
        best = regional.sort_values([col,'Genre'],ascending=[False,True]).iloc[0]
        truth['Q04_regions'][region+'_top_genre'] = best.Genre
        truth['Q04_regions'][region+'_top_genre_sales'] = best[col]
    plots = {
        'Q02_top_games': {'kind': 'bar', 'x': 'Name', 'ys': ['Global_Sales'], 'rows': top[['Name','Global_Sales']].to_dict('records')},
        'Q03_release_year': {'kind': 'line', 'x': 'Year', 'ys': ['Global_Sales'], 'rows': annual.to_dict('records')},
        'Q04_regions': {'kind': 'bar', 'x': 'Genre', 'ys': ['NA_Sales','EU_Sales','JP_Sales'], 'rows': regional.to_dict('records')},
        'Q06_publishers': {'kind': 'bar', 'x': 'Publisher', 'ys': ['Global_Sales'], 'rows': publishers.to_dict('records')},
    }
    return clean({'answers': truth, 'plots': plots, 'unanswerable_reasons': UNANSWERABLE_REASONS})

def main():
    truth = derive(pd.read_csv(DATASET))
    truth['dataset_sha256'] = digest(DATASET.read_bytes())
    destination = ROOT/'data'/'ground_truth.json'
    destination.write_text(json.dumps(truth, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps(truth['answers'], indent=2))

if __name__ == '__main__':
    main()
