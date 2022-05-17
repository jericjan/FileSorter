"""Used for viewing text files"""
from tkinter import Text
from tkinter.ttk import Frame, Scrollbar
import threading


class myText:
    """This is initialized when a text file is selected"""
    def __init__(self, master, path):

        # self.master = master
        # self.path = path
        # self.img = ImageTk.PhotoImage(Image.open(path))
        # self.panel = Label(self.master,image=self.img)
        # self.panel.image = self.img
        # self.panel.pack(side=TOP,expand=True, fill=BOTH)

        self.master = master
        self.path = path
        self.frame = Frame(self.master)
        self.frame.pack(side="top", expand=True, fill="both")
        self.textwidget = Text(self.frame)
        self.textwidget.pack(side="left", expand=True, fill="both")
        self.scrollbar = Scrollbar(
            self.frame, orient="vertical", command=self.textwidget.yview
        )
        self.scrollbar.pack(side="left", fill="both")
        self.textwidget["yscrollcommand"] = self.scrollbar.set
        startit = threading.Thread(target=self.loadfile(self.path))
        startit.start()
        startit.join()
        delta = 1000  # in millseconds
        delay = 0
        self.index = 0
        for i in self.text_contents:
            self.master.after(delay, lambda: self.loadtext(i))
            delay += delta

    def loadtext(self, text):
        """Adds text to the preview window"""
        try:
            self.textwidget.config(state="normal")
            self.textwidget.insert("end", str(text))
            self.index += 1
            self.textwidget.config(state="disabled")
        except:
            pass

    def loadfile(self, file):
        """Split text into n bits which will be sent later to loadtext"""
        with open(file, "r", encoding="utf-8") as f:
            text_contents = f.read()
        n = 30000
        self.text_contents = [
            text_contents[index : index + n]
            for index in range(0, len(text_contents), n)
        ]

    def OnStop(self):
        """Destroy the frame the text preview window is in"""
        self.frame.destroy()
