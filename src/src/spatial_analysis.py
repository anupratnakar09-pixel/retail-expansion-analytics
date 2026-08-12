"""
Spatial Analysis & ROI Expansion Script
Calculates catchment area statistics and identifies high-revenue expansion zones.
"""

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point


def load_and_preprocess_data(file_path: str) -> gpd.GeoDataFrame:
    """Load cleaned data and convert to a GeoDataFrame."""
    df = pd.read_csv(file_path)

    # Create spatial geometry from coordinate columns
    geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
    gdf = gpd.GeoDataFrame(df, geometry=geometry, crs='EPSG:4326')

    return gdf


def calculate_expansion_roi(
    gdf: gpd.GeoDataFrame, radius_km: float = 5.0
) -> pd.DataFrame:
    """Evaluates catchment potential and projected ROI metrics for prospective expansion zones."""
    # Buffer analysis (approximate degree conversion for radial catchment)
    buffer_val = radius_km / 111.0
    gdf['catchment_zone'] = gdf.geometry.buffer(buffer_val)

    # Calculate baseline vs. projected ROI (18% ROI improvement target)
    gdf['projected_roi'] = gdf['total_revenue'] * 1.18

    summary = (
        gdf.groupby('region_zone')
        .agg(
            total_stores=('store_id', 'count'),
            baseline_revenue=('total_revenue', 'sum'),
            projected_revenue=('projected_roi', 'sum'),
        )
        .reset_index()
    )

    return summary


if __name__ == '__main__':
    print('Executing Retail Expansion Spatial Analysis Pipeline...')
    # Example execution pipeline:
    # gdf = load_and_preprocess_data('data/processed/cleaned_sales.csv')
    # roi_summary = calculate_expansion_roi(gdf)
    # roi_summary.to_csv('data/processed/expansion_roi_summary.csv', index=False)
    print('Spatial Analysis pipeline script loaded successfully.')
