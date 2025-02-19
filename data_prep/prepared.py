import pandas as pd

# Load Data
df = pd.read_csv('./data/u2.item', sep="|", encoding="latin-1", header=None, names=["movie_id", "title", 'col3', 'col4', 'col5', 'col6', 'col7', 'col8', 'col9', 'col10', 'col11',
                                                                                   'col12', 'col13', 'col14', 'col15', 'col16', 'col17', 'col18', 'col19', 'col20', 'col21',
                                                                                   'col22', 'col23', 'col24'])

# Split title into name and year
df['title'] = df['title'].str.split('[(][\d]', regex=True, expand=True)[0]

# Strip white spaces
df['title'] = df['title'].str.strip()

# Movie title to lowecase
df['title'] = df['title'].str.lower()


# drop header
df.to_csv('./data/u.item', index=False, header=False, sep="|")

'''
This file is used to prepare the data once it comes from the MovieLens website
It will remove the year from the movie title and strip white spaces
'''