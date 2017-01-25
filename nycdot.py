"""
----------------------------------------------------------------------
Name of website: NYC_dotsignals (http://dotsignals.org/)
Author of code: Ajay Gopakumar, guide used made by Ryan Dailey
Contact info: agopakum@purdue.edu
Description: Parsing the NYC camera Website (http://dotsignals.org/)
Command to run script: nycdot
Input file format: This script has no input file

Other files required by this script: This code requires PhantomJS a headless wen browser
                                    found at https://nodejs.org/en/
----------------------------------------------------------------------
"""
from bs4 import BeautifulSoup
import urllib2
import re
import time
import json
import pprint
import platform
from selenium import webdriver
import sys
import codecs


if platform.system() == 'WIndows':
    PHANTOMJS_PATH = './phantomjs.exe'
else:
    PHANTOMJS_PATH = './phantomjs'
browser = webdriver.PhantomJS(PHANTOMJS_PATH)

def nycdot():
    jsonURL = "http://dotsignals.org/new-data.php" #URL to the JSON file containing camera data
    CameraPopupURL = "http://dotsignals.org/google_popup.php?cid=" #URL to access the camera URL
    #f = open('nycdot_cameralist','wb') #Output file
    f = codecs.open('nycdot_cameralist','w', encoding='utf8') #Python2.7's open function does not transparently handle unicode characters like python3 does.

    #header info to file
    f.write("description#snapshot_url#latitude#longitude#country#city\n")

    #Load JSON file
    jsondata = urllib2.urlopen(jsonURL).read()

    #Parse Json file
    parsed_json = json.loads(jsondata)
    

    cameras = parsed_json['markers'] #access markers key

    for data in cameras:
        cam_id = data['id']
        content = data['content']
        latitude = data['latitude']
        longitude = data['longitude']
        url = CameraPopupURL + cam_id

        browser.get(url)
        soup = BeautifulSoup(browser.page_source)
        snapshot_url=soup.find('img').get('src')
        print snapshot_url.encode('utf-8')
       
       
        #soup = BeautifulSoup(urllib2.urlopen(url).read())
        #img = soup.find('img')
        #print img
        if re.search(r'img/inactive',snapshot_url) == None:
            snapshot_url = re.search(r'(?P<URL>[\w\.\/:\\]*)',snapshot_url).group('URL')
            f.write(content+"#"+snapshot_url.encode('utf-8').strip()+"#"+latitude+"#"+longitude+"#"+"USA#NY#New York\n")
        pass



        
    f.close()
    return

if __name__ == '__main__':
    nycdot()
