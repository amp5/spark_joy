# -*- coding: UTF-8 -*-
import pandas as pd
from pandas.io.json import json_normalize
import json
from collections import Counter
    
filepath = '/Users/alexandraplassaras/src/spark_joy/comments.json'

with open(filepath, 'r') as f:
    data = json.load(f)

comment_list = []
for item in data['items']:
    comment_row = item['snippet']['topLevelComment']['snippet']
    del comment_row['authorDisplayName']
    del comment_row['authorProfileImageUrl']
    del comment_row['canRate']
    del comment_row['updatedAt']
    del comment_row['viewerRating']
    del comment_row['textOriginal']
    del comment_row['authorChannelUrl']
    del comment_row['likeCount']

    comment_list.append(comment_row)

df = pd.DataFrame(comment_list)
def extract_emojis(sentence):
    return [word for word in sentence.split() if str(word.encode('unicode-escape'))[2] == '\\' ]
df['emoji'] = df['textDisplay'].apply(lambda x: extract_emojis(x))

emoji_lst = df['emoji'].tolist()

main_emoji = []
for i in emoji_lst:
    if i == []:
        continue
    for j in i:
        for k in j:
            main_emoji.append(k)

counts = Counter(main_emoji)
emoji_df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
emoji_df = emoji_df.rename(index=str, columns={"index": "emoji", 0: "count"})

emoji_df = emoji_df.sort_values(by=['count'], ascending = False)


emoji_df['pct'] = round((emoji_df['count']/emoji_df['count'].sum()) * 100, 2)

return emoji_df

