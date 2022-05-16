from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
import glob
import os
import shutil
import custom_vlc
from custom_vlc import Player as vlcPlayer
from send2trash import send2trash
from ttkthemes import ThemedTk
import importlib
import json
import sys
from mimetypes import guess_type
from PIL import ImageTk, Image
from image_handler import myImage
from text_handler import myText

class ToolTip:
    def __init__(self,widget,text=None):
        def on_enter(event):
            self.tooltip=Toplevel()
            self.tooltip.overrideredirect(True)
            self.tooltip.geometry(f'+{event.x_root+15}+{event.y_root+10}')
            self.label=Label(self.tooltip,text=self.text)
            self.label.pack()
        def on_leave(event):
            self.tooltip.destroy()
        self.widget=widget
        self.text=text
        self.widget.bind('<Enter>',on_enter)
        self.widget.bind('<Leave>',on_leave)
        
def browse_source():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global source_path
    filename = filedialog.askdirectory()
    source_path.set(filename)
    print(filename)
    
    
def browse_dest():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global dest_path
    filename = filedialog.askdirectory()
    dest_path.set(filename)
    print(filename)
    
def go():    
    global results
    global filenames
    errors = ""
    source = source_path.get()
    dest = dest_path.get()
    if source == "":
        errors += "Source path is empty\n"
    if dest == "":
        errors += "Destination path is empty\n"        
    filter_entries = inputtxt.get()
    print(filter_entries)
    if errors != "":
        results.set(errors)
    else:
        files = glob.glob(f"{source}/{filter_entries}")
        files = [os.path.basename(x) for x in files]
        files = tuple(files)
        filenames.set(files)
        

def read_paths():
    global saved_paths
    if not os.path.exists("saved_paths.json") or os.stat("saved_paths.json").st_size == 0:
        blank = {"names":[],"paths":[]}
        with open("saved_paths.json", 'w') as json_file:
            json.dump(blank, json_file)    
    
    with open("saved_paths.json") as file:
        json_decoded = json.load(file)
    names = json_decoded["names"]
    a = tuple(names)
    saved_paths.set(a)   
    
def save_path():
    global results
    global saved_paths
    dest = dest_path.get()
    saved = paths_listbox.get(0,END)

    with open("saved_paths.json") as file:
        json_decoded = json.load(file)
    names = json_decoded["names"]
    paths = json_decoded["paths"]
    if dest == "":
        results.set("Destination path is empty. Cannot save path.")
    else:  
        names.append(os.path.basename(dest))
        paths.append(dest)
        json_decoded["names"] = names
        json_decoded["paths"] = paths  
        with open("saved_paths.json", 'w') as json_file:
            json.dump(json_decoded, json_file)
        a = tuple(names)
        saved_paths.set(a)   
    
def remove_path():  
    index = paths_listbox.curselection()[0]
    with open("saved_paths.json") as file:
        json_decoded = json.load(file)
    names = json_decoded["names"]
    paths = json_decoded["paths"]
    names.pop(index)
    paths.pop(index)
    json_decoded["names"] = names
    json_decoded["paths"] = paths      
    with open("saved_paths.json", 'w') as json_file:
        json.dump(json_decoded, json_file)    
    paths_listbox.delete(index)
    
def clear_paths():
    global saved_paths
    a = ()
    saved_paths.set(a)
    blank = {"names":[],"paths":[]}
    with open("saved_paths.json", 'w') as json_file:
        json.dump(blank, json_file)        
        
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
        
#window=Tk()
window  = ThemedTk(theme='radiance')

if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
# add widgets here
def leftReleased(event):
    print("Left key released")
    listbox.xview_moveto(0)
    curr_index = listbox.curselection()
    if not curr_index:
        if last_index != "":
            curr_index = last_index
        else:
            print("No index previously selected.")
            return
    else:
        curr_index = curr_index[0]            
    selected_file = listbox.get(curr_index)    
    player.OnStop()
    fixed_path = f"{source_path.get()}/{selected_file}".replace('/', '\\')
    send2trash(fixed_path)
    listbox.selection_clear(curr_index)
    if curr_index == listbox.size()-1:
        new_index = curr_index-1
    else:    
        new_index = curr_index+1
    listbox.selection_set(new_index)
    listbox.activate(new_index)
    items_selected()
    listbox.delete(curr_index)    
    
def upReleased(event):
    print("Up key released")
    listbox.xview_moveto(0)
    curr_index = listbox.curselection()
    if not curr_index:
        if last_index != "":
            curr_index = last_index
        else:
            print("No index previously selected.")
            return
    else:
        curr_index = curr_index[0]            
    listbox.selection_clear(curr_index) 
    if curr_index == 0:
        new_index = curr_index
    else:    
        new_index = curr_index-1        
    listbox.selection_set(new_index)
    listbox.activate(new_index)
    listbox.see(new_index)
    items_selected()
    
