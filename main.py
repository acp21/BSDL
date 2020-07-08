import requests
import shutil
import os
from tkinter import *
import json
import urllib.request


def setup():
    # Create dl directory
    direct = os.path.isdir("dl")
    if not direct:
        os.mkdir("dl")

    root = Tk()
    root.geometry("500x200")
    gui = GUI(root)
    root.mainloop()


def getMapperID(mapper: str):
    # Create url to check mapper id
    url = "https://beatsaver.com/api/search/advanced?q=uploader.username:" + mapper.lower()
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    # Parse through json to find proper data
    mapperID = data["docs"][0]["uploader"]["_id"]
    lastPage = data["lastPage"]
    print(mapper.upper(), "ID:")
    print(data["docs"][0]["uploader"]["_id"])
    print(lastPage + 1, "Total pages")
    return mapperID, lastPage


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

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.label = Label(frame, text="Input Mapper Name")
        self.label.pack()
        self.button = Button(frame, text="DOWNLOAD!", fg="red", command=self.beginDL)
        self.button.pack()
        self.input = Entry(frame)
        self.input.pack()

    def beginDL(self):
        mapper = self.input.get()
        data = getMapperID(mapper.lower())
        mapperID = data[0]
        lastPage = data[1]
        DLPage(mapperID, 0, lastPage)

    def begin(self):
        root = Tk()
        root.geometry("500x200")
        gui = GUI(root)
        root.mainloop()


if __name__ == "__main__":
    setup()
