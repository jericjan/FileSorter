from tkinter import *
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
        with open(self.path, "r", encoding = 'utf-8') as f:
            text_contents = f.read()
        self.textwidget.insert(1.0, text_contents)
        self.textwidget.config(state=DISABLED)    
        
            
    def OnStop(self):
        self.frame.destroy()