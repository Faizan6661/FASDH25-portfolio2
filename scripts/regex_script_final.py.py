# import the library
# import library for regular expressions 
import re 
# import library for os-dependent functions like files
import os
import pandas as pd

# define the folder that contains the articles
folder = "../articles"

# define the path to the gazetteer file
gazetteer_path = "../gazetteers/geonames_gaza_selection.tsv"
# open and read the file
with open(gazetteer_path, encoding="utf-8") as file:
    data = file.read()

# splits the entire gazetteer file into a list of rows
rows = data.split("\n")

# improve and recall of place names by using more columns for gazetteer

# build a dictionary of patterns from the place names in the first column and the alternative name column
# Create an empty dictionary to store place name patterns and their frequencies
patterns = {}
# split the gazetteer data by a new line to each row
rows = data.split("\n")

# Loop through all rows of the gazetteer, skipping the header
for row in rows[1:]:
    # Split each row into columns using tab as separator
    columns = row.split("\t")

    # Get the main place name (asciiname)
    asciiname = columns[0].strip()

    # check if there is alternativenames column (column 6 = index 5)
    if len(columns) > 5:
        alternatenames = columns[5]  # if yes use the names 
    else:
        alternatenames = ""  # if no alternativename column then leave it blank

    # make a list of all the names by splitting alternates by comma
    name_list = alternatenames.split(",")
    # adding the main asciinmaes to the list
    name_list.append(asciiname)

    # create a regex pattern by joining the names with the '|' symbol #from ChatGPT conversation 1
    regex_pattern = "|".join(re.escape(name) for name in set(name_list) if name)

    # add the patterns to the dictionary and start with the count 0
    if regex_pattern:
        patterns[asciiname] = regex_pattern

# dictionary to store total mentions per place
place_counts = {}

# dictionary to store mentions per month
mentions_per_month = {}

# count the number of times each pattern is found in the entire folder:
for filename in os.listdir(folder):  # loop through all the files in the folder
    # build the file path
    file_path = os.path.join(folder, filename)

    # Skip files before 2023-10-07
    if filename[:10] < "2023-10-07":  # goes through the first 10 characters in filename which represent YYYY-MM-DD
        continue

    # Extract the YYYY-MM part for the monthly count (e.g., "2023-11")
    month = filename[:7]

    # Read the article content
    with open(file_path, encoding="utf-8") as file:
        text = file.read()

    # find all the occurences of the patterns in the text:
    for placename, pattern in patterns.items():
        matches = re.findall(r"\b(" + pattern + r")\b", text, flags=re.IGNORECASE)  # Use word boundaries and ignore case
        n_matches = len(matches)  # number of times the place was found

        # add the number of times it was found to the total frequency:
        if placename not in place_counts:
            place_counts[placename] = 0
        place_counts[placename] += n_matches

        if n_matches > 0:
            # Initialize if this pattern is not in the dictionary yet
            if placename not in mentions_per_month:
                mentions_per_month[placename] = {}

            # Initialize the month if not already there
            if month not in mentions_per_month[placename]:
                mentions_per_month[placename][month] = 0

            # Add the count to the monthly mentions
            mentions_per_month[placename][month] += n_matches

# Prepare header for the TSV file
tsv_output = "placename\tmonth\tcount"

# Loop through the mentions_per_month dictionary to populate the rows
for placename in mentions_per_month:
    for month in mentions_per_month[placename]: # for each monh where the place was mentioned
        count = mentions_per_month[placename][month] # get the number of mentions for place in this month
        tsv_output += f"\n{placename}\t{month}\t{count}" # add a new row to the tsv with tab seperated value

# Write the output to a TSV file similar syntax to reading a file
with open("regex_counts.tsv", mode="w", encoding="utf-8") as f:
    f.write(tsv_output)
