import requests
import shutil
import re
from selenium import webdriver
from bs4 import BeautifulSoup

def pageSearch(mapper):
    pass


def main():
    mapper = input("Input mapper name:").lower()
    driver = webdriver.Chrome()
    url = "https://bsaber.com/songs/new/?uploaded_by="
    url += mapper
    try:
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        songs = soup.findAll("a", {"rel" : False}, href=re.compile("https://bsaber.com/songs/"))
        i = 0
        urls = []
        names = []
        for item in songs:
            dl = (str(item))
            # If statement makes sure only authors songs are captured
            try:
                fields = dl.split('"')
                # Skip over first unneeded link
                if i >= 2:
                    if "https://" in fields[3]:  # Once reached last song, break out of loop
                        break
                    urls.append(fields[1])  # Add songs to array
                    names.append(fields[3])
            except IndexError:
                print("Invalid Song")
            i += 1
        print(urls)
        print(names)

            # for i in range(len(list)):
            #     print("i EQUALS ", i)
            #     print(list[i])
            #     i += 1


            # list = dl.split('"')
            # link = list[3]
            # print(list)
    except ImportError:
        print("Mapper does not exist")


main()