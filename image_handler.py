"""This is for showing image previews of selected image files"""

from tkinter import Canvas
import threading
import queue
from PIL import ImageTk, Image



class ImageLoader(threading.Thread):
    """This will load an image in a separate thread in order to not freeze the UI"""
    def __init__(self, canvas, q, path):
        super().__init__()
        self.canvas = canvas
        self.queue = q
        self.path = path

    def run(self):
        with Image.open(self.path) as file:
            self.img = ImageTk.PhotoImage(file)
            self.img_copy = file
            print(f"2. canvas id is: {self.canvas.winfo_id()}")
            self.canvas_img = self.canvas.create_image(0, 0, image=self.img, anchor="nw")
            self.canvas.itemconfigure(self.canvas_img, state="hidden")
            self.queue.put([self.img, self.img_copy])


class myImage:
    """This is what will be called from the main thread"""
    def __init__(self, master, path):

        # self.master = master
        # self.path = path
        # self.img = ImageTk.PhotoImage(Image.open(path))
        # self.panel = Label(self.master,image=self.img)
        # self.panel.image = self.img
        # self.panel.pack(side=TOP,expand=True, fill=BOTH)

        self.master = master
        self.path = path
        self.canvas = Canvas(self.master)
        print(f"1. canvas id is: {self.canvas.winfo_id()}")
        self.canvas.pack(expand=True, fill="both")
        self.loadimg()

    def loadimg(self):
        """This will intialize the ImageLoader"""
        self.queue = queue.Queue()
        ImageLoader(self.canvas, self.queue, self.path).start()
        self.master.after(100, self.process_img)

    def process_img(self):
        """This is called after the ImageLoader finishes"""
        try:
            result = self.queue.get_nowait()
            self.img = result[0]
            self.img_copy = result[1]
            # self.canvas_img = result[2]
            self.width = 0
            self.height = 0
            self.zoomfactor = 1
            # if type(self.master).__name__ == "Frame":
            # print("master is a Frame.")
            # self.master.update()
            print(f"3. canvas id is: {self.canvas.winfo_id()}")
            self.OnConfigure()
            # self.canvas.itemconfigure(self.canvas_img,state='normal')
            self.master.bind("<Configure>", self.OnConfigure)
        except queue.Empty:
            self.master.after(100, self.process_img)

    def OnStop(self):
        """Deletes the image so that the next one can display"""
        try:
            print("Destroying image")
            self.canvas.destroy()
        except:
            pass

    def OnConfigure(self, pener=None):
        """
        When the window is updated, this will check if the window size has changed
        If it has, it runs ActualResize.
        """
        try:
            width = self.canvas.winfo_width()
        except:
            return  # canvas has been deleted
        height = self.canvas.winfo_height()
        stored_width = int(round(width * self.zoomfactor))
        stored_height = int(round(height * self.zoomfactor))

        if self.width != stored_width or self.height != stored_height:
            self.ActualResize(width, height)

    def ActualResize(self, width, height):
        """Resizes the image to fit the preview window"""
        print("rsizing")

        width = int(round(width * self.zoomfactor))
        height = int(round(height * self.zoomfactor))
        # print(f"width and height is: {width} x {height}")
        new_height = int(round(width * self.img_copy.height / self.img_copy.width))
        new_width = int(round(height * self.img_copy.width / self.img_copy.height))
        # print(f"new width and height is: {new_width} x {new_height}")
        if new_height <= round(self.canvas.winfo_height() * self.zoomfactor):
            resized = self.img_copy.resize((width, new_height), Image.NEAREST)
            # print(f"1. new size:{width} x {new_height}")
        elif new_width <= round(self.canvas.winfo_width() * self.zoomfactor):
            resized = self.img_copy.resize((new_width, height), Image.NEAREST)
            # print(f"2. new size:{new_width} x {height}")
        self.img = ImageTk.PhotoImage(resized)
        self.width = width
        self.height = height
        self.canvas.create_image(
            self.canvas.winfo_width() / 2,
            self.canvas.winfo_height() / 2,
            image=self.img,
            anchor="center",
        )
        self.canvas.bind("<ButtonPress-1>", self.scroll_start)
        self.canvas.bind("<B1-Motion>", self.scroll_move)
        self.canvas.bind("<MouseWheel>", self.do_zoom)

    def scroll_start(self, event):
        """When left mouse button is clicked, it marks where it is initially"""
        self.canvas.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        """When the mouse is moved while holding LMB, move canvas by that offset"""
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def do_zoom(self, event):
        """For zooming in/out an image"""
        print(f"X: {event.x}, Y: {event.y} delta: {event.delta}")
        magic_number = event.delta / 1000
        if (self.zoomfactor + magic_number) > 0:
            self.zoomfactor = self.zoomfactor + magic_number
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        self.ActualResize(width, height)
