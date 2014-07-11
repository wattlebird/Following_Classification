# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 19:13:57 2014

@author: Chengcheng
"""

import tweepy
import gettweets
from key import *
import codecs
from pnn import pnn
import pickle

fw = open('data/classify.dat','wb')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

model = pnn()
wholedata = []

foinglst = api.friends_ids('wattlebird_01')

for itm in foinglst:
    usr = api.get_user(itm)
    speechlst = gettweets.gettweetuser(itm)
    if speechlst!=None:
        wholedata.append((usr.screen_name,usr.name,speechlst))

        
pickle.dump(wholedata,fw)
fw.close()