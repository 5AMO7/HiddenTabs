from pystray import Icon, Menu, MenuItem
from PIL import Image
import sys

def openApp():
    print("opened")

def exitApp(icon):
    icon.stop()
    sys.exit()

menu = Menu(
    MenuItem('Open HiddenTabs', openApp),
    MenuItem('Exit', exitApp)
)

image = Image.open("resources/icon.png")

icon = Icon("MyApp", image, "HiddenTabs", menu)
icon.run()