import pandas as pd
import plotly.express as px

# Load TSV files
ner_counts = pd.read_csv("ner_counts.tsv", sep="\t")
gazetteer = pd.read_csv("NER_gazetteer.tsv", sep="\t")

# Standardize column name for merging
gazetteer.rename(columns={"Name": "name"}, inplace=True)

# Merge both datasets
merged_df = pd.merge(ner_counts, gazetteer, on="name")

# Drop rows with missing frequency or coordinates
merged_df.dropna(subset=["frequency", "Latitude", "Longitude"], inplace=True)

# Ensure 'frequency' is numeric (sometimes it's read as string)
merged_df["frequency"] = pd.to_numeric(merged_df["frequency"], errors="coerce")

# Create the map
fig = px.scatter_geo(
    merged_df,
    lat="Latitude",
    lon="Longitude",
    text="name",
    size="frequency",
    projection="natural earth",
    title="NER-Extracted Placenames (January 2024)"
)

# Save the outputs
fig.write_html("ner_map.html")
fig.write_image("ner_map.png")


