from pystray import Icon, Menu, MenuItem
from PIL import Image
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
import sv_ttk
import win32gui
import win32process
import psutil
import configparser
from pynput import mouse
import threading

def get_hwnd(exe):
    exe_hwnd = None
    def callback(hwnd, windows):
        nonlocal exe_hwnd
        if exe_hwnd is not None:
            return
        
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            pid = win32process.GetWindowThreadProcessId(hwnd)[1]
            try:
                process = psutil.Process(pid)
                process_exe = process.name()

                if process_exe.lower() == exe.lower():
                    exe_hwnd = hwnd
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

    win32gui.EnumWindows(callback, None)
    return exe_hwnd

def get_pos_from_hwnd(hwnd):
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bottom = rect
    width = right - left
    height = bottom - top

    return left, top, width, height


def open_window(hwnd):
    config = configparser.ConfigParser()
    config.read('window_positions.ini')
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    exe = psutil.Process(pid).name()
    
    pos = config[str(exe)]["opened_pos"].split(",")
    left, top, width, height = int(pos[0]), int(pos[1]), int(pos[2]), int(pos[3])
    win32gui.MoveWindow(hwnd, left, top, width, height, True)

def close_windows():
    config = configparser.ConfigParser()
    config.read('window_positions.ini')
    
    for exe in config.sections():
        hwnd = get_hwnd(exe)
        if hwnd is not None:
            pos = config[str(exe)]["closed_pos"].split(",")
            left, top, width, height = int(pos[0]), int(pos[1]), int(pos[2]), int(pos[3])
            win32gui.MoveWindow(hwnd, left, top, width, height, True)


def on_click(x, y, button, pressed):
    print("clicked")
    config = configparser.ConfigParser()
    config.read('window_positions.ini')
    print(config.sections())

    pressedWindow = win32gui.GetForegroundWindow()
    pid = win32process.GetWindowThreadProcessId(pressedWindow)[1]
    
    if pid < 0:
        close_windows()
        return
    
    activeExe = psutil.Process(pid).name()
    print(activeExe)
    if activeExe is not None and activeExe in config and pressedWindow is not None:
        open_window(pressedWindow)
        print("opened")
    else:
        close_windows()
        print("closed")


def start_gui():
    def select_file():
        filetypes = [
            ("application files (*.exe)", ".exe")
        ]

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        selectComboBox.set(filename.split("/")[-1])

    def set_open_pos():
        exe = selectComboBox.get()
        hwnd = get_hwnd(exe)
        left, top, width, height = get_pos_from_hwnd(hwnd)

        config = configparser.ConfigParser()
        config.read('window_positions.ini')

        if str(exe) in config:
            config[str(exe)]["opened_pos"] = str(left) + "," + str(top) + "," + str(width) + "," + str(height)
        else:
            config[str(exe)] = {
                "opened_pos": str(left) + "," + str(top) + "," + str(width) + "," + str(height),
                "closed_pos": str(left) + "," + str(top) + "," + str(width) + "," + str(height)
            }

        with open('window_positions.ini', 'w') as configfile:
            config.write(configfile)

        print(str(left) + ", " + str(top) + ", " + str(width) + ", " + str(height))

    def set_close_pos():
        exe = selectComboBox.get()
        hwnd = get_hwnd(exe)
        left, top, width, height = get_pos_from_hwnd(hwnd)

        config = configparser.ConfigParser()
        config.read('window_positions.ini')

        if str(exe) in config:
            config[str(exe)]["closed_pos"] = str(left) + "," + str(top) + "," + str(width) + "," + str(height)
        else:
            config[str(exe)] = {
                "opened_pos": str(left) + "," + str(top) + "," + str(width) + "," + str(height),
                "closed_pos": str(left) + "," + str(top) + "," + str(width) + "," + str(height)
            }

        with open('window_positions.ini', 'w') as configfile:
            config.write(configfile)

        print(str(left) + ", " + str(top) + ", " + str(width) + ", " + str(height))

    def set_combobox_apps():
        config = configparser.ConfigParser()
        config.read('window_positions.ini')

        for section in config.sections():
            selectComboBox['values'] = (*selectComboBox['values'], section)

    root = tk.Tk()

    root.title("HiddenTabs")
    root.geometry("400x300")
    root.wm_iconphoto(True, tk.PhotoImage(file="src/resources/icon.png"))

    selectLabel = ttk.Label(root, text="Select an application:", font=("TkDefaultFont", 16))
    selectLabel.pack(pady=(20, 10))

    selectComboBox = ttk.Combobox(root, state="readonly")
    selectComboBox.bind("<<ComboboxSelected>>", lambda e: print(selectComboBox.get()))
    selectComboBox.pack()
    set_combobox_apps()

    selectButton = ttk.Button(root, text="Select a different app", command=select_file)
    selectButton.pack(pady=(10, 30))

    
    setOpenButton = ttk.Button(root, text="Set Open Position", command=set_open_pos)
    setOpenButton.pack(pady=(10))
    setCloseButton = ttk.Button(root, text="Set Close Position", command=set_close_pos)
    setCloseButton.pack(pady=(10))

    sv_ttk.set_theme("dark")

    root.mainloop()

def start_tray():
    def openApp():
        start_gui()

    def exitApp(icon):
        icon.stop()
        sys.exit()

    menu = Menu(
        MenuItem('Open HiddenTabs', openApp),
        MenuItem('Exit', exitApp)
    )

    image = Image.open("src/resources/icon.png")

    icon = Icon("MyApp", image, "HiddenTabs", menu)

    icon.run()

def start_listener():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


if __name__ == "__main__":
    listener_thread = threading.Thread(target=start_listener, daemon=True)

    listener_thread.start()
    start_tray()

