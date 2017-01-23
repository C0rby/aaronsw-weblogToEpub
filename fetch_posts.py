#!/usr/bin/env python
# -*- coding: utf-8 -*-


import crawler
import time
from data import Storage
from pymongo import MongoClient
import gridfs
import requests
import logging

def main():
    with open("article_links") as f:
        links = f.readlines()

    db = MongoClient().aaronsw
    bucket = gridfs.GridFSBucket(db)

    for link in links:
        html = html(link)
        bucket.upload_from_stream(
            link,
            html.encode('utf-8', 'strict'),
            metadata={"contentType": "text/html"}
        )
        time.sleep(10) # pause between requests

def html(url):
    response = requests.get(url)
    if response.status_code != 200:
        logging.warning("Uh oh. got status " + `response.status_code`)
    return requests.get(url).text

if __name__ == "__main__":
    main()
