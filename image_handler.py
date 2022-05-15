from tkinter import *
from PIL import ImageTk, Image
class myImage():
    def __init__(self, master, path):
    
        # self.master = master
        # self.path = path
        # self.img = ImageTk.PhotoImage(Image.open(path))
        # self.panel = Label(self.master,image=self.img)
        # self.panel.image = self.img
        # self.panel.pack(side=TOP,expand=True, fill=BOTH)         
    
        self.master = master
        self.path = path
        self.img = ImageTk.PhotoImage(Image.open(path))
        self.img_copy = Image.open(path)        
        self.canvas = Canvas(self.master)
        self.canvas.pack(expand=True, fill=BOTH)     
        self.canvas.create_image(0, 0, image=self.img, anchor='nw')
        self.width = 0   
        self.height = 0
        self.zoomfactor = 1
        if type(self.master).__name__ == "Frame":
            self.master.update()
            self.OnConfigure()
        self.master.bind("<Configure>", self.OnConfigure)       
        
    def OnStop(self):
        self.canvas.destroy() 
    def OnConfigure(self, pener=None):             
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            stored_width = int(round(width * self.zoomfactor))
            stored_height = int(round(height * self.zoomfactor))

            if self.width != stored_width or self.height != stored_height:
                self.ActualResize(width,height)
                
    def ActualResize(self, width,height):
                print("rsizing")   
                
                width = int(round(width * self.zoomfactor))
                height = int(round(height * self.zoomfactor))
                # print(f"width and height is: {width} x {height}")
                new_height = int(round(width * self.img_copy.height / self.img_copy.width))              
                new_width = int(round(height * self.img_copy.width / self.img_copy.height))  
                # print(f"new width and height is: {new_width} x {new_height}")
                if new_height <= round(self.canvas.winfo_height() * self.zoomfactor):
                    resized = self.img_copy.resize((width, new_height),Image.NEAREST)     
                    # print(f"1. new size:{width} x {new_height}")                    
                elif new_width <= round(self.canvas.winfo_width() * self.zoomfactor):
                    resized = self.img_copy.resize((new_width, height),Image.NEAREST)    
                    # print(f"2. new size:{new_width} x {height}")         
                self.img = ImageTk.PhotoImage(resized)
                self.width = width
                self.height = height
                self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image=self.img, anchor=CENTER)    
                self.canvas.bind("<ButtonPress-1>", self.scroll_start)
                self.canvas.bind("<B1-Motion>", self.scroll_move)
                self.canvas.bind("<MouseWheel>", self.do_zoom)
                
    def scroll_start(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    def do_zoom(self, event):
        print(f"X: {event.x}, Y: {event.y} delta: {event.delta}")    
        magic_number = event.delta / 1000
        if (self.zoomfactor + magic_number) > 0:
            self.zoomfactor = self.zoomfactor + magic_number
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.ActualResize(width,height)                   