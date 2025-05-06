# import the relevant libraries: plotly express and pandas
import pandas as pd
import plotly.express as px
import kaleido



# load the gazetteer tsv file:
gazetteer_path = "../gazetteers/geonames_gaza_selection.tsv"
coordinates = pd.read_csv(gazetteer_path, sep="\t")

# load the regex frequency counts
counts_path = "regex_counts.tsv"
counts = pd.read_csv(counts_path, sep="\t")

# Ensure both DataFrames use the same column name for merging
# Rename 'placename' to 'asciiname' to match the gazetteer file
counts.rename(columns={"placename": "asciiname"}, inplace=True)

# Merge the coordinates with the frequency counts using the common column 'asciiname'
merged = pd.merge(coordinates, counts, on="asciiname")

# create the map of all the place names:
# Create an animated map using Plotly Express # got from the mapping exercise slide 24
fig = px.scatter_map(            # switched to scatter_mapbox for correct functionality
    merged,                         # Data source
    lat="latitude",                 # Latitude column
    lon="longitude",                # Longitude column
    hover_name="asciiname",        # Name shown on hover
    color="count",                 # Color scale by mention count
    size="count",                  # Size of marker depends on mention count
    animation_frame="month",       # Create a frame for each month
    size_max=40,                   # Max size for markers
    color_continuous_scale=px.colors.sequential.YlOrRd
)

# use a different background map, without labels:  #slide 33 
fig.update_layout(map_style="carto-positron-nolabels", map=dict(style="dark"))

# display the interactive map in the browser:
fig.show()

# Save the interactive map as an HTML file
fig.write_html("regex_map.html")

# save the file as png
fig.write_image("regex_map.png")