def rightReleased(event):
    print("Right key released")
    listbox.xview_moveto(0)
    curr_index = listbox.curselection()
    if not curr_index:
        if last_index != "":
            curr_index = last_index
        else:
            print("No index previously selected.")
            return
    else:
        curr_index = curr_index[0]            
    selected_file = listbox.get(curr_index)    
    player.OnStop()
    shutil.move(f"{source_path.get()}/{selected_file}", f"{dest_path.get()}/{selected_file}")    
    listbox.selection_clear(curr_index)
    if curr_index == listbox.size()-1:
        new_index = curr_index-1
    else:    
        new_index = curr_index+1    
    listbox.selection_set(new_index)
    listbox.activate(new_index)
    items_selected()
    listbox.delete(curr_index)

def downReleased(event):
    print("Down key released")
    listbox.xview_moveto(0)
    curr_index = listbox.curselection()
    if not curr_index:
        if last_index != "":
            curr_index = last_index
        else:
            print("No index previously selected.")
            return
    else:
        curr_index = curr_index[0]
    listbox.selection_clear(curr_index)
    if curr_index == listbox.size()-1:
        new_index = curr_index
    else:    
        new_index = curr_index+1 
    listbox.selection_set(new_index)
    listbox.activate(new_index)
    listbox.see(new_index)
    items_selected()
    
# def upPressed(event):
    # print("Up key pressed")    
# def downPressed(event):
    # print("Down key pressed")    
# def leftPressed(event):
    # print("Left key pressed")    
# def rightPressed(event):
    # print("Right key pressed")        
window.bind('<KeyRelease-Left>', leftReleased)
window.bind('<KeyRelease-Up>', upReleased)
window.bind('<KeyRelease-Right>', rightReleased)
window.bind('<KeyRelease-Down>', downReleased)


top_part = Frame(window)
top_part.pack(side=TOP,fill=X)
frame1 = Frame(top_part)
frame1.pack(side=LEFT)
paths_frame = Frame(top_part)
paths_frame.pack(side=LEFT)
frame2 = Frame(window)
frame2.pack(side=TOP,fill=X)

source_path = StringVar()
dest_path = StringVar()
results = StringVar()
filenames = StringVar()
saved_paths = StringVar()
read_paths()
lbl1 = Entry(master=frame1,textvariable=source_path,width = 50)
lbl1.grid(row=0, column=2)
lbl2 = Entry(master=frame1,textvariable=dest_path,width = 50)
lbl2.grid(row=1, column=2)
lbl2 = Label(master=frame1,textvariable=results)
lbl2.grid(row=4, column=2)



button = Button(frame1,text="Browse", command=browse_source)
button.grid(row=0, column=3, padx=6)
button2 = Button(frame1,text="Browse", command=browse_dest)
button2.grid(row=1, column=3, padx=6)
button3 = Button(frame1,text="GO!", command=go)
button3.grid(row=3, column=2)
button4 = Button(frame1,text="➡", command=save_path,width=2)
button4.grid(row=1, column=4)
ToolTip(button4,"Save destination path for later.")
paths_label = Label(paths_frame, text = "Saved paths:")
paths_label.pack(side=TOP,anchor=NW)
paths_listbox = Listbox(
    paths_frame,
    listvariable=saved_paths,
    height=8,
    selectmode='single'
    )
paths_listbox.pack(side=LEFT,fill=X,expand=True)
paths_scrollbar = Scrollbar(
    paths_frame,
    orient='vertical',
    command=paths_listbox.yview
)
paths_listbox['yscrollcommand'] = paths_scrollbar.set
paths_scrollbar.pack(side=LEFT,fill=BOTH)


        
button5 = Button(paths_frame,text="❌", command=remove_path,width=5)
button5.pack(side=TOP)
ToolTip(button5,"Remove saved path")
button6 = Button(paths_frame,text="Clear", command=clear_paths,width=5)
button6.pack(side=TOP)
ToolTip(button6,"Clear all saved paths")
def path_selected(event=None):
    global dest_path
    selected_indices = paths_listbox.curselection()
    if not selected_indices:
        return
    with open("saved_paths.json") as file:
        json_decoded = json.load(file)
    path = json_decoded["paths"][selected_indices[0]]
    dest_path.set(path)
paths_listbox.bind('<<ListboxSelect>>', path_selected)

filterlbl = Label(frame1, text = "Source path:")
filterlbl.grid(row=0, column=1)
filterlbl = Label(frame1, text = "Destination path:")
filterlbl.grid(row=1, column=1)
filterlbl = Label(frame1, text = "Filters:")
filterlbl.grid(row=2, column=1)

inputtxt = Entry(frame1,width = 50)
inputtxt.grid(row=2, column=2)

instructions = Label(frame2, text = "⬅ = trash item, ⬆ = previous item, ⬇ = next item, ➡ = move item")
instructions.pack(side=TOP)
listbox = Listbox(
    frame2,
    listvariable=filenames,
    height=8,
    selectmode='single'
    )
listbox.pack(side=LEFT,fill=X,expand=True)

scrollbar = Scrollbar(
    frame2,
    orient='vertical',
    command=listbox.yview
)

