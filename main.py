import requests
import shutil
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from tkinter import *
import json
import urllib.request


# Setup function gets mapper name from user
# Starts web driver
# Begins to parse the first page of songs
def setup():



    # Starting web driver
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(options=option)
    print("Starting web driver")
    # Ensure DL folder exists
    direct = os.path.isdir("dl")
    if not direct:
        os.mkdir("dl")

    root = Tk()
    root.geometry("500x200")
    gui = GUI(root, driver)
    root.mainloop()

    # Download maps
    #mapper = gui.getName()
    #mapper = input("Input mapper name:").lower()
    #parsePage(mapper, 1, driver)


# parsePage() takes a mapper name, a page number, and a webdriver as paramaters
# The function then loops through the page looking for html links that match specific criteria
# It saves these links in an array and then passes them all to DLSongs()
# parsePage() then recursively calls itself with page + 1
# If page does not exist, program stops
def parsePage(mapper : str, page : int, driver : webdriver):
    if page == 1:
        url = "https://bsaber.com/songs/new/?uploaded_by="
    else:
        url = "https://bsaber.com/songs/new/page/" + str(page) + "/?uploaded_by="
    url += mapper
    try:
        driver.get(url)
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        if soup.find(text="No articles found matching your query"):
            if page == 1:
                print("Mapper not found")
                exit()
            else:
                print("All Downloads Complete")
                exit()
        # Get all links containing "https://bsaber.com/songs/"
        songs = soup.findAll("a", {"rel" : False}, href=re.compile("https://bsaber.com/songs/"))
        i = 0
        # Create lists to store urls and song names
        urls = []
        names = []
        for item in songs:
            dl = (str(item))
            # If statement makes sure only author's songs are captured
            try:
                fields = dl.split('"')
                # Skip over first unneeded link
                if i >= 2:
                    if "https://" in fields[3]:  # Once reached last song, break out of loop
                        break
                    urls.append(fields[1])  # Add songs to array
                    names.append(fields[3])
            # Catch all index errors thrown by incorrect link captures
            except IndexError:
                print("Invalid Song")
            i += 1
        # Debug print statements below
        # print(urls)
        # print(names)
        DLSongs(urls, names)
        print("Finished Page")
        # Recursively loop through function until empty page found
        parsePage(mapper, page + 1, driver)
    # This exception is currently unused, should be removed
    except Exception:
        if page == 1:
            print("Mapper does not exist")


def main():
    setup()


def getMapperID(mapper: str):
    url = "https://beatsaver.com/api/search/advanced?q=uploader.username:" + mapper.lower()
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    mapperID = data["docs"][0]["uploader"]["_id"]
    lastPage = data["lastPage"]
    print(mapper.upper(), "ID:")
    print(data["docs"][0]["uploader"]["_id"])
    print(lastPage + 1, "Total pages")
    DLPage(mapperID, 0, lastPage)
    #return mapperID, lastPage


def DLPage(mapperID: str, page: int, totalPages: int):
    url = "https://beatsaver.com/api/maps/uploader/"
    url += mapperID + "/" + str(page)
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    if page < totalPages:
        i = 0
        while True:
            try:
                name = data["docs"][i]["name"]
                key = "https://beatsaver.com" + data["docs"][i]["downloadURL"]
                r = requests.get(key, stream=True)
                print("Downloading", name)
                if r.status_code == 200:
                    name = fixName(name)
                    directory = os.getcwd()  # Get working directory
                    directory = directory + r"/dl//"
                    path = directory + name + ".zip"
                    print("Saving to ", path)
                    with open(path, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)
                i += 1
            except IndexError:
                print("END OF PAGE")
                DLPage(mapperID, page + 1, totalPages)
    else:
        print("Download Complete")
        sys.exit()


def DLSongs(urls: str, names: str):
    #
    # print("URLS")
    # print(urls)
    # print("NAMES")
    # print(names)
    for i in range(len(urls)):
        urlsplit = urls[i].split("/")
        key = urlsplit[4]
        key = "https://beatsaver.com/api/download/key/" + key
        r = requests.get(key, stream=True)
        print("Dowloading ", names[i])
        print(urls[i])
        # Check if dl folder exists in working directory
        direct = os.path.isdir("dl")
        if not direct:  # If dl does not exist, create dl
            os.mkdir("dl")
        if r.status_code == 200:  # If request successful
            name = fixName(names[i])  # Use fixName() to fix song name
            directory = os.getcwd()   # Get working directory
            directory = directory + r"/dl//"
            path = directory + name + ".zip"
            print("Saving to ", path)
            with open(path, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

# fixName() accepts a string and removes certain characters that cause problems
# in Windows file names
def fixName(name: str):
    name = name.replace(r"\\", "")
    name = name.replace("/", "")
    name = name.replace("*", "")
    name = name.replace(":", "")
    name = name.replace("?", "")
    name = name.replace(">", "")
    name = name.replace("<", "")
    name = name.replace('"', "")
    name = name.replace('|', "")
    return name

class GUI:

    def __init__(self, master, driver):
        frame = Frame(master)
        frame.pack()
        self.driver = driver
        self.label = Label(frame, text="Input Mapper Name")
        self.label.pack()
        self.button = Button(frame, text="DOWNLOAD!", fg="red", command=self.beginDL)
        self.button.pack()
        self.input = Entry(frame)
        self.input.pack()

    def beginDL(self):
        mapper = self.input.get()
        getMapperID(mapper.lower())

    def begin(self):
        root = Tk()
        root.geometry("500x200")
        gui = GUI(root)
        root.mainloop()



if __name__ == "__main__":
    getMapperID("oddloop")