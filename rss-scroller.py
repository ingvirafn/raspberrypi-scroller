#!/usr/bin/env python

# pip install feedparser

import logging
import time
import requests
from bs4 import BeautifulSoup

from autoscroller import AutoScroll

# logging.basicConfig(level=logging.INFO)


HN_URL = "https://api.hnpwa.com/v0/news/1.json"
# MBL_RSS_URL = "https://www.mbl.is/feeds/fp/"
MBL_RSS_URL = "https://www.mbl.is/feeds/helst/" # Helstu fréttir

def parseRss(content):
    soup = BeautifulSoup(content, features='xml')
    article_list = []
    articles = soup.findAll('item')
    for a in articles:
        title = a.find('title').text
        link = a.find('link').text
        published = a.find('pubDate').text
        article = {
            'title': title,
            'link': link,
            'published': published
            }
        article_list.append(article)
    return article_list

def getRssNews():
    response = requests.get(MBL_RSS_URL)
    rssItems = parseRss(response.content)
    items = []
    for item in rssItems:
        items.append(item["title"])
    return items


def getHackernewsItems():
    response = requests.get(HN_URL)
    data = response.json()
    items = []
    for item in data:
        items.append(item["title"])
    return items

def getItems():
    return getRssNews()

def main():
    logging.basicConfig(level=logging.INFO)

    autoscroll = AutoScroll()
    autoscroll.startstop()
    logging.info("Still running")
    while True:
        logging.info("Downloading news feed...")
        items = getItems()
        for item in items:
            autoscroll.append(item)
            logging.info(item)

        logging.info("Sleeping for 60secs")
        time.sleep(60)

if __name__ == '__main__':
    main()

