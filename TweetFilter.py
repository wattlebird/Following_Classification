# -*- coding: utf-8 -*-
"""
Created on Thu Jul 03 21:15:48 2014

@author: Chengcheng
"""

import re

AT_SIGNS = ur'[@\uff20]'
HASH_SIGNS = ur'[#\uff03]'
UTF_CHARS = ur'a-zA-Z0-9_\u00c0-\u00d6\u00d8-\u00f6\u00f8-\u00ff'
SPACES = ur'[\u0020\u00A0\u1680\u180E\u2002-\u202F\u205F\u2060\u3000]'

USER_STR = ur'\B'+AT_SIGNS+ur'([a-zA-Z0-9_]{1,15})'
USER_REGEX = re.compile(USER_STR)

HASHTAG_STR = ur'[^\w&]'+HASH_SIGNS+ur'([\w]+\b)'
HASHTAG_REGEX = re.compile(HASHTAG_STR, re.UNICODE)

URL_REGEX = re.compile(ur'(https?://[A-Za-z0-9~;/?:@=&$-_.+!*\'(),%]*)')

RETWEET_REGEX = re.compile(ur'(RT\s?@([a-zA-Z0-9_]{1,15}).*$)')
FORWARD_REGEX = re.compile(ur'\u0022'+USER_STR+ur'.*\u0022|“'+USER_STR+ur'.*”')

TAGS_AUTO_LIST = ('ifttt','Tweet4China','asbot')

class TweetContent:
    
    ''' A class that contains all the necessary information for syntax parsing
    
    Attributes:
    - content: real content of a tweet.
    - mentioned_users: all the mentioned users, in the form of a list of strings
    - hashtags: all the hashtags, in the form of a list of strings
    
    Methods:
    - isvalid(): whether the real content of the tweet exists.
    - isretweet(): whether the tweet is a retweet.
    '''
    
    def __init__(self, content, mention, hashtags, rtflag):
        self.content = content if content else u""
        self.mention = mention if mention else []
        self.hashtags = hashtags if hashtags else []
        self.rtflag = False
    
    def isvalid(self):
        return self.content == u""
    
    def isrewteet(self):
        return self.rtflag

class TweetFilter:
    
    '''Tweet filter trys to get the real content and meaningful sentenses in a real-situation tweet.'''
    
    def parse(self,sentense):
        mentions = USER_REGEX.findall(sentense) #return a list of groups
        
        mtch = RETWEET_REGEX.match(sentense)
        if(mtch != None):
            content = u""
            rtflag = True
        else:
            embedmtch1 = RETWEET_REGEX.search(sentense)
            embedmtch2 = FORWARD_REGEX.search(sentense)
            if (embedmtch1 == None and embedmtch2 != None):
                content = sentense[:embedmtch2.start()]+sentense[embedmtch2.end():]
            elif (embedmtch2 == None and embedmtch1 != None):
                content = sentense[:embedmtch1.start()]+sentense[embedmtch1.end():]
            elif (embedmtch2 != None and embedmtch1 != None):
                len1 = embedmtch1.end()-embedmtch1.start()
                len2 = embedmtch2.end()-embedmtch2.start()
                if(len2>len1):
                    content = sentense[:embedmtch2.start()]+sentense[embedmtch2.end():]
                else:
                    content = sentense[:embedmtch1.start()]+sentense[embedmtch1.end():]
            else:
                content = sentense
            rtflag = False
        
        hashlst = HASHTAG_REGEX.findall(content)
        #look for if the hashlst contains auto tweet hashtags
        for hashitm in hashlst:
            try:
                TAGS_AUTO_LIST.index(hashitm)
                content = u""
                break
            except ValueError:
                continue
            
        if content == u"":
            return TweetContent(content,mentions,hashlst,rtflag)

        content = content.replace(u'#',u' ')
        content = URL_REGEX.sub(u' ',content)
        content = re.sub(USER_STR+ur':?',u'',content)
        
        return TweetContent(content,mentions,hashlst,rtflag)
    