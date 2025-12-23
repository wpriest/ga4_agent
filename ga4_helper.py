import pandas as pd
import plotly.express as px

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange, Dimension, Metric, RunReportRequest

def fetch_ga4_data(property_id, start_date, end_date, dimensions, metrics):
    """
    Haalt gegevens op uit Google Analytics Data API v1.
    Args:
        property_id (str): Het GA4 property ID (bijv. '328403728')
        start_date (str): Begin datum in 'YYYY-MM-DD' formaat
        end_date (str): Eind datum in 'YYYY-MM-DD' formaat
        dimensions (list): Lijst van dimension strings (bijv. ['date', 'country'])
        metrics (list): Lijst van metric strings (bijv. ['sessions', 'totalUsers'])
    Returns:
        DataFrame: Een pandas DataFrame met het resultaat
    """
    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name=d) for d in dimensions],
        metrics=[Metric(name=m) for m in metrics],
        date_ranges=[DateRange(start_date=start_date, end_date=end_date)],
    )
    response = client.run_report(request)
    
    # Parse rows into DataFrame
    rows = []
    for row in response.rows:
        record = {}
        for i, dim in enumerate(dimensions):
            record[dim] = row.dimension_values[i].value
        for i, metric in enumerate(metrics):
            record[metric] = float(row.metric_values[i].value)
        rows.append(record)
    df = pd.DataFrame(rows)
    return df

def plot_metrics(df, dimensions, metrics, output_file):
    """
    Maakt een plot van de metrics met Plotly en slaat deze op als afbeelding.
    Args:
        df (DataFrame): DataFrame met de data
        dimensions (list): Lijst met dimensions gebruikt als x-as (pakte eerste)
        metrics (list): Lijst met metrics (meerdere mogelijk, meerdere lijnen)
        output_file (str): Pad naar bestand om op te slaan (bijv. .png, .jpg, .html)
    """
    # Create line plot
    x_axis = dimensions[0]
    fig = px.line(df, x=x_axis, y=metrics, title="GA4 Metrics Plot")
    
    # Save to file
    # Note: Requires 'kaleido' package for static image export
    if output_file.endswith('.html'):
        fig.write_html(output_file)
    else:
        fig.write_image(output_file)
