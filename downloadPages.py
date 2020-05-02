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

def download_pages(args):
    pageIndex, page = args
    # pageIndex = int(str(page).split('_')[0])
    for i in range(6):
        try:
            if path.exists("{}/{}/{}_{}".format(manga['title'], chapter['title'], pageIndex, str(page).split('/')[-1])):
                return "Page {} already exists ".format(str(page).split('/')[-1])
            else:
                url = str(page)
                urlretrieve(url, "{}/{}/{}_{}".format(manga['title'], chapter['title'], pageIndex, str(page).split('/')[-1]))
                return "Page({}) ".format(pageIndex)
        except HTTPError as e:
            print(e.status, e.reason)
            print('An error happened [HTTPError] when downloading Page {}. Trying again [{} of 6]'.format(str(page).split('/')[-1], i + 1))
            sleep(pow(2, i))
        except URLError as e:
            print(e.reason)
            print('An error happened [URLError] when downloading Page {}. Trying again [{} of 6]'.format(str(page).split('/')[-1], i + 1))
            sleep(pow(2, i))
        except:
            print('Unknown Error')
            print('An error happened [Unknown] when downloading Page ({}) page. Trying again [{} of 6]'.format(str(page).split('/')[-1], i + 1))
            sleep(pow(2, i))
    return "ERROR " + page
    
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
    for manga in mangas:
        start_time = time.time()
        print("Downloading Manga {}. This Manga has {} chapters".format(manga['title'], len(manga['chapters'])))
        if not path.exists(manga['title']):
            os.mkdir(manga['title'])
        
        manga['chapters'] = manga['chapters'][:max_chapters]
        
        for index, chapter in enumerate(manga['chapters']):
            start_time_chapter = time.time()
            if not path.exists(manga['title']+'/'+chapter['title']):
                os.mkdir(manga['title']+'/'+chapter['title'])
            print("Downloaded pages: ")
            results = ThreadPool(len(chapter['pages'])).imap_unordered(download_pages, enumerate(chapter['pages']))
            for r in results:
                print(r, end=' ')
            print()
            print("Chapter {}/{} downloaded in {} seconds".format(index, len(manga['chapters']), round(time.time() - start_time_chapter, 2)))
            print('---------------')
            
        print("Finished in {} seconds ({} minutes)".format(round(time.time() - start_time, 2), round((time.time() - start_time) / 60), 2))
        print("------------------------------------------------------------------")

    
    print("End")
