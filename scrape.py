#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from termcolor import colored
<<<<<<< HEAD

=======
>>>>>>> ff8614cfda98690dfe932a1f36b96e6e6683c543

sns.set(style='ticks', palette='Set2')


#Twitter API credentials
consumer_key = "F3HRVhBsGeTXEmaI2pr19AvnO"
consumer_secret = "fjU4SLZayBBcYkIJHaFFXpRRH0kxR0uISMnPYOGXjwB66UMWvW"
access_key = "276380747-eIovsf6m2KP6HuETAURXdebTxiCrcat88gK2ODGq"
access_secret = "NNwbuBsWOipEhKl1Kf7M5FglVd89axMGbIaNvzPme3Phk"

headers = (["handle","time","tweet"])


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(alltweets) < 10:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	# for tweet in tweepy.Cursor(api.search,q="*",count=100,geocode="5.29126,52.132633,150km").items(100):
	# 	print [tweet.created_at,tweet.user.id, tweet.geo, tweet.text.encode('utf-8')]
    
	outtweets = []

	for tweet in alltweets:
		if (not tweet.retweeted) and ('RT @' not in tweet.text):
			outtweets.append([screen_name, tweet.created_at, tweet.text.encode("utf-8")])
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'awb') as f:
		writer = csv.writer(f)
		writer.writerow(headers)
		# writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)

	return outtweets


def findEmotion(tonearray):
	maximum = 0
	name = ""
	for emotion in tonearray:
		if emotion['score'] > maximum:
			maximum = emotion['score']
			name = emotion["tone_name"]

	if name == "" or maximum < 0.5:
		return "Neutral"
	else:
		return name


import json
from watson_developer_cloud import ToneAnalyzerV3

def generateFrequencies(timeline, divisions):
	endtime = timeline[0][0]
	starttime = timeline[len(timeline) - 1][0]
	diff = endtime - starttime
	sampledistance = diff / divisions
	samplesize = 2 * sampledistance

	results = []
	for i in range(divisions):
		ngood = 0
		nbad = 0
		ratio = 0.0
		previous = 0.5
		for entry in timeline:
			if entry[0] < endtime - (samplesize * (i) - sampledistance):
				break
			elif endtime - (samplesize * i) <= entry[0]:
				if entry[1] == "Neutral":
					pass
				elif entry[1] == "Joy":
					ngood += 1
				else:
					nbad += 1
		if ngood > 0 and nbad > 0:
			ratio = (ngood) / float(nbad + ngood)
		elif ngood > 0:
			ratio = 1
		elif nbad > 0:
			ratio = 0
		else:
			ratio = previous
		previous = ratio
		results.append((endtime - (samplesize * i), ratio))
	return results

def analyzer(messages):
		#pass in the username of the account you want to download
		results = []

		out = open('jsonDumpSwapnilsGuy.txt', 'w')
		plt.ion()
		plt.show()
		for message in messages:
			tweet = message[2]
			try:
				out.write(tweet)
			except UnicodeEncodeError:
				pass	
			print tweet

			tone_analyzer = ToneAnalyzerV3(
				username='91c31290-336f-4443-b0f7-372ef802e513',
				password='yzLUszcd3pXm',
				version='2016-05-19 ')
			tone = tone_analyzer.tone(text=tweet)
			tone_types = tone["document_tone"]["tone_categories"][0]["tones"]
			results.append(((message[1] - datetime.datetime(1970,1,1)).total_seconds(), findEmotion(tone_types)))
			final = generateFrequencies(results, 20)
			print final
			finalresult = []
			for item in final:
				finalresult.append(item[1])
			plt.plot(finalresult)
			plt.pause(0.001)
			plt.draw()
			plt.clf()
		

		out.close()

# analyzer(get_all_tweets("koush"))	
