from random import choice, seed
from copy import deepcopy
from time import time, sleep

from config import *
from global_items import bodies, handle, plants, data_for_smart_body
from evolution_functions import memory_things
from crosses import delete_all_crosses
from window_functions import update_progress, show_progress_bar, delete_progress_bar
from tips import show_tip
from global_items import window_commands
import global_items

@handle
def shape_ai_guess():
    (sqaure := select_ai_survivor()).shape = SQUARE
    if window_commands['hold-evolution-start-back']:
        for k in range(9):
            global_items.canvas.itemconfig(sqaure.image_reference, fill='black' if k % 2 == 0 else 'white')
            sleep(0.1)
            global_items.canvas.update()
            global_items.canvas.itemconfig(sqaure.image_reference, fill='#%02x%02x%02x' % sqaure.species)
            sleep(0.1)
            global_items.canvas.update()

def select_ai_survivor() -> object:
    show_tip('Working on the prediction of the AI...')

    # Storing the initial states of plants and bodies
    bodies_copy = [deepcopy(body) for body in bodies]
    plants_copy = [deepcopy(plant) for plant in plants]

    # Modelling the evolution
    data_for_smart_body['steps'] = 0
    initial_state = int(time())
    seed(initial_state)
    show_progress_bar()
    start = time()
    while (since_start := time() - start) <= AI_THINKS:
        memory_things()
        data_for_smart_body['steps'] += 1
        update_progress(since_start/AI_THINKS)
    delete_all_crosses()
    delete_progress_bar()
    seed(initial_state)
    
    survived_bodies = []
    for body in bodies:
        survived_bodies.append(deepcopy(body))

    # Recovering the initial states of plants and bodies
    bodies.clear()
    for body in bodies_copy:
        bodies.append(deepcopy(body))

    plants.clear()
    for plant in plants_copy:
        plants.add(deepcopy(plant))

    if survived_bodies == []:
        return choice(bodies)

    survived_bodies_dict_by_id: dict[int, int] = { # {ID: Amount of descendants}
        id: len([body for body in survived_bodies if body.species_id == id])
        for id in range(BODIES_AMOUNT)
    }

    max_descendants_by_id = max( # Returns the ID
        (dict_key for dict_key in survived_bodies_dict_by_id),
        key=survived_bodies_dict_by_id.get
    )
    
    for body in bodies:
        if body.species_id == max_descendants_by_id:
            return body # If the user select a body and changes it behaviour while the evolution, then the prediction of the AI might be not as precise