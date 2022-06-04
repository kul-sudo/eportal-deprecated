from tkinter import FLAT, N, NORMAL, DISABLED, HORIZONTAL, LEFT, RIGHT, TOP, W, BooleanVar, Button, Canvas, Frame, PhotoImage, StringVar, Label, LabelFrame, Scale
from tkinter.ttk import Checkbutton, OptionMenu
from tkinter.font import Font

from config import *
from crosses import delete_all_crosses
from images import PLANT_IMAGE
from help_maintenance import create_help_window, show_help
from global_items import center_window
from window_functions import change_in_dict
from evolution import evolution
from global_items import window_commands, window, checkbuttons_for_triangle
import global_items

def window_handling(): # Creating and handling the window
    # Creating the window
    window.title(TITLE)
    window.iconphoto(True, PhotoImage(data=PLANT_IMAGE))
    window.geometry(f"{WINDOW_SIZE['width']}x{WINDOW_SIZE['height']}")
    window.resizable(width=False, height=False)

    center_window(window)
    create_help_window()

    # Creating top_frame
    (top_frame := Frame()).pack()
     
    # Creating canvas
    global_items.canvas = Canvas(
        master=top_frame,
        width=CANVAS_WIDTH,
        height=CANVAS_HEIGHT,
        bd=CANVAS_BORDER, # Canvas outline width
        relief=FLAT # Appearence of the outline of canvas
    )
    
    global_items.canvas.pack(side=LEFT)

    class TweakedCheckbutton(Checkbutton):
        def __init__(self, master, text: str, variable: object, key: str, state: str):
            Checkbutton.__init__(
                self,
                master=master,
                takefocus=False,
                text=text,
                variable=variable,
                command=lambda: change_in_dict(self),
                state=state,
                onvalue=True,
                offvalue=False
            )
            self.variable=variable
            self.dict_key=key

    # Creating a frame for controlling the behaviour of the bodies
    (user_control_frame := Frame(master=top_frame)).pack(side=TOP)

    (triangle_control_frame := LabelFrame(master=user_control_frame, 
                text="Selected species", labelanchor='n')).pack(side=TOP)

    # Creating a checkbutton for ignoring eating the plants
    key = 'dont-eat-plants'
    (dont_eat_plants := TweakedCheckbutton(
        master=triangle_control_frame,
        text="Don't eat plants",
        variable=BooleanVar(value=window_commands[key]),
        key=key,
        state=DISABLED
    )).grid(row=0, column=0, sticky=W, pady=8)
    checkbuttons_for_triangle.append(dont_eat_plants)

    # Creating a checkbutton for ignoring eating the bodies
    key = 'dont-eat-bodies'
    (dont_eat_bodies := TweakedCheckbutton(
        master=triangle_control_frame,
        text="Don't eat bodies",
        variable=BooleanVar(value=window_commands[key]),
        key=key,
        state=DISABLED
    )).grid(row=1, column=0, sticky=W, pady=8)
    checkbuttons_for_triangle.append(dont_eat_bodies)

    # Creating a checkbutton for ignoring escaping from bodies that are chasing
    key = 'ignore-chasers'
    (ignore_chasing_bodies := TweakedCheckbutton(
        master=triangle_control_frame,
        text='Ignore chasers',
        variable=BooleanVar(value=window_commands[key]),
        key=key,
        state=DISABLED
    )).grid(row=2, column=0, sticky=W, pady=8)
    checkbuttons_for_triangle.append(ignore_chasing_bodies)

    # Creating a checkbutton for making sure that if there is a body following a plant except the body of the user's species, that body will die on the path of going towards the plant
    key = 'smart-plant'
    (smart_plant_chasing := TweakedCheckbutton(
        master=triangle_control_frame,
        text='Smart plant chasing*',
        variable=BooleanVar(value=window_commands[key]),
        key=key,
        state=DISABLED
    )).grid(row=3, column=0, sticky=W, pady=8)
    checkbuttons_for_triangle.append(smart_plant_chasing)

    # Creating a checkbutton for making sure the same requirement is satisfied as in smart_plant_chasing
    key = 'smart-body'
    (smart_body_chasing := TweakedCheckbutton(
        master=triangle_control_frame,
        text='Smart body chasing*',
        variable=BooleanVar(value=window_commands[key]),
        key=key,
        state=DISABLED
    )).grid(row=4, column=0, sticky=W, pady=8)
    checkbuttons_for_triangle.append(smart_body_chasing)

    # Creating a LabelFrame to separte two sections of user_control_frame
    (evolution_control_frame := LabelFrame(
        master=user_control_frame,
        text="Evolution",
        labelanchor=N)).pack(side=TOP)

    # Creating a label with a title for the time-lapse scale
    Label(
        master=evolution_control_frame,
        text='Time-lapse',
    ).grid(row=0, column=0, sticky=W, padx=33, pady=8)

    # Creating a scale for selecting the evolution animations
    def timelapse_handle(speed: str):
        match speed:
            case '0':
                timelapse['label'] = NONE_LABEL
                window_commands['time-lapse-term'] = 0
            case '1':
                delete_all_crosses()
                timelapse['label'] = SHORT_TERM_LABEL
                window_commands['time-lapse-term'] = SHORT_TERM_SEC
            case '2':
                delete_all_crosses()
                timelapse['label'] = LONG_TERM_LABEL
                window_commands['time-lapse-term'] = LONG_TERM_SEC

    (timelapse := Scale(
        label=NONE_LABEL,
        master=evolution_control_frame,
        from_=0,
        to=2,
        orient=HORIZONTAL,
        length=120,
        showvalue=False,
        command=timelapse_handle
    )).grid(row=1, column=0, sticky=W, padx=5, pady=3)

    timelapse.set(0) # Setting the scale to 'none'

    # Creating a checkbutton for holding the start of the evolution back to select a body
    TweakedCheckbutton(
        master=evolution_control_frame,
        text='Hold the evolution\nstart back\nto select a body',
        variable=BooleanVar(value=window_commands[key]),
        key='hold-evolution-start-back',
        state=NORMAL
    ).grid(row=2, column=0, sticky=W, padx=4, pady=28)

    # Creating a checkbutton for display the results at the end of the evolution
    TweakedCheckbutton(
        master=evolution_control_frame,
        text='Display averaged\nproperties\nat the end\nof evolution',
        variable=BooleanVar(value=window_commands[key]),
        key='display-properties',
        state=NORMAL
    ).grid(row=3, column=0, sticky=W, padx=4, pady=9)

    # Creating a label for tips
    global_items.tip_text = StringVar()
    Label(textvariable=global_items.tip_text).pack(side=LEFT, padx=5)

    # Creating a LabelFrame with a title describing what the menu can be used for
    (menu_frame := LabelFrame(
        bd=0,
        text='Which body properties to display',
        labelanchor='n'
    )).pack(side=RIGHT, padx=5)

    # Creating a OptionMenu for selecting which properties have to be shown over the bodies
    def handle_selection(choice: str):
        window_commands['to-show-selected-property'] = choice

    menu_options = (
        'Nothing',
        '"Newly born" if newly born',
        'Current energy',
        'Speed',
        'Vision distance',
        'Procreation threshold',
        'Food preference',
        'Generation number',
        'Amount of bodies with this species',
        'ID of the species'
    )

    selected = StringVar(value=menu_options[0])
    (properties_menu := OptionMenu(
        menu_frame,
        selected,
        menu_options[0],
        *menu_options,
        direction='above',
        command=handle_selection
    )).pack(anchor='e')
    properties_menu.configure(width=30)

    # Creating the help button
    Button(
        text='?',
        width=2,
        command=show_help
    ).pack(side=RIGHT, pady=8, padx=2)

    # Creating the refresh button
    def refresh_request():
        window_commands['refresh'] = True

    global_items.refresh_button = Button(
        text='refresh',
        width=6,
        command=refresh_request
    )
    global_items.refresh_button.pack(side=RIGHT, pady=8, padx=2)

    # Creating the start/pause button
    def start_pause_request():
        if global_items.start_pause_button['text'] == START_TEXT:
            window_commands['run/pause'] = RUN
            global_items.start_pause_button['text'] = PAUSE_TEXT
        else:
            window_commands['run/pause'] = PAUSE
            global_items.start_pause_button['text'] = START_TEXT  

    global_items.start_pause_button = Button(
        width=1,
        text=START_TEXT,
        command=start_pause_request,
        state=DISABLED,
        font=Font(size=25)
    )
    global_items.start_pause_button.pack(side=RIGHT, pady=8, padx=2)

    window.after(0, evolution)
    window.mainloop()

window_handling()