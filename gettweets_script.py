# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 15:24:02 2014

@author: Chengcheng
"""

import tweepy
from key import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

fd = open('data/class1','w');

for mem in tweepy.Cursor(api.list_members, owner_screen_name='wattlebird_01',slug='class1').items():
    tl = mem.timeline(count=100)
    for itm in tl:
        print>>fd,itm.text.encode('utf-8','ignore')

fd.close()