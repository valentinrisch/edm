"""This program extracts the training and evaluation set in a way that they conform the required input format of FastText model"""

import pandas as pd
import numpy as np
import sqlite3

#Comment it out for main training
np.random.seed(0)

#Removes the empty lines in comment body
def remove_empty_lines(comment):
    out = comment.replace('\r\n', ' ').replace('\n',' ')
    return out

#Reading in the Post table 
litedb = sqlite3.connect('./assets/dataset/million_post_corpus/corpus.sqlite3')
df = pd.read_sql_query("SELECT * from Posts", litedb)
litedb.close()

#getting rid od the missing values in Body column
df.loc[df.Body == '','Body'] = np.nan
df = df[df.Body.notnull()]

#Spliting the dataset to train and evalute datasets 80%-20% respectivly
msk = np.random.rand(len(df)) < 0.8
training_df = df[msk]
evaluation_df = df[~msk]

#Writing the results to txt files
with open('./assets/outputs/FastTextTraining.txt', 'w') as text_file:
	for index, row in training_df.iterrows():
		text_file.write("__label__%s %s\n" % (row['Status'], remove_empty_lines(row["Body"])))

with open('./assets/outputs/FastTextEvaluation.txt', 'w') as text_file:
    for index, row in evaluation_df.iterrows():
        text_file.write("__label__%s %s\n" % (row['Status'], remove_empty_lines(row["Body"])))

