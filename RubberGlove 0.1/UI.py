from tkinter import *
from tkinter import filedialog
from datetime import datetime
import os, webbrowser, hashlib
import multiprocessing as mp
import bs_highent

# Global Variables
NAME = "Rubber Glove"
ICON = "icon.ico"
FONT = "Helvetica" #font has to be on windows, should google tkinter fonts to get the correct font family
FONT_SIZE = "11" #font size for all text
TITLE_SIZE = "15" #font size for all titles and larger headings
BG_COLOUR = "#5bbce4" #main blue as specified in the Design Ideas
PATH = "" #path for selected file, should be blank
BUTTON_WIDTH = 10
PADDING = 2
ABOUT_FILE = "about.txt"
WEBSITE = "https://github.coventry.ac.uk/lams39/Bluescreen" #we need to change this once we have the website up and running
# Colours
BLUE1 = "#45b3e0"
BLUE2 = "#5bbce4"
BLUE3 = "#71c5e7"
BLUE4 = "#87ceeb" 
BLUE5 = "#9ddqef"
BLUE6 = "#b3e0f2"
BLUE7 = "#c9e9f6"
GRAY1 = "#989898"
GRAY2 = "#A0A0A0"
GRAY3 = "#A8A8A8"
L_GRAY1 = "#D3D3D3"
L_GRAY2 = "#D8D8D8"
BLACK = "#080808"

# functions

# function to read about file
def about_text(win):
    with open(ABOUT_FILE) as f:
        lines = f.read().split("\n")
        for i in lines:
            Label(win, text=i, bg=BG_COLOUR,font=(FONT,FONT_SIZE)).grid(sticky="W")

# function to center window
def center_window(win):
    win.update()
    x = (win.winfo_screenwidth() / 2) - (win.winfo_reqwidth() / 2)  # calculates what the width should be
    y = (win.winfo_screenheight() / 2) - (win.winfo_reqheight() / 2)  # calculates what the height should be
    win.geometry('+%d+%d' % (x, y))  # puts the window in the middle of the screen

# function for the about window
def about():
    about_window = Toplevel()
    about_window.configure(background=BG_COLOUR)
    about_window.resizable(width=FALSE, height=FALSE)
    about_window.title('About')
    about_window.iconbitmap(ICON)
    about_label = Label(about_window, text="About", bg=BG_COLOUR, font=(FONT,TITLE_SIZE,UNDERLINE))
    about_label.grid(row=1, column=0,sticky="W")
    about_text(about_window)
    button1 = Button(about_window, text="Ok",fg=BLACK, font=(FONT,FONT_SIZE),command = lambda:about_window.destroy(),width=BUTTON_WIDTH)
    button1.grid(row=4,pady=PADDING,padx=PADDING)
    center_window(about_window)
    lock_window(about_window)

# function to make it impossible to interact with window below, ie you must close the current window to go back to the old window
def lock_window(win):
    win.transient()
    win.grab_set()
    win.wait_window(win)

#function to make windows select file diolog display
def pick_file(label1):
    global PATH,FILE
    FILE = True
    file_path = filedialog.askopenfilename()
    if file_path == "":
        label1.config(text="Current Path: None")
        quick_scan_button.config(state=DISABLED)
    else:
        PATH = file_path.replace("/", "\\\\")
        label1.config(text="Current Path: " + PATH)
        quick_scan_button.config(state=NORMAL)

#function to make windows select folder diolog display
def pick_folder(label1):
    global PATH,FILE
    FILE = False
    folder_path = filedialog.askdirectory()
    if folder_path == "":
        label1.config(text="Current Path: None")
        quick_scan_button.config(state=DISABLED)
    else:
        PATH = folder_path.replace("/", "\\\\")
        label1.config(text="Current Path: " + PATH)
        quick_scan_button.config(state=NORMAL)

#function for icon
def func_icon(win):
    win.iconbitmap(ICON) # gives the main window an icon


#function to get output from textbox
def textbox_output():
    text = output_box.get("1.0",END)
    return text

#function to export into a .txt file
def export_and_hashing():
    title = str(datetime.now().replace(microsecond=0))
    title = title.replace(":","")
    title_exports = "Exports\\" + title + ".txt"
    title_hash = "Hashes\\" + title + ".txt"
    with open(title_exports,"w") as f:
        f.write(textbox_output())
    hasher =hashlib.md5()# we hash the new file and save that in different file so we check in the export has been changed
    with open(title_exports,"rb") as f:
        buf = f.read()
        hasher.update(buf)
    hash_out = hasher.hexdigest()
    with open(title_hash,"w") as f:
        f.write (hash_out)
    op_comp_window("The output has been exported to " + title_exports)

#function to make new directory
def new_dir(name):
    try:
        os.mkdir(name)
        print("Directory " + name +  " Created ") 
    except FileExistsError:
        print("Directory " + name + " already exists")

