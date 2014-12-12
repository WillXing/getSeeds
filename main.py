# -*- coding: utf-8 -*-
# -*- Call me god father, and you can get your seed -*-

import urllib2
import urllib
import re
import thread
import os


class CL_spider:

    def __init__(self):
        self.y=""
        self.movies = []

    def start(self, host, correction, startPage, endPage):
        self.host = host
        self.mainUrl = host + 'index.php'
        self.correction = correction
        self.startPage = startPage
        self.endPage = endPage
        self.enter_the_main_page()
        
    def enter_the_main_page(self):
        req = urllib2.Request(self.mainUrl)
        resp = urllib2.urlopen(req)
        mainPage = resp.read()

        urlList = re.findall(u'<tr.*?tr3 f_one.*?>.*?<th.*?<a.*?href="(.*?)".*?target="_blank".*?</a>.*?</th>.*?</tr>', mainPage, re.S)
        if(self.correction == 1):
            self.subUrl = self.host + urlList[1]
        else:
            self.subUrl = self.host + urlList[0]

        for pCount in range(self.startPage, self.endPage+1):
            self.subUrl = self.subUrl + "&search=&page=" + str(pCount)
            self.enter_the_sub_page()

    def enter_the_sub_page(self):
        req = urllib2.Request(self.subUrl)
        resp = urllib2.urlopen(req)
        subPage = resp.read()
        
        movieList = re.findall(u'<tr.*?<h3.*?<a.*?href="(.*?)".*?target="_blank".*?>\[.*?\](.*?)</a>.*?</h3>.*?</tr>', subPage, re.S)

        del movieList[0]
        for movie in movieList:
            self.movies.append([self.host + movie[0], movie[1]])
        
        self.enter_the_movie_page(0,len(self.movies))

    def enter_the_movie_page(self, startPos, endPos):
        for iCount in range(startPos, endPos):
            req = urllib2.Request(self.movies[iCount][0])
            resp = urllib2.urlopen(req)
            moviePage = resp.read()
            downloadUrl = re.findall(u'(http://www.rmdown.com/link.php\?hash=.*?)</a>', moviePage, re.S)
            length = len(downloadUrl)
            if(length != 0):
                print "Downloading: "+self.movies[iCount][1]
                try:
                    self.down_load_the_seed(downloadUrl[0], self.movies[iCount][1])
                    print "success"
                except :
                    print "this one fail"
        
        
    def down_load_the_seed(self, referer, title):
        url = 'http://www.rmdown.com/download.php'
        
        req = urllib2.Request(referer)

        resp = urllib2.urlopen(req)
        data = resp.read()
        res = re.findall("<FORM.*?action='download.php'.*?<INPUT.*?name=\"ref\".*?value=\"(.*?)\".*?<INPUT.*?NAME=\"reff\".*?value=\"(.*?)\".*?</FORM>", data, re.S)

        postValue = {'ref':res[0][0]
                     ,'reff':res[0][1]
                     }
        postData = urllib.urlencode(postValue)
        
        reqDown=urllib2.Request(url, postData)

        respDown = urllib2.urlopen(reqDown)

        dataDown = respDown.read()

        downloadPath='./caoliuseed/'
        
        title = title.replace('\\','-').replace('/','-')
        if not os.path.isdir(downloadPath):
            os.makedirs(downloadPath)
        with open(downloadPath + title + '.torrent', 'wb') as code:
            code.write(dataDown)
        

print u"""  
---------------------------------------  
   程序：CL爬虫  
   版本：0.1  
   作者：Xing 
   操作：按提示操作
   注意：本程序没有异常处理，鲁棒性不强，请不要乱操作~~~~
   温馨提示：片是人家拍的，身体是自己的
---------------------------------------  
"""  

print u"""
少年你要看有码还是无码？
0,无码
1,有码
"""
correction = raw_input()
correction = int(correction)
print u"""
你想从第几页开始看？
（请输入数字）
"""
startPage = raw_input()
startPage = int(startPage)
print u"""
你想看到第几页？
（请输入数字）
"""
endPage = raw_input()
endPage = int(endPage)

if(correction == 1):
    print "你选择了【有码】，从第"+str(startPage)+"页到第"+str(endPage)+"页"
else:
    print "你选择了【无码】，从第"+str(startPage)+"页到第"+str(endPage)+"页"
print u"""
----------------------------------------------------------------
开始爬行~!况且况且况且
----------------------------------------------------------------
"""

mySpider = CL_spider()
mySpider.start('http://caoliu2014.com/',correction, startPage, endPage)

print u"""
----------------------------------------------------------------
看看'caoliuseed'文件夹下面有木有好东西
----------------------------------------------------------------
"""


