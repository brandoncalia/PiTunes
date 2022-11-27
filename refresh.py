import tkinter
import os
from tkinter import Tk, Canvas, Entry, Text, PhotoImage
from pathlib import Path

parent_path = Path(__file__).parent

refresh = Tk()
refresh.configure(bg="#FFFFFF")
refresh.config(cursor='none')
refresh.attributes('-fullscreen', True)

refreshScreen = Canvas(refresh, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
refreshScreen.place(x=0, y=0)

refresh_image = PhotoImage(file=Path(os.path.join(parent_path, "assets", "refresh.png")))
refresh_image_image = refreshScreen.create_image(512, 300, image=refresh_image)

refresh.mainloop()
