import Linkedin_Scraper as ls
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
# nltk.download()
from transformers import pipeline

plt.style.use('ggplot')

# Data = ls.linkedin_scraper()
# Data.to_excel('/Users/navin.jain/Desktop/Linkedin Sentiment/scraping_test.xlsx', index=False)

Data = pd.read_excel('/Users/navin.jain/Desktop/Linkedin Sentiment/scraping_test.xlsx')

## EDA
Data['Length'] = Data['Post'].str.len()

Data['Post'] = Data['Post'].astype('string')

bins = [0, 50, 100, 250, 500, 750, 1500, 2000, 2500]

Data['Len_bin'] = pd.cut(Data['Length'], bins)

Data.dtypes

fig, axs = plt.subplots(1, 2, figsize=(18, 3))
sns.histplot(Data['Length'], color='Red', kde=True, ax=axs[0])
sns.countplot(data=Data, x='Len_bin', ax=axs[1], color='Pink')
plt.show()

## WorkCloud


''''VADER (Valence Aware Dictionary and Sentiment Reasoner) - Bag of words approach
* This uses a "bag of words" approach:
* Stop words are removed
* each word is scored and combined to a total score'''

sia = SentimentIntensityAnalyzer()

scores = {}

for index, row in Data.iterrows():
    text = row['Post']
    id = row['Id']
    scores[id] = sia.polarity_scores(text)

scores = pd.DataFrame.from_dict(scores).T
scores = scores.reset_index().rename(columns={'index': 'Id'})
scores = scores.merge(Data, how='left')

# Plot sentiment
fig, axs = plt.subplots(1, 3, figsize=(18, 3))
sns.histplot(scores['pos'], color='Green', kde=True, ax=axs[0])
sns.histplot(scores['neg'], color='Red', kde=True, ax=axs[1])
sns.histplot(scores['neu'], color='Silver', kde=True, ax=axs[2])
plt.show()

'''
Transformers Pipeline
'''

Transformer = Data.copy()

Transformer['Truncate'] = np.where(Transformer['Post'].str.len() > 512, Transformer['Post'].str[:512],Transformer['Post'].str[:] )

sent_pipeline = pipeline("sentiment-analysis")

bert_scores = {}

for index, row in Transformer.iterrows():
    text = row['Truncate']
    Id = row['Id']
    bert_scores[Id] = sent_pipeline(text)

bert_scores = pd.DataFrame.from_dict(bert_scores).T
bert_scores = bert_scores.reset_index().rename(columns={'index': 'Id'})
bert_scores = bert_scores.merge(Transformer, how='left')