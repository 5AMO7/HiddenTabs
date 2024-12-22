# HiddenTabs (Windows only) (WIP)
 An app to hide your open windows/tabs to view your beautiful background and save the much needed space.

![HiddenTabs hiding and showing windows](HiddenTabs_in_action.gif)

## Installation
### Using the repository
1. Clone the repository :
```bash
git clone https://github.com/5AMO7/HiddenTabs.git
cd HiddenTabs
```
2. Install the required dependecies :
```bash
pip install -r requirements.txt
```
3. Run HiddenTabs :
```bash
python src/hiddentabs.py
```

## Using HiddenTabs
1. HiddenTabs starts minimized in the system tray, so open the GUI.
2. Select an app's .exe
3. Move the app's window to your desired open position, then press `Set Open Position`
4. Do the same for the close position.

_If you need finetuning of the positions, be sure to change them in the conifg file._
```ini
[app.exe]
opened_pos = [left],[top],[width],[height]
...
```

And you're done, you can now close HiddenTabs, but be sure to leave the app running in the background for it to work!