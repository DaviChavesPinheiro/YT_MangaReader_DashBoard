from urllib.request import Request, urlopen, urlretrieve, install_opener, build_opener
from urllib.error import URLError, HTTPError
from urllib import parse
from bs4 import BeautifulSoup
import json
import re
from time import sleep
import os
from os import path
from multiprocessing.pool import ThreadPool
import time


opener = build_opener()
opener.addheaders = [
    ('user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36')]
install_opener(opener)


def download_chapter(chapter):
    start_time = time.time()
    if not path.exists(manga['title']+'/'+chapter['title']):
        os.mkdir(manga['title']+'/'+chapter['title'])
    for pageIndex, page in enumerate(chapter['pages']):
        for i in range(6):
            try:
                if path.exists("{}/{}/{}_{}".format(manga['title'], chapter['title'], pageIndex, str(page).split('/')[-1])):
                    print("Page {} already exists. Moving on to the next page...".format(str(page).split('/')[-1]))
                    break
                else:
                    url = str(page)
                    urlretrieve(url, "{}/{}/{}_{}".format(manga['title'], chapter['title'], pageIndex, str(page).split('/')[-1]))
                    print("Chapter ({}): Page({}) Downloaded.".format(chapter['title'],pageIndex))
                    break
            except HTTPError as e:
                print(e.status, e.reason)
                print('An error happened [HTTPError] when downloading Page {}. Trying again [{} of 6]'.format(str(page).split('/')[-1] ,i + 1))
                sleep(pow(2, i))
            except URLError as e:
                print(e.reason)
                print('An error happened [URLError] when downloading Page {}. Trying again [{} of 6]'.format(str(page).split('/')[-1] ,i + 1))
                sleep(pow(2, i))
    return "Chapter {} Downloaded. ({} pages) in {} seconds".format(chapter['title'], len(chapter['pages']), time.time() - start_time)


mangas = []
max_chapters = 999999999
if __name__ == '__main__':
    print("Start")
    
    max_chapters = int(input('How Many Chapters Do You want to Download? [0 = Infinity] '))
    if max_chapters == 0:
        max_chapters = 999999999
    
    with open('mangas_pages.json') as json_file:
        mangas = json.load(json_file)
        print("{} mangas finded.".format(len(mangas)))
    for index, manga in enumerate(mangas):
        start_time = time.time()
        print("Downloading Manga {}. This Manga has {} chapters".format(manga['title'], len(manga['chapters'])))
        if not path.exists(manga['title']):
            os.mkdir(manga['title'])
        
        manga['chapters'] = manga['chapters'][:max_chapters]
        
        results = ThreadPool(len(manga['chapters'])).imap_unordered(download_chapter, manga['chapters'], chunksize= 10)
        for r in results:
            print(r)
        print("Finished in {} seconds ({} minutes)".format(time.time() - start_time, (time.time() - start_time) / 60))

    
    print("End")
