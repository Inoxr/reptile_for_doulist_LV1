# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 13:59:21 2017

@author: pc
"""
#看不懂JS
import urllib
import urllib2
from bs4 import BeautifulSoup
import operator

class Movie:
    def __init__(self,startURL='https://www.douban.com/doulist/13704241/?start=0&sort=seq&sub_type='):
        self.url=startURL#
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : user_agent }     #
        self.dataSet={}
    def getPage(self):   # page start witch 0
        pageURL=self.url
        try:
            request=urllib2.Request(pageURL,headers=self.headers)
            response=urllib2.urlopen(request)
            html=response.read().decode('utf-8')
            soup=BeautifulSoup(html, "lxml")  # , "lxml"  !
            print 'page get'
            return soup  #souo++
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason   
    def getURLs(self,soup):
        urlData=[]
        soupU=soup.find_all('div',{'class':'title'})
        for i in soupU:
            nameFORself=i.get_text().strip()
            urlData.append([i.a['href'],nameFORself])
            self.dataSet[nameFORself]={}
        return urlData
    def getoneMovie(self,urlData,getTDL=False):
        #oriNum=len(self.dataSet.keys())######
        for u in urlData:
            OM=oneMovie()
            try:
                soupI,name=OM.getInf(OM.getInfPage(u[0]))
                OM.getDEA(soupI) #DataSet complete
                if getTDL:
                    OM.getTTL(soupI)    #  whether to get type,date,long
                self.dataSet[name]=OM.dataSet
            except:
                print 'there is no information about ',u[1],'     <---'
                
        #print len(self.dataSet.keys()),' ->',len(self.dataSet.keys())==oriNum  #####  judgement
    def turnNext(self,soup):
        nextS=soup.find_all('span',{'class':'next'})
        try:
            findHref=nextS[0].a['href']
            return findHref
        except:
            return False
        
    def start(self,filename,getTDL=False):
        soup=self.getPage()
        nextPage=self.turnNext(soup)
        while 1:
            dd=self.getURLs(soup)
            self.getoneMovie(dd,getTDL)
            self.url=nextPage
            if self.url==False:
                break
            soup=self.getPage()
            nextPage=self.turnNext(soup)
        storeDS(self.dataSet,filename)
    def printDataSet(self):
        for i in self.dataSet.keys():
            print unicode(i)
            for ii in self.dataSet[i].keys():
                print unicode(ii)
                for iii in self.dataSet[i][ii]:
                    print unicode(iii),
                print '\n'
            print '----------------------------------<>--'

def countDEA(dataSet):
    dataD={}
    dataE={}
    dataA={}
    for i in dataSet.keys():
        if dataSet[i].has_key('director'):
            for d in dataSet[i]['director']:
                dataD[d]=dataD.get(d,0)+1
        if dataSet[i].has_key('editor'):
            for e in dataSet[i]['editor']:
                dataE[e]=dataE.get(e,0)+1
        if dataSet[i].has_key('actor'):
            for a in dataSet[i]['actor']:
                dataA[a]=dataA.get(a,0)+1
    sortD=sorted(dataD.iteritems(),key=operator.itemgetter(1),reverse=True)
    sortE=sorted(dataE.iteritems(),key=operator.itemgetter(1),reverse=True)
    sortA=sorted(dataA.iteritems(),key=operator.itemgetter(1),reverse=True)  
    return sortD,sortE,sortA
def printTop10_DEA(D,E,A):
    print 'top 10 director         <---'
    for i in D[:10]:
        print i[0],i[1]
    print 'top 10 editor           <---'
    for i in E[:10]:
        print i[0],i[1]
    print 'top 10 actor            <---'
    for i in A[:10]:
        print i[0],i[1]
    
def storeDS(DS,filename):
    import pickle
    fw=open(filename,'w')
    pickle.dump(DS,fw)
    fw.close()
def grabDS(filename):
    import pickle
    fr=open(filename)
    return pickle.load(fr)
def remindMe(mode='hard'):
    import pygame
    fileMUS=r'C:\Users\pc\Desktop\Long_long_ago\MUS\.mp3'
    fileMUS=fileMUS[:-4]+mode+fileMUS[-4:]
    pygame.mixer.init()
    pygame.mixer.music.load(fileMUS)
    pygame.mixer.music.play()
    try:
        input('Job is Over\nplease stop\n')
    except:
        pass
    pygame.mixer.music.stop()
##########################################################               
class oneMovie(Movie):
    def getInfPage(self,trueURL):
        try:
            request=urllib2.Request(trueURL,headers=self.headers)
            response=urllib2.urlopen(request)
            html=response.read().decode('utf-8')
            soup=BeautifulSoup(html, "lxml")  # , "lxml"  !
            print 'page get'
            return soup  #souo++
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason   
    def getInf(self,soup):
        self.getS(soup)
        soupI=soup.find_all('div',{'id':'info'})
        soupI=soupI[0]
        fff=soup.find('span',{'property':'v:itemreviewed'})
        print fff.get_text()#####
        return soupI,fff.get_text()
    def getDEA(self,soupI):
        soupDEA=soupI.find_all('span',{'class':"attrs"})
        dSkey=['director','editor','actor']
        ik=0
        for i in soupDEA:
            dataOne=[]
            for ii in i.contents:
                try:
                    dataOne.append(ii.get_text())
                except:
                    pass
            self.dataSet[dSkey[ik]]=dataOne
            ik+=1
        if(len(soupDEA)<>3):
            print "DEA error!",len(soupDEA),'               <---'
        return 
    def getS(self,soup):
        #soupS=soup.find_all('div',{'class':'rating_wrap clearbox'})
        dSkey=['totalScore','num','five','four','three','two','one']
        dataOne={}
        try:
            ff=soup.find('span',{'property':'v:votes'})
            dataOne[dSkey[1]]=ff.get_text()
        except:
            print 'not showed                             <---'
            return
        dataOne[dSkey[0]]=float(soup.find_all('strong',{'class':'ll rating_num'})[0].get_text())
        soupR=soup.find_all('span',{'class':'rating_per'})
        ii=2
        for i in soupR:
            dataOne[dSkey[ii]]=float(i.get_text()[:-1])
            ii+=1
        self.dataSet['score']=dataOne
        
    def getTTL(self,soupI):#type,time,long
        try:
            Type=soupI.find_all('span',{'property':'v:genre'})
            dataType=[i.get_text() for i in Type]
            self.dataSet['Type']=dataType
        except:
            print 'no Type                   <---'
        try:
            Time=soupI.find_all('span',{'property':'v:initialReleaseDate'})[0].get_text()
            self.dataSet['Date']=Time
        except:
            print 'no Date                   <---'
        try:
            Long=soupI.find_all('span',{'property':'v:runtime'})[0].get_text()[:-3]
            self.dataSet['Long']=Long
        except:
            print 'no Long                   <---'
        
       
#==============================================================================
# ex=Movie('https://www.douban.com/doulist/13704241/?start=0&sort=seq&sub_type=')
# ex.start('ex.txt')
#==============================================================================


