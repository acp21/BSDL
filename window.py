from tkinter import *
import main


class GUI:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.label = Label(frame, text="Input Mapper Name")
        self.label.pack()
        self.button = Button(frame, text="DOWNLOAD!", fg="red", command=self.printname)
        self.button.pack()
        self.input = Entry(frame)
        self.input.pack()

    def beginDL(self):
        print(self.input.get())

    def begin(self):
        root = Tk()
        root.geometry("500x200")
        gui = GUI(root)
        root.mainloop()

# Required for tkinter to function properly

g
#root.destroy()

#
# class Window(Frame):
#
#
#
#     def __init__(self, master=None):
#         Frame.__init__(self, master)
#         self.master = master
#         self.init_window()
#
#     entry1 = Entry(root)
#
#     def init_window(self):
#         self.master.title("GUI TEST")
#         self.pack(fill=BOTH, expand=1)
#        # entry1 = Entry(root)
#         entry1.place(x=0,y=0)
#         menu = Menu(self.master)
#         button = Button(self, text="Print")
#         button.place(x=50,y=50,command=self.print_something(entry1))
#         self.master.config(menu=menu)
#         file = Menu(menu)
#         file.add_command(label="Exit", command=self.client_exit)
#         menu.add_cascade(label="File", menu=file)
#         edit = Menu(menu)
#         edit.add_command(label="Undo")
#         menu.add_cascade(label="Edit", menu=edit)
#
#     def print_something(self, entry1):
#         print(entry1.get())
#
#
#     def hello_world(self):
#         print("Hello world")
#     def client_exit(self):
#         exit()
#
# root = Tk()
# root.geometry("400x300")
#
# app = Window(root)
# root.mainloop()