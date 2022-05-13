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
        
    
#window=Tk()
window  = ThemedTk(theme='radiance')

if '_PYIBoot_SPLASH' in os.environ and importlib.util.find_spec("pyi_splash"):
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
# add widgets here
def leftKey(event):
    print("Left key pressed")
    
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
    curr_index = listbox.curselection()
    print(f"on {curr_index[-1]}. going to {curr_index[-1]-1}")
    listbox.selection_clear(curr_index[-1])
    listbox.selection_set(curr_index[-1]-1)
    listbox.activate(curr_index[-1]-1)
    items_selected()
def rightKey(event):
    print("Right key pressed")
    
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
frame1 = Frame(window)
frame1.pack(side=TOP,fill=X)

frame2 = Frame(window)
frame2.pack(side=TOP,fill=X)

source_path = StringVar()
dest_path = StringVar()
results = StringVar()
filenames = StringVar()
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
button2 = Button(frame1,text="GO!", command=go)
button2.grid(row=3, column=2)
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

window.mainloop()