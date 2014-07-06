# -*- coding: utf-8 -*-
"""
Created on Sat Jul 05 16:01:14 2014

@author: Chengcheng


"""

from TwitterFilter import TwitterFilter
from key import *
import codecs
import tweepy

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

tfilter = TwitterFilter()

availablelist = [u'class1',u'class2',u'class3']

def gettweetlist(listowner, listname):
    tweettable = {}
    for mem in tweepy.Cursor(api.list_members, owner_screen_name=listowner,slug=listname).items():
        tl = mem.timeline(count=100)
        tweetlst = []
        for itm in tl:
            content = tfilter.parse(itm.text)
            if content.content!=u"":
                tweetlst.append(content.content)
        if len(tweetlst)!=0:
            tweettable[mem.screen_name]=tweetlst
    return tweettable
    
def gettweetpool():
    (utf8_encoder, utf8_decoder, utf8_reader, utf8_writer) = codecs.lookup('utf-8')
    fw = utf8_writer(open('data/train','w'))
    for itm in availablelist:
        table = gettweetlist(u'wattlebird_01',itm)
        for tweet in table.values():
            fw.write(tweet+u'\n')
    fw.close()
    
def gettweetuser(uid):
    usr = api.get_user(uid)
    tl = usr.timeline(count=100)
    tweetlst = []
    for itm in tl:
        content = tfilter.parse(itm.text)
        if content.content!=u"":
            tweetlst.append(content.content)
    if len(tweetlst)!=0:
        return tweetlst
    else:
        return None
    