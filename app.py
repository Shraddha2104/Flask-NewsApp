
from flask import Flask, request,jsonify, make_response, abort
from newsapi import NewsApiClient
import requests
from datetime import datetime
import string
from collections import Counter 
import re
from newsapi.newsapi_exception import NewsAPIException
app = Flask(__name__)

newsapi =NewsApiClient(api_key='bd1633c2e8fe42938ef415eb8aa060e0');


@app.route('/')
def index():
	return app.send_static_file('home.html')
		
@app.errorhandler(400)
def resource_not_found(e):
	return jsonify(str(e))

@app.route('/ajax', methods = ['POST'])
def ajax_request():
	start_date = request.form['start_date'];
	# print(start_date);
	end_date = request.form['end_date'];
	keyword = request.form['keyword'];
	category = request.form['category'];
	source = request.form['source'];
	print('sourceout'+source)
	if(source=='all'):
		source=request.form['source_list']
		print('sourcein'+source);
	# print(type(source));
	try:
		all_articles = newsapi.get_everything(q=keyword,language='en',sort_by='publishedAt',from_param=start_date,to=end_date,sources=source,page_size=30);
	except Exception as e:
		abort(400,description=e)
	retlist = []
	keys = ['description','source','author','title','url','urlToImage','publishedAt']
	
	for news in all_articles['articles']:
		p=0
		for key in keys:
			if (key not in news) or news[key]==None or len(news[key])==0:
				p = 1
		if p==0: retlist.append(news)
	print(retlist)
	return jsonify(all_articles=retlist)
	
@app.route('/loadHeadlines',methods = ['POST'])
def loadHeadlines():
	# print("in headlines");
	# newsapi=NewsApiClient(api_key='4dbc17e007ab436fb66416009dfb59a8');
	cnn_news=newsapi.get_top_headlines(sources='cnn')
	keys = ['description','source','author','title','url','urlToImage','publishedAt']
	retlist1 = []
	retlist2=[]
	# print(cnn_news)
	# print()
	for news in cnn_news['articles']:
		p=0
		for key in keys:
			if (key not in news) or news[key]==None or len(news[key])==0:
				p = 1
		if p==0: retlist1.append(news)

	# print(retlist1)
	fox_news=newsapi.get_top_headlines(sources='fox-news')
	for news in fox_news['articles']:
		p=0
		for key in keys:
			if (key not in news) or news[key]==None or len(news[key])==0:
				p = 1
		if p==0: retlist2.append(news)

	# print(retlist2)
	headlines = {
	"cnn_news": retlist1,
	"fox_news": retlist2
	}
	
	return jsonify(headlines=headlines)

@app.route('/sliding_headlines',methods = ['POST'])
def sliding_headlines():
	# print("in headlines");
	# newsapi=NewsApiClient(api_key='4dbc17e007ab436fb66416009dfb59a8');
	sliding_news=newsapi.get_top_headlines(language='en');
	keys = ['description','source','author','title','url','urlToImage','publishedAt']
	retlist1 = []
	
	for news in sliding_news['articles']:
		p=0
		for key in keys:
			if (key not in news) or news[key]==None or len(news[key])==0:
				p = 1
		if p==0: retlist1.append(news)
	
	return jsonify(all_articles=retlist1)

@app.route('/word_cloud',methods = ['GET'])
def word_cloud():
	f= open("stopwords_en.txt","r")
	stop_words = f.read()
	print(stop_words)
	# stop_words=['a','an','and','are','as','at','be','but','by','for','if','in','into','is','it','no','not','of','on','or','such','that','the','their','then','there','these','they','this','to','was','will','with']
	punc = "'!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'"
	# newsapi=NewsApiClient(api_key='4dbc17e007ab436fb66416009dfb59a8');
	frequent_news=newsapi.get_top_headlines(language='en');
	text_combined = ''
	freq_words=[]
	for i in frequent_news['articles']:
		s = i['title'].lower()
		table = str.maketrans('', '', string.punctuation)
		stripped = [w.translate(table) for w in s.split()]
		for j in stripped:
			if j not in stop_words:
				if(len(j)):
					freq_words.append(j)

		


	m = Counter(freq_words) 
	most_occur = m.most_common(30) 
	# print(m.most_common(30))

	fin_dict = []
	for ele in most_occur:
		temp = {'word':ele[0],'size':ele[1]*10}
		fin_dict.append(temp)

	# print(fin_dict)

	return jsonify(all_articles=fin_dict)

@app.route('/get_sources',methods = ['POST'])
def get_sources():
	# newsapi =NewsApiClient(api_key='4dbc17e007ab436fb66416009dfb59a8');
	category = request.form['category'];
	# print(category);
	# if category=="all":
	# 	sources=newsapi.get_sources();
	# else:
	source_list=[]
	
	if(category=='all'):
		sources=newsapi.get_sources(language='en');
		
	else:
		sources=newsapi.get_sources(language='en',category=category);
		


	# print(len(source_list));
	return jsonify(sources=sources)

@app.route('/get_default_sources',methods = ['POST'])
def get_default_sources():
	sources=newsapi.get_sources(language='en');
	return jsonify(sources=sources)
	
if __name__ == "__main__":
	app.run(debug = True)