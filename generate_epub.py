#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pymongo
import gridfs
import pyquery
import time
from ebooklib import epub


def main():
    db = pymongo.MongoClient().aaronsw
    fs = gridfs.GridFS(db)
    filenames = fs.list()
    remove_comments = False

    book_title = 'Aaron_Swartz_-_Raw_Thought'
    book = epub.EpubBook()
    book.set_identifier('rawthought' + `time.time()`)
    book.set_title(book_title)
    book.set_language('en')
    book.add_author('Aaron Swartz')

    chapters = []
    for filename in filenames:
        gridout = fs.get_last_version(filename)
        pq = pyquery.PyQuery(gridout.read())
        cq = pq('.content')
        title = cq('h1:first').text()
        if not title:
            continue
        cq('script').remove()
        cq('form').remove()
        if(remove_comments):
            cq('#comments_body').remove()
        content = cq.html()

        chapter = epub.EpubHtml(title = title, file_name = filename[filename.rfind('/') + 1:] + '.xhtml', lang = 'en')
        chapter.content = content
        book.add_item(chapter)
        chapters.append(chapter)

    book.toc = tuple(chapters)
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = chapters
    epub.write_epub(book_title + '.epub', book, {})

if __name__ == '__main__':
    main()
