# -*- coding: utf-8 -*-
"""
Created on Sat Jul 05 08:31:04 2014

@author: Chengcheng
"""

import TweetFilter
import codecs

(utf8_encoder, utf8_decoder, utf8_reader, utf8_writer) = codecs.lookup('utf-8')
fd = utf8_reader(open('data/class1'))
fw = utf8_writer(open('data/testwrite','w'))

tfilter = TweetFilter.TweetFilter()

while True:
    sentense = fd.readline()
    if sentense == u'':
        break
    content = tfilter.parse(sentense)
    if content.content!=u'':
        fw.write(content.content.strip()+u'\n')
    
fd.close()
fw.close()
