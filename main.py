import requests
import shutil
from selenium import webdriver
from bs4 import BeautifulSoup
import os
from tkinter import *


# Setup function gets mapper name from user
# Starts web driver
# Begins to parse the first page of songs
def setup():

    # Starting web driver
    print("Starting web driver...")
    option = webdriver.ChromeOptions()
    option.add_argument("headless")
    driver = webdriver.Chrome(options=option)
    print("Web driver setup complete")

    root = Tk()
    root.title("BSDL")
    root.geometry("300x200")
    gui = GUI(root, driver)
    root.mainloop()


# parsePage() takes a mapper name, a page number, and a web driver as paramaters
# The function then loops through the page looking for html links that match specific criteria
# It saves these links in an array and then passes them all to DLSongs()
# parsePage() then recursively calls itself with page + 1
# If page does not exist, program stops
def parsePage(mapper: str, page: int, driver: webdriver):
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
    # Catch any exception and print to user
    except Exception as e:
        print(e)


def main():
    setup()


def DLSongs(urls: str, names: str):
    for i in range(len(urls)):
        urlsplit = urls[i].split("/")
        key = urlsplit[4]
        key = "https://beatsaver.com/api/download/key/" + key
        r = requests.get(key, stream=True)
        print("Downloading ", names[i])
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
        self.master = master
        frame = Frame(master)
        frame.pack()
        self.driver = driver
        self.label = Label(frame, text="Input Mapper Name")
        self.label.pack(pady=10)
        self.input = Entry(frame)
        self.input.pack(pady=10)
        self.button = Button(frame, text="DOWNLOAD!", fg="red", command=self.beginDL)
        self.button.pack(pady=10)

        menuBar

    def beginDL(self):
        mapper = self.input.get()
        parsePage(mapper, 1, self.driver)

    def openSettings(self):
        self.settingsFrame = Toplevel(self.master)
        self.settings = Settings(self.settingsFrame)


class Settings:
    def __init__(self, master):
        frame = Frame(master)


main()
