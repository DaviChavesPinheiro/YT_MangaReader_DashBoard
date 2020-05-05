import numpy as np
import cv2
from moviepy.editor import *
from os import listdir
from os import mkdir
from os import path
from functools import cmp_to_key
import json
import time
import math


def resizeImages(manga):
    for chapter in manga['chapters']:
        print()
        print("Chapter {}:".format(chapter['title']), end=' ')
        for page_path in chapter['pages']:
            page_img = cv2.imread(page_path)
            page_index = int(page_path.split('/')[-1].split('_')[0])
            height, width = page_img.shape[:2]
            # print(height, width, end=" | ")
            if height == DEFAULT_SIZE['width'] and width == DEFAULT_SIZE['heigth']:
                print("{} OK".format(page_index), end=" | ")
                continue
            
            page_img = cv2.transpose(page_img)
            page_img = cv2.flip(page_img, flipCode=1)

            page_img = cv2.resize(page_img, (DEFAULT_SIZE['heigth'], DEFAULT_SIZE['width']), interpolation=cv2.INTER_AREA)

            cv2.imwrite(page_path, page_img)
            print("{} Resized".format(page_index), end=" | ")
        print()


def sortChapters(m1, m2):
    if float(str(m1).split('_')[0]) >= float(str(m2).split('_')[0]):
        return 1
    else:
        return -1


def sortPages(m1, m2):
    if float(str(m1).split('_')[0]) >= float(str(m2).split('_')[0]):
        return 1
    else:
        return -1





def getMangaInformation(manga_title):
    manga = {}
    manga['title'] = manga_title
    manga['fps'] = FPS
    manga['chapters'] = []
    
    chapters_title = listdir("{}/".format(manga_title))
    chapters_title = sorted(chapters_title, key=cmp_to_key(sortChapters))
    for chapter_title in chapters_title:
        chapter = {}
        chapter['title'] = chapter_title
        pages = listdir("{}/{}/".format(manga_title, chapter_title))
        pages = sorted(pages, key=cmp_to_key(sortPages))
        pages = list(map(lambda page_title: "{}/{}/{}".format(manga_title, chapter_title, page_title), pages))
        chapter['pages'] = pages
        manga['chapters'].append(chapter)
    print(manga.keys())
    return manga

def createVideos(manga, chuncksize):
    videos_amount = math.ceil(len(manga['chapters']) / chuncksize)
    print("{} videos will be created...".format(videos_amount))
    
    for video_index in range(videos_amount):
        manga_chunck = {}
        manga_chunck['title'] = "{} {}-{}".format(manga['title'], chuncksize * video_index, min(chuncksize * video_index + chuncksize, len(manga['chapters'])) - 1)
        manga_chunck['fps'] = manga['fps']
        manga_chunck['chapters'] = [intro_chapter] + manga['chapters'][video_index * chuncksize: video_index * chuncksize + chuncksize]
        
        chunck_pages = []
        for chapter in manga_chunck['chapters']:
            chunck_pages.extend(chapter['pages'])
        
        print('Converting {} ({} pages)'.format(manga_chunck['title'], len(chunck_pages)))
        clip = ImageSequenceClip(chunck_pages, fps=manga_chunck['fps'])
        clip.write_videofile("{}.mp4".format(manga_chunck['title']))
        
def printDescription(manga, chuncksize):
    descriptions_amount = math.ceil(len(manga['chapters']) / chuncksize)
    print("{} description will be created...".format(descriptions_amount))
    for description_index in range(descriptions_amount):
        manga_chunck = {}
        manga_chunck['title'] = "{} {}-{}".format(manga['title'], chuncksize * description_index, min(chuncksize * description_index + chuncksize, len(manga['chapters'])) - 1)
        manga_chunck['fps'] = manga['fps']
        manga_chunck['chapters'] = [intro_chapter] + manga['chapters'][description_index * chuncksize: description_index * chuncksize + chuncksize]
        manga_chunck['chaptersTimes'] = {}
        sum = 0
        for chapter in manga_chunck['chapters']:
            manga_chunck['chaptersTimes'][chapter['title'].split(' ')[-1]] = time.strftime('%H:%M:%S', time.gmtime(int(sum / manga_chunck['fps'])))
            sum += len(chapter['pages'])
        print("""
Mangá: {} |
Capítulos: {} |
FPS: {}""".format(manga_chunck['title'], str(manga_chunck['chaptersTimes']).replace("'", "").replace('{', '').replace('}', ''), manga_chunck['fps']))
        print('------------------------------------------------------------')

def getIntroChapter(chapter_title):
    chapter = {}
    chapter['title'] = chapter_title
    pages = listdir("{}/".format(chapter_title))
    pages = sorted(pages, key=cmp_to_key(sortPages))
    pages = list(map(lambda page_title: "{}/{}".format(chapter_title, page_title), pages))
    chapter['pages'] = pages
    return chapter
    

chuncksize = 999999999
FPS = 2
DEFAULT_SIZE = {'width': 850, 'heigth': 1300}
intro_chapter = {}
if __name__ == '__main__':

    mangas_titles = list(filter(lambda file: '.' not in file, listdir('.')))
    for index, manga in enumerate(mangas_titles):
        print("{} | ID = {}".format(manga, index))
    
    mangaIndex = int(input("Choose a manga (ID) to convert to video: "))
    
    chuncksize = int(input('How Many Chapters per video do you want? [0 = 200] '))
    if chuncksize <= 0:
        chuncksize = 200

    intro_chapter = getIntroChapter("Intro")
    # print(intro_chapter)
    
    manga = getMangaInformation(mangas_titles[mangaIndex])
    print('--------------------------------------------------')
    print("The Mangá {} has {} chapters".format(manga['title'], len(manga['chapters'])))
    print('--------------------------------------------------')
    
    print("Resizing images:")
    # resizeImages(manga)
    print("All images have been resized!")
    print()
    
    print("Description:")
    printDescription(manga, chuncksize)
    print()
    
    print("Creating Videos")
    createVideos(manga, chuncksize)

    print('-----------------------Finished-----------------------')
   
    # print(chaptersStartTime)
    
    
