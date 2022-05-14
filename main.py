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
def leftKey(event):
    print("Left key pressed")
    listbox.xview_moveto(0)
    curr_index = listbox.curselection()
    selected_file = listbox.get(curr_index)    
    player.OnStop()
    fixed_path = f"{source_path.get()}/{selected_file}".replace('/', '\\')
    send2trash(fixed_path)
    listbox.selection_clear(curr_index[-1])
    listbox.selection_set(curr_index[-1]+1)
    listbox.activate(curr_index[-1]+1)
    items_selected()
    listbox.delete(curr_index[-1])    
    
def upKey(event):
    print("Up key pressed")
    listbox.xview_moveto(0)
    curr_index = listbox.curselection()
    print(f"on {curr_index[-1]}. going to {curr_index[-1]-1}")
    listbox.selection_clear(curr_index[-1])
    listbox.selection_set(curr_index[-1]-1)
    listbox.activate(curr_index[-1]-1)
    items_selected()
def rightKey(event):
    print("Right key pressed")
    listbox.xview_moveto(0)
    curr_index = listbox.curselection()
    selected_file = listbox.get(curr_index)    
    player.OnStop()
    shutil.move(f"{source_path.get()}/{selected_file}", f"{dest_path.get()}/{selected_file}")    
    listbox.selection_clear(curr_index[-1])
    listbox.selection_set(curr_index[-1]+1)
    listbox.activate(curr_index[-1]+1)
    items_selected()
    listbox.delete(curr_index[-1])

def downKey(event):
    print("Down key pressed")
    listbox.xview_moveto(0)
    curr_index = listbox.curselection()
    print(f"on {curr_index[-1]}. going to {curr_index[-1]+1}")
    listbox.selection_clear(curr_index[-1])
    listbox.selection_set(curr_index[-1]+1)
    listbox.activate(curr_index[-1]+1)
    items_selected()
window.bind('<Left>', leftKey)
window.bind('<Up>', upKey)
window.bind('<Right>', rightKey)
window.bind('<Down>', downKey)
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
    
player = vlcPlayer(window)
    
def items_selected(event= None):

    # get selected indices
    selected_indices = listbox.curselection()
    # get selected items
    selected_file = listbox.get(selected_indices)
    msg = f'You selected: {selected_file}'
    #vpWindow=Tk()
    player.OnStop()
    player._Play(f"{source_path.get()}/{selected_file}")
    print(msg)


listbox.bind('<<ListboxSelect>>', items_selected)    

window.title('File sorter')
window.iconbitmap(resource_path('filesorter.ico'))
window.mainloop()