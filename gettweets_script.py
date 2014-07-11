# -*- coding: utf-8 -*-
"""
Created on Wed Jul 02 15:24:02 2014

@author: Chengcheng
"""

import tweepy
import TweetFilter
from key import *
import codecs

(utf8_encoder, utf8_decoder, utf8_reader, utf8_writer) = codecs.lookup('utf-8')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
tfilter = TweetFilter.TweetFilter()

fw = utf8_writer(open('data/train','w'));
classlist = ('class1', 'class2', 'class3')

for itm in classlist:
    for mem in tweepy.Cursor(api.list_members, owner_screen_name='wattlebird_01',slug=itm).items():
        tl = mem.timeline(count=100)
        for itm in tl:
            content = tfilter.parse(itm.text)
            ct = content.content.strip()
            if ct!=u'':
                fw.write(ct + u'\n')

fw.close()