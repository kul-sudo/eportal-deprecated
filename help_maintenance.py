from tkinter import Toplevel, Button, DISABLED, WORD, INSERT
from tkinter.scrolledtext import ScrolledText

from config import *
from help_text import HELP_TEXT
from global_items import center_window

def hide_help():
    help_window.withdraw()

def show_help():
    help_window.deiconify()

def create_help_window():
    # Creating the help window
    global help_window
    help_window = Toplevel(takefocus=True)
    hide_help()
    help_window.protocol('WM_DELETE_WINDOW', hide_help)
    help_window.resizable(width=False, height=False)
    help_window['bg'] = HELP_WINDOW_BG
    help_window.geometry(f'{round(GEOMETRY_RATIO*help_window.winfo_screenwidth())}x{round(GEOMETRY_RATIO*help_window.winfo_screenheight())}') # Setting the window geometry according to the size of the screen
    help_window.update() # If this update is not done, nothing further works
    center_window(help_window)
    help_window.title(TITLE)
    
    # Creating the window with ScrolledText
    txt = ScrolledText(
        master=help_window,
        height=int((help_window.winfo_height()-POPULATED_ROOM)/(SCROLLED_FONT_SIZE_GAP_HEIGHT)),
        foreground=TEXT_COLOR,
        bg=HELP_WINDOW_BG,
        borderwidth=0,
        width=int(help_window.winfo_width()/LETTER_WIDTH),
        font=('Arial', HELP_SCROLLED_TEXT_FONT_SIZE),
        wrap=WORD
    )

    txt.pack()
    txt.insert(INSERT, HELP_TEXT)
    txt.configure(state=DISABLED)

    Button(
        master=help_window, text='I have read the guideline',
        command=hide_help
    ).pack(pady=10)