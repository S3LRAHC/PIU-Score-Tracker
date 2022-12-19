# Gathers PIU XX full song list titles from xlsx to txt file

import pandas as pd

df = pd.read_excel("full_song_list.xlsx", usecols = "F")

with open("songTitles.txt", 'w', encoding="utf-8") as f:
    dfAsString = df.to_string(header=False, index=False)
    f.write(dfAsString)

