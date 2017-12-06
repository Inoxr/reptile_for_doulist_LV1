# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 20:02:40 2017

@author: pc
"""

import doubanMovie as DM  #grabDS(filename)

DS=DM.grabDS('TOP100_Chinese.txt')
D,E,A=DM.countDEA(DS)
DM.printTop10_DEA(D,E,A)


