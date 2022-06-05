from tkinter import NORMAL, DISABLED
from math import dist, ceil
from tkinter.ttk import Progressbar

from config import *
from draw_erase import change_shape, handle_body_properties, prepare_draw_handle
from global_items import handle, window_commands, bodies, evolution_status, window, checkbuttons_for_triangle
from tips import info_handle, mouse_clicked_on_body, prepare_info_handle

import global_items

def change_in_dict(button: object):
    '''Changing the corresponding value in the dictionary.'''
    window_commands[button.dict_key] = button.variable.get()

@handle
def start_pause_button_change_state(action: str): 
    global_items.start_pause_button.configure(state=NORMAL if action == ENABLE else DISABLED)
    window.update()

@handle
def pause_mode(enable:bool):
    if enable:
        window_commands['run/pause'] = PAUSE
        global_items.start_pause_button.configure(text=START_TEXT)
    else:
        window_commands['run/pause'] = RUN
        global_items.start_pause_button.configure(text=PAUSE_TEXT)
    window.update()


def mouse_bind():
    global bind
    bind = global_items.canvas.bind('<Button-1>', mouse_clicked)

def mouse_unbind():
    global_items.canvas.unbind('<Button-1>', bind)

replace_shapes = {
    CIRCLE: TRIANGLE,
    TRIANGLE: CIRCLE,
    RHOMBUS: SQUARE,
    SQUARE: RHOMBUS
}

def mouse_clicked(event):
    '''Maintaining the features that work with the mouse inside the evolution field.'''
    for body in bodies:
        if dist((event.x, event.y), (body.x+CANVAS_BORDER, body.y+CANVAS_BORDER)) <= HALF_BODY_SIZE*1.2:
            change_shape(body, replace_shapes[body.shape])
            mouse_clicked_on_body(body)
            handle_checkbuttons(NORMAL if body.shape == TRIANGLE else DISABLED)
            if evolution_status.selected_body is None:
                evolution_status.selected_body = body
            else:
                if body is evolution_status.selected_body:
                    evolution_status.selected_body = None
                else:
                    change_shape(evolution_status.selected_body, replace_shapes[evolution_status.selected_body.shape])
                    evolution_status.selected_body = body
            return

def user_select_body():
    '''Maintaining the process of the user selecting the body.'''
    @handle
    def selected() -> bool: # A separate function is required for the decorator to work along with it
        handle_body_properties()
        info_handle()
        return window_commands['run/pause'] == RUN
    prepare_info_handle()
    prepare_draw_handle()
    while not selected():
        continue

@handle
def handle_checkbuttons(action: str):
    '''Changing states of buttons which provide the access to the behaviour of the species which is selected by the user.'''
    for checkbutton in checkbuttons_for_triangle:
        checkbutton.configure(state=action)

@handle
def disable_checkbuttons_checkmarks():
    '''Removing the checkmarks of buttons which provide the access to the behaviour of the species which is selected by the user.'''
    for checkbutton in checkbuttons_for_triangle: 
        checkbutton.variable.set(False)

@handle
def restore_checkbuttons_checkmarks():
    '''Restoring the current states of checkmarks.'''
    for checkbutton in checkbuttons_for_triangle: 
        checkbutton.variable.set(window_commands[checkbutton.dict_key]) 

@handle
def set_checkbuttons_for_evolution():
    '''
    Deactivating all of the checkbuttons which provide the access to the behaviour of the species which is selected by the user and removing the checkmark of these checkbuttons
    if it's needed.
    '''
    if evolution_status.selected_body is None or evolution_status.selected_body.shape != TRIANGLE:
        disable_checkbuttons_checkmarks()
        handle_checkbuttons(DISABLED)

def show_progress_bar():
    global progress_bar, canvas_window, previous_value
    progress_bar = Progressbar(
        master=global_items.canvas,
        length=300,
        mode='determinate',
        maximum=100
    )

    canvas_window = global_items.canvas.create_window(
        HALF_EVOLUTION_FIELD_SIZE['width'], 
        HALF_EVOLUTION_FIELD_SIZE['height'],
        window=progress_bar
    )
                
    previous_value = 0

def update_progress(to_show: float):
    '''Progressing the progress of the progess bar.'''
    global previous_value
    new_value = ceil(to_show*100)
    if new_value > previous_value:
        progress_bar['value'] = new_value
        previous_value = new_value

def delete_progress_bar():
    global canvas_window
    try:
        global_items.canvas.delete(canvas_window)
    except NameError: # NameError is thrown if the progress bar does not exist yet
        pass   
