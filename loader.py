# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 20:04:59 2017

@author: pc
"""


import doubanMovie as DM
try:
    a=DM.Movie('https://www.douban.com/doulist/249029/')
    a.start('Cold_but_NotBad_8.4-8.txt',getTDL=True)
    DM.remindMe('aa')
except:
    DM.remindMe('error')
    


