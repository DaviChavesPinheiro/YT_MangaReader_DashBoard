import numpy as np
import cv2
from moviepy.editor import *
from os import listdir
from os import mkdir
from os import path
from functools import cmp_to_key
import json
import time


def resizeImages(mangaName):
    chapters = listdir("{}/".format(mangaName))
    chapters = sorted(chapters, key=cmp_to_key(sortChapters))
    for index, chapter in enumerate(chapters):
        if index >= max_chapters:
            break
        pages = listdir("{}/{}/".format(mangaName, chapter))
        pages = sorted(pages, key=cmp_to_key(sortPages))
        for page in pages:
            img = cv2.imread("{}/{}/{}".format(mangaName, chapter, page))

            h, w = img.shape[:2]
            if h == defaultSize['w'] and w == defaultSize['h']:
                print(
                    "Page {} already is resized ({}, {}). Moving to the next one...".format(page, w, h))
                continue

            # Rotate Image
            out = cv2.transpose(img)
            out = cv2.flip(out, flipCode=1)

            img = cv2.resize(
                out, (defaultSize['h'], defaultSize['w']), interpolation=cv2.INTER_AREA)

            cv2.imwrite("{}/{}/{}".format(mangaName, chapter, page), img)

            # cv2.imshow("Resized image", img)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()

            print("Chap.({}) Page {} Resized!".format(chapter.split(' ')[-1] ,page))


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


def getPages(mangaName):
    totalPages = []
    chapters = listdir("{}/".format(mangaName))
    chapters = sorted(chapters, key=cmp_to_key(sortChapters))
    for index, chapter in enumerate(chapters):
        if index >= max_chapters:
            break
        pages = listdir("{}/{}/".format(mangaName, chapter))
        pages = sorted(pages, key=cmp_to_key(sortPages))
        pages = list(
            map(lambda title: "{}/{}/".format(mangaName, chapter) + title, pages))
        totalPages.extend(pages)
    # print(totalPages)
    return totalPages


def getChaptersStarts(mangaName):
    chapterStartTime = {}
    chapters = listdir("{}/".format(mangaName))
    chapters = sorted(chapters, key=cmp_to_key(sortChapters))
    sum = 0
    for index, chapter in enumerate(chapters):
        if index >= max_chapters:
            break
        pages = listdir("{}/{}/".format(mangaName, chapter))
        pages = sorted(pages, key=cmp_to_key(sortPages))
        chapterStartTime[chapter.split(' ')[-1]] = time.strftime('%H:%M:%S', time.gmtime(int(sum / FPS)))
        sum += len(pages)
        pages = list(
            map(lambda title: "{}/{}/".format(mangaName, chapter) + title, pages))
    return chapterStartTime


max_chapters = 999999999
FPS = 2
defaultSize = {'w': 850, 'h': 1300}

if __name__ == '__main__':

    mangas = list(filter(lambda file: '.' not in file, listdir('.')))
    for index, manga in enumerate(mangas):
        print("{} | ID = {}".format(manga, index))
    mangaIndex = int(input("Choose a manga (ID) to convert to video: "))
    print("FPS SET TO {}".format(FPS))
    max_chapters = int(
        input('How Many Chapters Do You want to Convert? [0 = Infinity] '))
    if max_chapters == 0:
        max_chapters = 999999999
    manga = {}
    manga['chapterStartPage'] = []
    manga['title'] = mangas[mangaIndex]
    manga['fps'] = FPS
    manga['chapterStartPage'] = getChaptersStarts(manga['title'])
    # print(chaptersStartTime)
    print("[[[{}]]]".format(json.dumps(manga)))

    resizeImages(manga['title'])
    manga['pages'] = getPages(manga['title'])

    clip = ImageSequenceClip(manga['pages'], fps=FPS)
    clip.write_videofile("{}.mp4".format(manga['title']))
    
    del manga['pages']
    # print(chaptersStartTime)
    print("[[[{}]]]".format(json.dumps(manga)))
    
