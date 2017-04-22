import tweepy
from tweepy import OAuthHandler
import csv
import cv2
import numpy as np
import sys
import random
import math
import glob
import os
import io
import re
import string
import operator
import itertools
from collections import Counter
from collections import defaultdict 
import json
import urllib2
 
consumer_key = 'wluJ7ioGkGH13LSSe0mPdZz3d'
consumer_secret = 'Ty2Wz9jVPJel0WB4xZPLUhlTUhiw8FUfMTztnIeqT26SmTlbAS'
access_token = '201213497-5NRIqeKoMvh4Q2Tso24JAXXUyHnRoXeNqw910Gu1'
access_secret = 'kHfIBIPAx9V7Tr5zRPHrzJfy0azzmOehykOIgJN8msYs0'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)


def test():
	for status in tweepy.Cursor(api.home_timeline).items(10):
		print("status: ")
		print(status.text)
		print("\n")


def processTweet(tweet):
	print tweet
	tweet = tweet.lower()
	tweet = re.sub('[\s]+', ' ', tweet)	#remove extra whitespaces
	tweet = re.sub(r'#([^\s]+)', r'\1', tweet) #replace #word with word
	tweet = tweet.strip('\'"')	#trim
	return tweet


def get_all_tweets(screen_name):
	#will get most recent 3240 tweets
	allTweets = []	
	
	#make initial request ,200 is max count
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	for tweet in new_tweets:
		tweet = processTweet(tweet)
	allTweets.extend(new_tweets)
	last_pos = allTweets[-1].id - 1
	
	while len(new_tweets) > 0:
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=last_pos)
		for tweet in new_tweets:
			tweet = processTweet(tweet)
		allTweets.extend(new_tweets)
		last_pos = allTweets[-1].id - 1
		
	print "... %s tweets downloaded for the given user" % (len(allTweets))
	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in allTweets]
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	pass


if __name__ == '__main__':
	uName = "DrumilDeshpande"
	get_all_tweets(uName)
