# -*- coding: utf-8 -*-
"""
Created on Sat Jul 05 13:59:31 2014

@author: Chengcheng
"""

from snownlp import SnowNLP
import codecs
import pickle
import os
import re

class pnn:
    def __init__(self):
        self.featuretable = {}
        if os.path.exists('data/dict.dat'):
            fd = open('data/dict.dat','rb')
            self.featuretable = pickle.load(fd)
        
    def trainsample(self):
        None
    
    def classify(self):
        None
    
    def trainfeature(self, filepath):
        (utf8_encoder, utf8_decoder, utf8_reader, utf8_writer) = codecs.lookup('utf-8')
        fd = utf8_reader(open(filepath))
        tweetlist = fd.readlines()
        fd.close()
        VALID_EXP = ur'([A-Za-z\u4e00-\u9fa5]+)'
        VALID_REGEX = re.compile(VALID_EXP)
        for tweet in tweetlist:
            s=SnowNLP(tweet)
            s=SnowNLP(s.han)
            keys = s.keywords(3)
            for wd in keys:
                mtch = VALID_REGEX.search(wd)
                if mtch is None:
                    continue
                else:
                    wd = mtch.group(0)
                if self.featuretable.has_key(wd):
                    continue
                else:
                    self.featuretable[wd]=len(self.featuretable)+1
        fd = open('data/dict.dat','wb')
        pickle.dump(self.featuretable,fd)
        fd.close()
