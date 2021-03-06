#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
from termcolor import colored

#Twitter API credentials
consumer_key = "F3HRVhBsGeTXEmaI2pr19AvnO"
consumer_secret = "fjU4SLZayBBcYkIJHaFFXpRRH0kxR0uISMnPYOGXjwB66UMWvW"
access_key = "276380747-eIovsf6m2KP6HuETAURXdebTxiCrcat88gK2ODGq"
access_secret = "NNwbuBsWOipEhKl1Kf7M5FglVd89axMGbIaNvzPme3Phk"

def get_all_tweets(screen_name, numberoftweets):
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
	while len(new_tweets) > 0 and len(alltweets) <= numberoftweets:
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
	outtweets = []

	for tweet in alltweets:
		if (not tweet.retweeted) and ('RT @' not in tweet.text):
			outtweets.append([screen_name, tweet.created_at, tweet.text.encode("utf-8")])
	
	return outtweets


def findEmotion(tonearray):
	maximum = 0
	name = ""
	for emotion in tonearray:
		if emotion['score'] > maximum:
			maximum = emotion['score']
			name = emotion["tone_name"]

	if name == "" or maximum < 0.6:
		return "Neutral"
	else:
		return name


import json
from watson_developer_cloud import ToneAnalyzerV3

def generateFrequencies(timeline, divisions):
	endtime = timeline[0][0]
	starttime = timeline[len(timeline) - 1][0]
	diff = endtime - starttime
	sampledistance = diff / float(divisions)
	samplesize = 2 * sampledistance

	results = []
	for i in range(divisions):
		ngood = 0
		nbad = 0
		ratio = 0.0
		for entry in timeline:
			# if entry[0] < (endtime - samplesize * (i)) - sampledistance:
			# 	break
			if endtime - (samplesize * i) >= entry[0]:
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
			pass
		results.append(ratio)
	return results

def analyzer(messages, name):
		#pass in the username of the account you want to download
		results = []
		sns.set(style='ticks', palette='Set2')
		plt.ion()
		plt.show()
		for message in messages:
			tweet = message[2]

			tone_analyzer = ToneAnalyzerV3(
				username='91c31290-336f-4443-b0f7-372ef802e513',
				password='yzLUszcd3pXm',
				version='2016-05-19 ')
			tone = tone_analyzer.tone(text=tweet)
			tone_types = tone["document_tone"]["tone_categories"][0]["tones"]



			emotion = findEmotion(tone_types)
			results.append(((message[1] - datetime.datetime(1970,1,1)).total_seconds(), emotion))

			if emotion == "Joy":
				print colored(tweet, "green")
			elif emotion == "Neutral":
				print colored(tweet, "white")
			else:
				print colored(tweet, "red")

			final = generateFrequencies(results, 20)
			finalresult = []
			for item in final:
				finalresult.append(item)
			plt.clf()
			plt.ylabel("Emotional Ratio Joy/Emotions")
			plt.ylim(-1.1, 1.1)
			plt.suptitle(name, fontsize = 30)
			plt.plot([0]*len(finalresult))
			plt.plot(map(lambda x: (x - 0.5) * 2, finalresult))
			plt.pause(0.001)
			plt.draw()
		
# analyzer(get_all_tweets("koush"))	
def plot(input):
	plt.plot(finalresult)
	plt.pause(0.001)
	plt.draw()

def clear():
	plt.clf()