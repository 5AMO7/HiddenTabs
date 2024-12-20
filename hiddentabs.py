from pystray import Icon, Menu, MenuItem
from PIL import Image
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import darkdetect
import sv_ttk

def on_select(event):
    selected_item = comboBox.get()
    print(selected_item)

def select_file():
    filetypes = [
        ("application files (*.exe)", ".exe")
    ]

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    comboBox.set(filename.split("/")[-1])


root = tk.Tk()

root.title("HiddenTabs")
root.geometry("600x400")
root.wm_iconphoto(True, tk.PhotoImage(file="resources/icon.png"))

selectLabel = ttk.Label(root, text="Select an application:", font=("TkDefaultFont", 16))
selectLabel.pack(pady=(20, 10))

comboBox = ttk.Combobox(root, state="readonly", values=["Option 1", "Option 2", "Option 3"])
comboBox.bind("<<ComboboxSelected>>", lambda e: print(comboBox.get()))

button = ttk.Button(root, text="Select a different app", command=select_file)

comboBox.pack()
button.pack(pady=(10))

sv_ttk.set_theme("dark")
root.mainloop()

# def openApp():
#     print("opened")

# def exitApp(icon):
#     icon.stop()
#     sys.exit()

# menu = Menu(
#     MenuItem('Open HiddenTabs', openApp),
#     MenuItem('Exit', exitApp)
# )

# image = Image.open("resources/icon.png")

# icon = Icon("MyApp", image, "HiddenTabs", menu)
# icon.run()
