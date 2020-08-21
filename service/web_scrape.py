import urllib
import requests
from bs4 import BeautifulSoup
import random
from gensim.summarization import summarize

def find_average(score):
  return sum(score)/len(score)

def generateScore(link):
  article = requests.get(link)
  article_content = article.content
  soup_article = BeautifulSoup(article_content, 'html.parser')
  p_tags  = soup_article.find_all('p')
  p_tags_text = [tag.get_text().strip() for tag in p_tags]
  document = [" ".join(p_tags_text)]
  if len(document[0])>10000:
    document = [" ".join(random.sample(p_tags_text,int(8000/len(document[0])*len(p_tags_text))))]
  if len(document[0])>5000:
    #print(len(document[0]))
    summary = summarize(document[0], ratio=(3500/len(document[0])))
    document = [summary.replace("\n", " ")]
    # Combine list items into string.
  #print(len(document[0]))
  #print(f'Summary: {document}\n')
  return sentiment_analysis_example(client,document)
generateScore("https://www.healthline.com/nutrition/milk-benefits")