listbox['yscrollcommand'] = scrollbar.set

scrollbar.pack(side=LEFT,fill=BOTH)
    
class fakePlayer():
    def OnStop(self):
        print("Player not initialized yet.")
        
# class myImage():
    # def __init__(self, master, path):
    
        # # self.master = master
        # # self.path = path
        # # self.img = ImageTk.PhotoImage(Image.open(path))
        # # self.panel = Label(self.master,image=self.img)
        # # self.panel.image = self.img
        # # self.panel.pack(side=TOP,expand=True, fill=BOTH)         
    
        # self.master = master
        # self.path = path
        # self.img = ImageTk.PhotoImage(Image.open(path))
        # self.img_copy = Image.open(path)        
        # self.canvas = Canvas(self.master)
        # self.canvas.pack(expand=True, fill=BOTH)     
        # self.canvas.create_image(0, 0, image=self.img, anchor='nw')
        # self.width = 0   
        # self.height = 0
        # self.zoomfactor = 1
        # self.master.bind("<Configure>", self.OnConfigure)       
        
    # def OnStop(self):
        # self.canvas.destroy() 
    # def OnConfigure(self, pener):             
            # width = self.canvas.winfo_width()
            # height = self.canvas.winfo_height()
            # stored_width = int(round(width * self.zoomfactor))
            # stored_height = int(round(height * self.zoomfactor))
            # if self.width != stored_width or self.height != stored_height:
                # self.ActualResize(width,height)
                
    # def ActualResize(self, width,height):
                # print("rsizing")   
                
                # width = int(round(width * self.zoomfactor))
                # height = int(round(height * self.zoomfactor))
                # new_height = int(round(width * self.img_copy.height / self.img_copy.width))              
                # new_width = int(round(height * self.img_copy.width / self.img_copy.height))                         
                # if new_height <= round(self.canvas.winfo_height() * self.zoomfactor):
                    # resized = self.img_copy.resize((width, new_height),Image.NEAREST)     
                    # print(f"1. new size:{width} x {new_height}")                    
                # elif new_width <= round(self.canvas.winfo_width() * self.zoomfactor):
                    # resized = self.img_copy.resize((new_width, height),Image.NEAREST)    
                    # print(f"2. new size:{new_width} x {height}")         
                # self.img = ImageTk.PhotoImage(resized)
                # self.width = width
                # self.height = height
                # self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image=self.img, anchor=CENTER)    
                # self.canvas.bind("<ButtonPress-1>", self.scroll_start)
                # self.canvas.bind("<B1-Motion>", self.scroll_move)
                # self.canvas.bind("<MouseWheel>", self.do_zoom)
               
    # def scroll_start(self, event):
        # self.canvas.scan_mark(event.x, event.y)

    # def scroll_move(self, event):
        # self.canvas.scan_dragto(event.x, event.y, gain=1)
        
    # def do_zoom(self, event):
        # print(f"X: {event.x}, Y: {event.y} delta: {event.delta}")    
        # magic_number = event.delta / 1000
        # if (self.zoomfactor + magic_number) > 0:
            # self.zoomfactor = self.zoomfactor + magic_number
        # width = self.canvas.winfo_width()
        # height = self.canvas.winfo_height()
        # self.ActualResize(width,height)    
    # def click(self, pener, value):
        # print("clicked!")
        # self.clicked = value
        # if pener != "banan":
            # self.width = pener.width
        # if (pener.width != self.width):
            # self.widthchanged = True
        # else:
            # self.widthchanged = False
player = fakePlayer()

last_index = ""
# saved_time = 1.1
def items_selected(event= None):

    # get selected indices
    selected_indices = listbox.curselection()
    if not selected_indices:
        return    
    global last_index
    global player
    global saved_time
    last_index = selected_indices[0]
    print(f"Setting {last_index} as the last index")
    # get selected items
    selected_file = listbox.get(selected_indices)
    msg = f'You selected: {selected_file}'
    print(msg)
    fullpath = f"{source_path.get()}/{selected_file}"
    parsed = guess_type(fullpath)
    print(f"MIME type:{parsed}")
    filetype = parsed[0].split('/')[0]
    player.OnStop()
    # passed_time = time.time() - saved_time
    # if (passed_time) > 1:
    # print(f"{passed_time} seconds passed")
    if filetype == "video" or filetype == "audio":
        player = vlcPlayer(window)        
        player._Play(fullpath,filetype)
    elif filetype == "image":   
            player = myImage(window,fullpath)   
    elif filetype == "text":
            player = myText(window,fullpath)   
        # saved_time = time.time()        
    
print(window.winfo_children())

listbox.bind('<<ListboxSelect>>', items_selected)    
listbox.bind('<KeyPress-Left>',  lambda e: "break")
listbox.bind('<KeyPress-Up>',  lambda e: "break")
listbox.bind('<KeyPress-Right>',  lambda e: "break")
listbox.bind('<KeyPress-Down>',  lambda e: "break")

window.title('File sorter')
window.iconbitmap(resource_path('filesorter.ico'))
window.mainloop()