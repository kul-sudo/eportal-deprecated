from pygame.time import Clock
from time import time
from tkinter import DISABLED

from config import *
from plants import create_plant
from crosses import delete_old_cross
from bodies_functions import progenitor_properties
from draw_erase import prepare_draw_handle, handle_body_properties, update_arrows, update_crosses, update_plants, update_bodies
from global_items import data_for_smart_body, handle, window_commands, bodies, evolution_status
from tips import prepare_info_handle, info_handle, erase_information, show_tip, show_evolution_number
from window_functions import handle_checkbuttons, disable_checkbuttons_checkmarks
from bodies_functions import no_triangles
import global_items

fps_clock = Clock()

def one_evolution():
    handle_body_properties()
    data_for_smart_body['actions'] = 0

    while True:
        one_evolution_step()
        if window_commands['time-lapse-term'] == 0:
            fps_clock.tick(FPS)
        if bodies == []:
            evolution_status.description = DRAW
            return
        if len({body.species for body in bodies}) == 1:
            evolution_status.description = WON
            return

def memory_things():
    data_for_smart_body['actions'] += 1
    for body in bodies:
        body.one_action()
    create_plant(chance=PLANT_CHANCE)

@handle
def one_evolution_step():
    if window_commands['time-lapse-term'] == 0:
        memory_things()
    else:
        start = time()
        while time() <= start + window_commands['time-lapse-term']:
            memory_things()
            if window_commands['run/pause'] == PAUSE:
                break
    erase_information()
    update_plants()
    update_bodies()
    update_arrows()
    delete_old_cross()
    update_crosses()
    handle_body_properties()
    global_items.canvas.update()
    if no_triangles():
      handle_checkbuttons(DISABLED)
      disable_checkbuttons_checkmarks()
    if window_commands['run/pause'] == PAUSE:
        evolution_status.description = ON_PAUSE
        show_tip('Put your cursor on a body.')
        prepare_info_handle()
        prepare_draw_handle()
        while window_commands['run/pause'] == PAUSE:
            handle_body_properties()
            info_handle()
        evolution_status.description = EVOLUTION
        show_evolution_number()

# Analysis
@handle
def get_survivor_progenitor_properties():
    global progenitor_properties_of_survivor_species
    if bodies == []:
        evolution_status.description = DRAW
    else:
        survivor_properties = progenitor_properties[bodies[0].species_id]
        evolution_status.survivor = {
            'progenitor': {
                'food_preference': survivor_properties['progenitor_food_preference'],
                'vision_distance': survivor_properties['progenitor_vision_distance'],
                'body_speed': survivor_properties['progenitor_body_speed'],
                'procreation_threshold': survivor_properties['progenitor_procreation_threshold'],
                'energy': survivor_properties['progenitor_energy'],
                'x': survivor_properties['progenitor_x'],
                'y': survivor_properties['progenitor_y']
            },
            "prediction of the AI was correct": bodies[0].shape in (SQUARE, RHOMBUS),
            "user's prediction was correct": bodies[0].shape in (TRIANGLE, RHOMBUS)
        }
        evolution_status.description = WON