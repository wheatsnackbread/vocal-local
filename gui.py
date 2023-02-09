import tkinter as tk
from tkinter import *
from tkinter.ttk import *
import tkinter.filedialog as filedialog
import whisper
import os
from pytube import YouTube  # !pip install pytube
from pytube.exceptions import RegexMatchError
import threading
#import pkg_resources.py2_warn


def drop_inside_list_box(event):
    listb.insert("end", event.data)


def select_file():
    file_path = filedialog.askopenfilename()
    listb.insert(tk.END, file_path)


def clear_file():
    # Get the selected item's index
    selected_index = listb.curselection()

    # Delete the selected item from the listbox
    listb.delete(selected_index)


def clear_all_file():
    # Clear all files from listbox
    listb.delete(0, tk.END)


def download_yt():
    def save_video():
        yt = YouTube(e.get())

        video = yt.streams.filter(only_audio=True).first()
        destination = './tracks'
        out_file = video.download(output_path=destination)
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)

        file_path = new_file
        listb.insert(tk.END, file_path)

        popup.destroy()
        window.update()

    popup = Tk()

    popup.title('Enter YouTube URL')
    popup.geometry('500x80')

    e = Entry(popup)
    e.pack()
    e.focus_set()

    b = Button(popup, text='Download and Select',
               command=lambda: save_video())
    b.pack(side='bottom')

    popup.mainloop()
    save_path = "./mp3"


# Create the main window
window = Tk()

# Define frame
frame = Frame(window)
frame.pack(side=TOP)

# Set the window size
window.geometry('1000x800')
# window.config(bg='lightblue')
window.wm_title("GUI for OpenAI Whisper")

# Title label
label = tk.Label(frame, text="\n Transcribe",
                 font=("Lato", 24), justify=tk.LEFT)
label.pack(side=TOP)

# Text label
label = tk.Label(frame, text="\n• Select files below.\n• Click the file you want to transcribe and hit process. \n• The text will appear and will be automatically added to the clipboard.\n", justify=tk.LEFT)
label.pack(side=TOP)

# Define mid-frame
midFrame = Frame(window)
midFrame.pack(side=TOP)

# Create a button select file and add it to the window
button = tk.Button(midFrame, text='Add Local File',
                   command=select_file, justify=tk.LEFT)
button.pack(side=TOP, fill=X)

# Create a button select file and add it to the window
button = tk.Button(midFrame, text='Add YouTube Video (URL)',
                   command=download_yt, justify=tk.LEFT)
button.pack(side=BOTTOM, fill=X)

# Create a button select file and add it to the window
# button = tk.Button(midFrame, text='Add Online File (URL)', command = select_file, justify = tk.LEFT)
# button.pack(side=LEFT, fill=X)

lowFrame = Frame(window)
lowFrame.pack(side=TOP)

# File select box
listb = tk.Listbox(lowFrame, selectmode=tk.SINGLE, width=100, height=10)
listb.pack(side=BOTTOM, pady=20)

# Define the callback function for the transcribe button


def transcribe_file():

    # Check if the listbox has a selected item
    if listb.curselection():

        # bar()

        progress['value'] = 20
        # window.update_idletasks()

        # Get the selected item from the listbox
        selected_item = listb.get(listb.curselection())

        # Load the Whisper model, options are tiny.en/base.en/small.en
        model = whisper.load_model("base.en")

        progress['value'] = 40
        # window.update_idletasks()

        # Transcribe the selected audio file
        result = model.transcribe(selected_item)

        # Delete the existing text in the text widget
        text.delete('1.0', tk.END)

        progress['value'] = 80
        # window.update_idletasks()

        # Insert the transcribed text into the text widget
        text.insert(tk.END, result["text"])

        # Copy the transcribed text to the clipboard
        text.clipboard_clear()
        text.clipboard_append(text.get('1.0', tk.END))

        progress['value'] = 100

    else:
        # Set the text of the textbox to "Select an item"
        text.delete(1.0, tk.END)
        text.insert(tk.END, "Select an item")


def bar():
    # import time
    progress['value'] = 20
    window.update_idletasks()
    # time.sleep(1)

    progress['value'] = 40
    window.update_idletasks()
    # time.sleep(1)

    progress['value'] = 50
    window.update_idletasks()
    # time.sleep(1)

    progress['value'] = 60
    window.update_idletasks()
    # window.sleep(1)

    progress['value'] = 80
    window.update_idletasks()
    # time.sleep(1)
    progress['value'] = 100


lowFrame = Frame(window)
lowFrame.pack(side=TOP)

# Create a button to clear selected file
button = tk.Button(lowFrame, text='Clear Selected',
                   command=clear_file, justify=tk.LEFT)
button.pack(side=LEFT, pady=5, fill=X)

# Create a button to clear ALL files
button = tk.Button(lowFrame, text='Clear All',
                   command=clear_all_file, justify=tk.LEFT)
button.pack(side=RIGHT, pady=5, fill=X)

lowFrame = Frame(window)
lowFrame.pack(side=TOP)

# Create a transcribe button and add it to the window
button = tk.Button(lowFrame, text='Transcribe Selected',
                   command=transcribe_file, justify=tk.RIGHT)
button.pack(side=LEFT, pady=5, fill=X)

# Create a transcribe button and add it to the window
button = tk.Button(lowFrame, text='Transcribe All',
                   command=transcribe_file, justify=tk.RIGHT)
#button.pack(side=RIGHT, pady=5, fill=X)

# This button will initialize
# the progress bar
lowFrame = Frame(window)
progress = Progressbar(window, orient=HORIZONTAL,
                       length=100, mode='determinate')
# progress.pack(pady=10)

lowFrame = Frame(window)
lowFrame.pack(side=TOP)

# Create a text widget to display the transcribed text
text = tk.Text(lowFrame, wrap=tk.WORD, width=100, height=30)
text.pack(pady=15)

# Run the main loop
window.mainloop()
