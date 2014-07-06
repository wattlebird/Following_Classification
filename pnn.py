# -*- coding: utf-8 -*-
"""
Created on Sat Jul 05 13:59:31 2014

@author: Chengcheng
"""

from snownlp import SnowNLP
import gettweets
import numpy
import codecs
import pickle
import os
import re


class pnn:
    def __init__(self):
        self.featuretable = {}
        self.sigma = 0.3
        if os.path.exists('data/dict.dat'):
            fd = open('data/dict.dat','rb')
            self.featuretable = pickle.load(fd)
            fd.close()
        if os.path.exists('data/para.dat'):
            fd = open('data/para.dat','rb')
            self.m_feature_to_mode = pickle.load(fd)
            self.m_mode_to_class = pickle.load(fd)
            
    def __del__(self):
        if len(self.featuretable)!=0:
            fw = open('data/dict.dat','wb')
            pickle.dump(self.featuretable,fw)
            fw.close()
        if hasattr(self, 'm_feature_to_mode') and hasattr(self,'m_mode_to_class'):
            fw = open('data/para.dat','wb')
            pickle.dump(self.m_feature_to_mode,fw)
            pickle.dump(self.m_mode_to_class,fw)
            fw.close()
        
    def trainsample(self):
        table = gettweets.gettweetlist(u'wattlebird_01',u'class1')
        for v in table.values():
            self._add_sample(v,0)
        table = gettweets.gettweetlist(u'wattlebird_01',u'class2')
        for v in table.values():
            self._add_sample(v,1)
        table = gettweets.gettweetlist(u'wattlebird_01',u'class3')
        for v in table.values():
            self._add_sample(v,2)
    
    def classify(self,tweets):
        f = self._tweet_to_feature(tweets)
        f.shape = (-1,1)
        g = self.m_feature_to_mode.dot(f)
        g.shape = (1,-1)
        h = numpy.dot(numpy.exp((g-1)/self.sigma),self.m_mode_to_class)
        return numpy.argmax(h)
    
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
        
    def _tweet_to_feature(self, tweetlist):
        f = numpy.zeros(len(self.featuretable),dtype=numpy.float64)
        for tweet in tweetlist:
            s = SnowNLP(tweet)
            s = SnowNLP(s.han)
            keys = s.keywords(3)
            for wd in keys:
                if self.featuretable.has_key(wd):
                    f[self.featuretable[wd]-1]+=1
        return f/numpy.sqrt(numpy.dot(f,f))
        
    def _add_sample(self, tweetlist, nclass):
        f = self._tweet_to_feature(tweetlist)
        f.shape = 1,f.shape[0]
        if hasattr(self, 'm_feature_to_mode'):
            self.m_feature_to_mode = numpy.vstack((self.m_feature_to_mode, f))
        else:
            self.m_feature_to_mode = f
        
        if hasattr(self, 'm_mode_to_class'):
            self.m_mode_to_class = numpy.concatenate((self.m_mode_to_class, self._class_vec(nclass)))
        else:
            self.m_mode_to_class = self._class_vec(nclass)
            
            
    def _class_vec(self,nclass):
        if nclass == 0:
            return numpy.array([[1,0,0]])
        elif nclass == 1:
            return numpy.array([[0,1,0]])
        elif nclass == 2:
            return numpy.array([[0,0,1]])
        else:
            return None