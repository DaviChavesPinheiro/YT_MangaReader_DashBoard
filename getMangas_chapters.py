from urllib.request import Request, urlopen, urlretrieve
from urllib.error import URLError, HTTPError
from urllib import parse
from bs4 import BeautifulSoup
import json
import re
from time import sleep
from multiprocessing.pool import ThreadPool
import os.path

def getMangaDetails(mangaUrl):
    manga = {}
    manga['url'] = mangaUrl
    req = Request(mangaUrl, headers=headers)
    response = urlopen(req)
    html = response.read()
    soup = BeautifulSoup(html, "html.parser")
    
    manga['title'] = soup.find('h1').getText()
    manga['title'] = re.sub('[^A-Za-z0-9 ]+', '', manga['title'])
    print("Manga Title: {}".format(manga['title']))
    
    chaptersElements = soup.select_one(".chap-holder").select("a")
    chaptersElements.reverse()
    
    manga['chapters'] = []
    print('Chapters getted:          ', end=' ')
    for index, chapterElement in enumerate(chaptersElements):
        chapterUrl = chapterElement.get("href")
        chapterTitle = chapterElement.get("title")
        chapterTitle = re.sub('[^A-Za-z0-9 .]+', '', chapterTitle)
        chapterTitle = "{}_{}".format(index + 1, chapterTitle)
        manga['chapters'].append({'title': chapterTitle, 'chapterUrl': chapterUrl})
        print(chapterTitle, end=' ')
    print()
    return manga
    


urls_mangas = []
mangas = []
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
if __name__ == '__main__':
    with open('mangas_urls.json') as json_file:
        urls_mangas = json.load(json_file)
        print("{} Mangas Finded:".format(len(urls_mangas)))
        for index, mangaUrl in enumerate(urls_mangas):
            print(index, mangaUrl)
    print()
    mangas = [{}] * len(urls_mangas)
    for index, mangaUrl in enumerate(urls_mangas):
        print('Getting Chapters Data from manga {}. ({})'.format(index, mangaUrl))
        for i in range(7):
            try:
                mangas[index] = getMangaDetails(mangaUrl)
                with open('mangas_chapters.json', 'w') as outfile:
                    json.dump(mangas, outfile)
                if 'title' in mangas[index] and 'chapters' in mangas[index]:
                    print("{} finished. {} chapters getted.".format(mangas[index]['title'], len(mangas[index]['chapters'])))
                else:
                    print("{} finished.".format(mangaUrl))
                break
            except HTTPError as e:
                print(e.status, e.reason)
                print('An error happened [HTTPError] when opening manga ({}). Trying again [{} of 6]'.format(mangaUrl, index))
                sleep(pow(2, i))
            except URLError as e:
                print(e.reason)
                print('An error happened [URLError] when opening manga ({}). Trying again [{} of 6]'.format(mangaUrl, index))
                sleep(pow(2, i))
            except:
                print('Unknown Error')
                print('An error happened [Unknown] when opening manga ({}). Trying again [{} of 6]'.format(mangaUrl, index))
                sleep(pow(2, i)) 
        print()
    print()
    print('---------------------------END---------------------------')