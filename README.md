vb# FASDH25-portfolio2
A repository for students' portfolios for mini-project 2

# Gaza Conflict Placename Analysis

This project analyzes geographical mentions in news articles about the 2023 Israel-Hamas conflict using two approaches: regex-based gazetteer matching and NLP-based named entity recognition (NER). The results are visualized on interactive maps showing spatial and temporal patterns.

## Project Structure

FASDH25-portfolio2/
├── articles/ # News article corpus (YYYY-MM-DD format)
├── gazetteers/
│ ├── geonames_gaza_selection.tsv # Original gazetteer
│ └── NER_gazetteer.tsv # Generated NER gazetteer
├── scripts/
│ ├── regex_script_final.py # Final regex extraction script
│ ├── regex_mapping.py # Regex-based mapping script
│ ├── build_gazetteer.py # Gazetteer construction script
│ └── copy_of_Gaza_NER2_kamil_faizan.ipynb # NER extraction notebook
│ │
│ ├── regex_counts.tsv # Regex-extracted frequencies
│ ├── ner_counts.tsv # NER-extracted frequencies
│ ├── regex_map.html # Regex interactive visualization
│ ├── regex_map.png # Regex static visualization
│ ├── ner_map.html # NER interactive visualization
│ └── ner_map.png # NER static visualization
└── README.md # This documentation

## Place Name Extraction (`regex_script_final.py`)

This project involves adapting a regular expression script to extract place names in Gaza from a corpus of news articles using a gazetteer with alternative name variants. The script processes a large corpus of articles published after October 7, 2023 and identifies place names by matching all known variants from the gazetteer using enhanced regular expressions. It improves recall by going beyond just the “asciiname” column and constructing regex patterns that account for alternative formats. The script performs case-insensitive, word-boundary-aware matching to avoid false positives and tracks how often each place is mentioned per month. These monthly counts are stored in a nested dictionary and saved to a `regex_counts.tsv` file.

###  Data Visualization (`mapping_script.py`) 

This project merges regex-extracted place name frequencies with gazetteer coordinates to generate an interactive, animated map using Plotly Express. The map shows markers whose size and color (based on a Yellow-Orange-Red scale) represent mention frequency, with monthly animation frames revealing changes over time. The Carto Positron basemap without labels was selected to reduce visual clutter, and markers are double-encoded with size and color for clarity. Output is saved as both an interactive HTML file (regex_map.html) and a static PNG (regex_map.png). This approach was chosen for its ability to clearly convey spatial and temporal trends in place name mentions across the dataset.

##  Use stanza to extract all place names from (part of) the corpus

In this part of the project, we used Stanza, an NLP toolkit developed by Stanford, to identify and extract place names from a large collection of news articles. The aim was to automate the detection of geographic entities—such as cities, countries, and regions—and count how often they appeared in texts written during January 2024. We began by loading a folder of `.txt` files from our portfolio repository, filtering only those filenames containing `"2024-01"` to isolate articles from the target month. After downloading the English language model, we initialized a Stanza pipeline equipped with tokenization and Named Entity Recognition (NER) processors. Each article was passed through this pipeline, and we extracted entities tagged as LOC (locations) or GPE (geopolitical entities). These place names were then normalized to account for variation in formatting—for instance, removing possessive endings like “’s”, stripping punctuation, and dropping the word “the” from the beginning of names. This helped to merge duplicate mentions under a single, standardized form. Finally, we compiled the results into a TSV file (`ner_counts.tsv`), with each row representing a place and the number of times it was mentioned.

### Create a gazetteer for the NER places

In this step, we transformed the list of place names extracted by Stanza into a structured gazetteer containing geographic coordinates. Using the `ner_counts.tsv` file generated earlier, we read all the unique place names and queried the GeoNames API to retrieve their latitude and longitude. This was done through a custom Python function, `get_coordinates`, which sent requests to the API with each place name and parsed the returned JSON response to extract the first matching coordinate. To avoid overwhelming the API server, we added a delay between requests. If the API returned no results for a place, we recorded its coordinates as `"NA"`. The final output, `ner_gazetteer.tsv`, contains three columns: Name, Latitude, and Longitude. For places where the API could not return results, we manually searched for coordinates using Google and updated the file accordingly. All manually looked-up locations were noted in the README for transparency. This gazetteer now serves as a reference to plot or analyze the spatial distribution of places mentioned in the January 2024 news articles.
these wre the list of places we manually searched the coordinates for.
1.	Miranda Cleland
2.	Al-Jiftlik
3.	Wadi Farhana
4.	Dahiyeh
5.	Shawawra
6.	alFukhari
7.	Bosnia and Herzegovina
8.	Sistan and Baluchestan
9.	Houthis
10.	alKarama	
11.	Beruit
12.	alShifa
13.	Bahaa
14.	alWalaja
15.	Rawaa
16.	alAhli
17.	Philadelphi
18.	Jawwal
19.	Africa4Palestine
20.	AlFukhari
21.	alNasser
22.	alSaftawi
23.	Pashias
24.	northGaza
25.	RedSea
26.	AlAqsa
27.	Margaliot
28.	Rmeish
29.	Taalbaya
30.	Dabbouch
31.	Hebrew
32.	alTanf
33.	Houthi
34.	alMaghazi
35.	alMughraqa
36.	Dahiyeb
37.	alMawasi
38.	alMahatta
39.	Ahmadiyyah Zawiya
40.	alFawakhir
41.	Mercator
42.	Nakba Layer
43.	Thameen Darby
44.	alMazraa Asharqiya
45.	alKhader
46.	alTawil