#function to display new windows saying that the operation is compleate
def op_comp_window(string):
    comp_window = Toplevel()
    comp_window.configure(background=BG_COLOUR)
    comp_window.title(NAME)
    label1 = Label(comp_window, text=string, bg=BG_COLOUR,font=(FONT,FONT_SIZE))
    label1.grid()
    button1 = Button(comp_window, text="Ok",fg=BLACK, font=(FONT,FONT_SIZE),command = lambda:comp_window.destroy(),width=BUTTON_WIDTH)
    button1.grid(row=2)
    center_window(comp_window)
    lock_window(comp_window)

#function for scan
def quick_scan():
    entropies = bs_highent.scan(PATH, 0)
    unexpected_files = entropies[0]
    expected_files = entropies[1]
    error_files = entropies[2]
    output_box.config(state=NORMAL)
    output_box.delete('1.0', END)
    for file in unexpected_files:
        unexpected_files_string = ("####UNEXPECTED#### file = " + file[0] + " Entropy value is: " + str(file[1]) + "\n")
        output_box.insert(END,unexpected_files_string)
    for file in expected_files:
        expected_files_string = ("#####EXPECTED##### file = " + file[0] + " exptected to have high entropy value" + "\n")
        output_box.insert(END,expected_files_string)
    for file in error_files:
        error_files_string = ("######ERROR######  file = " + file[0] + " error reason: " + file[1] + "\n")
        output_box.insert(END,error_files_string)
    output_box.config(state=DISABLED)
    export_button.config(state=NORMAL)
    file_submenu.entryconfig(2,state=NORMAL)

#end of functions

new_dir("Exports") # creates the exports folder
new_dir("Hashes") # creates the hashes folder
main_window = Tk()
main_window.title(NAME)  # the initial windows title
main_window.configure(bg=BG_COLOUR)  # background colour
func_icon(main_window)
#menubar
menubar = Menu(main_window)
#file cascade menu
file_submenu = Menu(menubar,tearoff=False)
file_submenu.add_command(label="Select File",command = lambda: pick_file(current_path_label))
file_submenu.add_command(label="Select Folder",command = lambda:pick_folder(current_path_label))
file_submenu.add_command(label="Export",command = lambda:export_and_hashing())
file_submenu.entryconfig(2,state=DISABLED)
file_submenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=file_submenu)
#help cascade menu
help_submenu = Menu(menubar,tearoff=False)
help_submenu.add_command(label="Website", command= lambda:webbrowser.open_new(WEBSITE))
help_submenu.add_command(label="About", command=about)
menubar.add_cascade(label="Help", menu=help_submenu)
main_window.config(menu=menubar)
#labels
label_frame = Frame(main_window,background=BG_COLOUR)
label_frame.pack(side=TOP,fill=X)
title_label = Label(label_frame, text="Rubber Glove", background=BG_COLOUR, font=(FONT,TITLE_SIZE,UNDERLINE))
title_label.grid(row=0, column=0,columnspan=2,sticky="W")
current_path_label = Label(label_frame,text="Current Path: None", background=BG_COLOUR, font=(FONT,FONT_SIZE))
current_path_label.grid(row=1, column=0, columnspan=1000,sticky="W")
#buttons
buttons_frame = Frame(main_window, background=BG_COLOUR)#frame for buttons
buttons_frame.pack(side=LEFT,fill=Y,padx=(5,0))
quick_scan_button = Button(buttons_frame, text="Scan", fg=BLACK, font=(FONT,FONT_SIZE),command = lambda:quick_scan(),width=BUTTON_WIDTH)
quick_scan_button.grid(row=2, column=0,padx=PADDING,pady=PADDING,sticky="W")
quick_scan_button.config(state=DISABLED)
export_button = Button(buttons_frame, text="Export",fg=BLACK, font=(FONT,FONT_SIZE),command = lambda:export_and_hashing(),width=BUTTON_WIDTH)
export_button.grid(row=3, column=0,padx=PADDING,pady=PADDING,sticky="W")
export_button.config(state=DISABLED)#make is disabled until the user has given a path
pick_file_button = Button(buttons_frame, text="Select File",fg=BLACK, font=(FONT,FONT_SIZE),command = lambda: pick_file(current_path_label),width=BUTTON_WIDTH)
pick_file_button.grid(row=4, column=0,padx=PADDING,pady=PADDING,sticky="W")
pick_folder_button = Button(buttons_frame, text="Select Folder",fg=BLACK, font=(FONT,FONT_SIZE),command = lambda:pick_folder(current_path_label),width=BUTTON_WIDTH)
pick_folder_button.grid(row=5, column=0,padx=PADDING,pady=PADDING,sticky="W")
#output box
output_box = Text(main_window,width=100,height=10)
output_box.pack(side=LEFT, anchor="s",fill=BOTH, expand = YES, padx=(5,0),pady=(0,5))
yscrollbar = Scrollbar(main_window,orient=VERTICAL,command=output_box.yview)
yscrollbar.pack(side=RIGHT,anchor="e", fill=Y, padx=(0,5),pady=(0,5))
output_box["yscrollcommand"]=yscrollbar.set
output_box.insert(END,"OUTPUT HERE")
output_box.config(state=DISABLED)
#mainloop
center_window(main_window)  # tells the computer where to put the initial window, in this case the middle of the screen.
main_window.mainloop()  # keeps the window in a loop so it stays open, some idles like pycharm will close the window after the code has finished