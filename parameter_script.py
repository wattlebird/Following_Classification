# -*- coding: utf-8 -*-
"""
Created on Thu Jul 10 21:38:31 2014

@author: Chengcheng
"""

from pnn import pnn
import codecs
import pickle

fb = open('data/classify.dat','rb')
tweetinfo = pickle.load(fb)
fb.close()

(utf8_encoder, utf8_decoder, utf8_reader, utf8_writer) = codecs.lookup('utf-8')
fw = utf8_writer(open('data/classify_result','w'))

model = pnn()

for itm in tweetinfo:
    fw.write(u'%s\t%s\t%d\n'%(itm[0],itm[1],model.classify(itm[3])))

fw.close()