### Map the NER-Extracted Placenames

In this task, we visualized the geographic distribution of place names extracted using Stanza-based NER from news articles published in January 2024. Using Plotly Express, we plotted the frequency of each location based on the coordinates retrieved earlier (from `NER_gazetteer.tsv`) and their occurrence counts (from `ner_counts.tsv`). After merging both datasets on the place name, we cleaned the data by removing rows with missing or non-numeric values in the frequency or coordinate columns. The result was a scatter geo map, with point sizes scaled by frequency, making it easy to observe which places were most frequently mentioned in the corpus. The map was saved as both an interactive HTML file (`ner_map.html`) and a static PNG image (`ner_map.png`), enabling both detailed exploration and easy sharing or inclusion in reports.

## advantages and disadvantages of the two techniques used (regex+gazetteer and NER)

The regex+gazetteer method is like using a detailed checklist to find place names. Since it only matches names that are already listed in the gazetteer (including different spellings and translations), it gives very precise results with few mistakes. This makes it great for projects where accuracy matters most, like mapping well-known cities or historical locations. It's also fast and easy to use since it doesn't need complex processing just simple word matching. However, its biggest weakness is that it can't find places that aren't on its list. If a news article mentions a new or unofficial location, this method will miss it. It also can't tell if a word is being used as a metaphor (like "Gaza" representing a humanitarian crisis rather than the actual place), which could lead to some incorrect matches.

The NER (Stanza) method, on the other hand, is more like a smart detective that reads sentences to find place names. It doesn’t just rely on a list—it looks at the context of words to decide if they’re locations. This means it can find new or rarely mentioned places that the regex method would miss, making it ideal for breaking news or rapidly changing situations like conflicts. However, because it depends on understanding language, it sometimes makes mistakes—like labeling people’s names or groups as places. It also requires extra work to clean up the results and match them with real-world coordinates. While it’s more flexible, it’s slower and needs more manual checking compared to the straightforward regex approach.

## maps
![image(scripts/regex_map)]
![image(scripts/ner_map)]

### comparison between the maps

The two maps for January 2024, one made using NER (Named Entity Recognition) and the other using regex, show clear differences in what they focus on and how easy they are to understand. The NER map shows place names from all over the world, including countries, cities, and regions. Because of this it looks very crowded, especially over areas like Europe, North America, and the Middle East. This wide coverage is helpful for seeing global patterns, but it can also be messy and hard to read, making it difficult to focus on any one region.
On the other hand, the regex map is much more focused. It only shows a few places, mostly in the Gaza Strip—like Gaza City, Rafah, Khan Yunis, and Deir al-Balah. This map is clearer and easier to understand, especially because it includes a time slider that shows how often these places were mentioned over time. It’s likely that the regex method was used to track specific news or events in that region, like conflict. So while the NER map gives a big-picture view of global mentions, the regex map gives a close-up of one important area. Overall, the regex map is more focused and easier to analyze, while the NER map shows a wider, but more cluttered view.

## Self-critical analysis: what are the weaknesses of the project as it currently is; what could be improved if there was more time?

Even though the project made solid progress in finding place names using both regex and NER (Stanza), there were still some issues. Not all place names were detected especially ones with uncommon spellings or punctuation like “Gaza’s.” Regex still depends too much on the gazetteer’s spelling patterns, so it misses names that aren't listed or written differently. The NER model also struggled with some locations, especially if they were less well-known or looked like people’s names. On top of that, the NER method was only applied to January 2024 articles, which makes it hard to compare with regex across the whole timeline. Manual location lookup also made things inconsistent, and the maps, while useful, could be more interactive. The code works, but it’s not modular or fully automated, which would make it harder to reuse or scale.
If there was more time, a lot could be improved. Using matching (like checking for similar spellings) could help clean up NER results by grouping similar names. Including more months in the NER analysis would give a fuller picture. Automating the coordinate lookup maybe with backup tools like Wikipedia or OpenStreetMap would reduce manual effort. It would also help to test how accurate both methods are using a small labeled dataset. An interactive dashboard would make it easier to explore the data, and better cleaning of text (like removing stopwords or fixing messy names) would improve results.


