from typing import Callable
from tkinter import TclError, Tk
from time import time
from sys import exit as sys_exit
from math import dist
from random import uniform, randrange

from config import *

window_commands: dict[str, bool | int] = {
    'run/pause': PAUSE,
    'to-show-selected-property': 'Nothing',
    'hold-evolution-start-back': True,
    'display-properties': True,
    'time-lapse-term': 0,
    'dont-eat-plants': False,
    'dont-eat-bodies': False,
    'ignore-chasers': False,
    'smart-plant': True,
    'smart-body': True,
    'refresh': False
}

def center_window(window: object):
    '''Centering a window on the screen.'''
    window.update()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    x = round(screen_width/2 - window_width/2)
    y = round(screen_height/2 - window_height/2)
    window.geometry(f'+{x}+{y}')

last_updating_time = time()

class ExceptionToRestart(Exception):
    pass

def time_to_update() -> bool:
    '''Checking if it is time to update the window where the evolution takes place.'''
    global last_updating_time
    now = time()
    if now > last_updating_time + DELTA:
        last_updating_time = now
        return True
    return False

def handle(func: Callable) -> Callable:
    '''Maintaining calls of functions making sure it is not time to do anything except this function which can affect the program.'''
    def wrapper(*arg, **kwargs):
        try:
            window.winfo_exists()
            # TclError is thrown if the window is closed with the cross
        except TclError:
            sys_exit()

        if time_to_update():
            window.update()
        if window_commands['refresh']:
            window_commands['refresh'] = False
            raise ExceptionToRestart     
        try: # The window might be closed by these time this command is accomplished, so the actions with the window are impossible
            return func(*arg, **kwargs)
        except TclError:
            sys_exit()
    return wrapper

def distance_between_objects(object1: object, object2: object) -> float:
    return dist((object1.x, object1.y),
                (object2.x, object2.y))

def random_attribute(attribute, deviation: float) -> float:
    return uniform(attribute-deviation*attribute, attribute+deviation*attribute)

def random_place(shape_size: int) -> tuple[int, int]:
    max_horizontal = CANVAS_WIDTH - shape_size
    max_vertical = CANVAS_HEIGHT - shape_size
    return randrange(shape_size, max_horizontal), randrange(shape_size, max_vertical)

class EvolutionStatus:
    def __init__(self):
        self.description = None
        self.selected_body = None
        self.survivor = None

window = Tk()
evolution_status = EvolutionStatus()
plants: set[object] = set()
bodies: list[object] = []
checkbuttons_for_triangle: list[object] = []
progenitor_properties: dict[str, dict] = {}
data_for_smart_body = {'steps': 0, 'actions': 0}