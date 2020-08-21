#rmb to hide!!
endpoint = "https://fast-google-api.cognitiveservices.azure.com/"

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

import urllib
import requests
from bs4 import BeautifulSoup
import random
from gensim.summarization import summarize

def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

def find_average(score):
  	return sum(score)/len(score)

def get_arg_max(l):
	return max(zip(l, range(len(l))))[1]

def sentiment_analysis_example(client,documents):

    response = client.analyze_sentiment(documents = documents)[0]
    return response.confidence_scores.positive, response.confidence_scores.neutral, response.confidence_scores.negative

def generateScore(client, link):
	article = requests.get(link)
	article_content = article.content
	soup_article = BeautifulSoup(article_content, 'html.parser')
	title = soup_article.title.string
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
	pos, neu, neg = sentiment_analysis_example(client,document)
	return pos, neu, neg, title

def get_results(query):

	# query: String

	# desktop user-agent
	USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
	# mobile user-agent
	MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"

	client = authenticate_client()

	query = query.replace(' ', '+')
	URL = f"https://google.com/search?q={query}"

	headers = {"user-agent": USER_AGENT}
	resp = requests.get(URL, headers=headers)

	pos_list = []
	neu_list = []
	neg_list = []
	link_list = []
	title_list = []

	if resp.status_code == 200:
	    soup = BeautifulSoup(resp.content, "html.parser")
	    results = []
	    for g in soup.find_all('div', class_='r'):
	        anchors = g.find_all('a')
	        if anchors:
	            link = anchors[0]['href']
	            try:
	              pos, neu, neg, title = generateScore(client, link)
	              pos_list.append(pos)
	              neu_list.append(neu)
	              neg_list.append(neg)
	              link_list.append(link)
	              title_list.append(title)
	            except:
	              continue
	
	pos_rate = find_average(pos_list)
	neu_rate = find_average(neu_list)
	neg_rate = find_average(neg_list)

	max_pos = get_arg_max(pos_list)
	pos_title = title_list[max_pos]
	pos_link = link_list[max_pos]

	max_neu = get_arg_max(neu_list)
	neu_title = title_list[max_neu]
	neu_link = link_list[max_neu]

	max_neg = get_arg_max(neg_list)
	neg_title = title_list[max_neg]
	neg_link = link_list[max_neg]

	pos = [pos_rate,pos_title,pos_link]
	neu = [neu_rate,neu_title,neu_link]
	neg = [neg_rate,neg_title,neg_link]

	return pos,neu,neg

if __name__ == '__main__':
	print(get_results('is lee kuan yew a good leader?'))