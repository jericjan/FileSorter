from tkinter import *
import threading
import time


class myText():
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
        self.frame.pack(side=TOP,expand=True, fill=BOTH)
        self.textwidget = Text(self.frame)
        self.textwidget.pack(side=LEFT,expand=True, fill=BOTH)    
        self.scrollbar = Scrollbar(
            self.frame,
            orient='vertical',
            command=self.textwidget.yview
        )
        self.scrollbar.pack(side=LEFT,fill=BOTH)
        self.textwidget['yscrollcommand'] = self.scrollbar.set
        startit = threading.Thread(target=self.loadfile(self.path))
        startit.start()
        startit.join()
        delta = 1000    #in millseconds
        delay = 0        
        self.index = 0
        for i in self.text_contents:
            self.master.after(delay, lambda: self.loadtext(i))
            delay += delta
            

    def loadtext(self, text):
        try:
            self.textwidget.config(state=NORMAL)        
            self.textwidget.insert(END, str(text))   
            self.index += 1
            self.textwidget.config(state=DISABLED)
        except:
            pass
            
        
    def loadfile(self, file):
        with open(file, "r", encoding = 'utf-8') as f:
            text_contents = f.read()                  
        n = 30000
        self.text_contents = [text_contents[index : index + n] for index in range(0, len(text_contents), n)]
  
    def OnStop(self):
        self.frame.destroy()