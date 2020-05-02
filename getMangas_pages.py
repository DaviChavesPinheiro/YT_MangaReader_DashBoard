from urllib.request import Request, urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from urllib import parse
from bs4 import BeautifulSoup
import json
import re
from time import sleep
from multiprocessing.pool import ThreadPool
import os.path

def getPagesFromChapter(chapter):
    for i in range(7):
        try:
            if('pages' in chapter):
                print("The Chapter {} already contains pages links. Moving on to the next chapter.".format(chapter['title']))
                return chapter
        
            if('chapterUrl' not in chapter):
                print("The Chapter {} does NOT contains pagesLinks. Moving on to the next chapter.".format(chapter['title']))
                return chapter

            pages = []
            req = Request(chapter['chapterUrl'], headers=headers)
            response = urlopen(req)
            html = response.read()
            soup = BeautifulSoup(html, "html.parser")
            
            for page in soup.find("div", {'id':"capitulos_images"}).select('img'):
                pageUrl = str(page.get('src'))
                pages.append(pageUrl)
            chapter['pages'] = pages
            del chapter['chapterUrl']
            break
        except HTTPError as e:
            print(e.status, e.reason)
            print('An error happened [HTTPError] when opening chapter ({}) page. Trying again [{} of 6]'.format(chapter['title'], index))
            sleep(pow(2, i))
        except URLError as e:
            print(e.reason)
            print('An error happened [URLError] when opening chapter ({}) page. Trying again [{} of 6]'.format(chapter['title'], index))
            sleep(pow(2, i))
        except:
            print('Unknown Error')
            print('An error happened [Unknown] when opening chapter ({}) page. Trying again [{} of 6]'.format(chapter['title'], index))
            sleep(pow(2, i))
    # print('Chapter {} page`s getted.'.format(chapter['title'].split('_')[0]), end=' ')
    return chapter


mangas = []
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
if __name__ == '__main__':
    
    max_chapters = int(input("How many chapters do you want to extract pages from? [0 = Infinity]"))
    if (max_chapters <= 0):
        max_chapters = 9999999
    
    with open('mangas_chapters.json') as json_file:
        mangas = json.load(json_file)
        print("{} Mangas Finded:".format(len(mangas)))
        for index, manga in enumerate(mangas):
            print('-', index, manga['title'])
    print()
    for index, manga in enumerate(mangas):
        print("The manga {} has {} chapters.".format(manga['title'], len(manga['chapters'])))
        manga['chapters'] = manga['chapters'][:max_chapters]
        
        chapters = ThreadPool(len(manga['chapters'])).imap_unordered(getPagesFromChapter, manga['chapters'], chunksize= 6)
        print('Getting Chapters page`s... ')

        for chapter in chapters:
            print(chapter['title'])
            mangas[index]['chapters'][int(chapter['title'].split('_')[0]) - 1] = chapter

        with open('mangas_pages.json', 'w') as outfile:
            json.dump(mangas, outfile)
        print('Manga {} Finished!'.format(manga['title']))
   
    print()
    print('---------------------------END---------------------------')