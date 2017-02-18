#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

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
	new_tweets = api.user_timeline(screen_name = screen_name,count=2)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
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


import json
from watson_developer_cloud import ToneAnalyzerV3


if __name__ == '__main__':
	#pass in the username of the account you want to download
	tweets = get_all_tweets("koush")

	out = open('jsonDumpSwapnilsGuy.txt', 'w')
	for tweetblock in tweets:
		tweet = tweetblock[2]
		out.write(tweet)
		print tweet

		tone_analyzer = ToneAnalyzerV3(
			username='91c31290-336f-4443-b0f7-372ef802e513',
			password='yzLUszcd3pXm',
			version='2016-05-19 ')
		out.write(json.dumps(tone_analyzer.tone(text=tweet), indent=2))
		print "result written"

	out.close()