from tkinter import DISABLED
from config import *
from bodies_functions import create_zero_generation, delete_all_bodies
from plants import create_initial_plants, create_plant_image, delete_all_plants
from draw_erase import erase_body_properties, erase_circles, update_arrows, update_bodies, update_crosses, update_plants
from crosses import create_cross_image, delete_all_crosses
from ai import shape_ai_guess
from window_functions import delete_progress_bar, set_checkbuttons_for_evolution, disable_checkbuttons_checkmarks, handle_checkbuttons, restore_checkbuttons_checkmarks, start_pause_button_change_state, pause_mode, user_select_body, mouse_bind, mouse_unbind
from evolution_functions import one_evolution, get_survivor_progenitor_properties
from display_results import display_results
from global_items import ExceptionToRestart, window_commands, evolution_status
from tips import show_tip, show_evolution_number, erase_information
import global_items

global_items.evolution_number = 0

def evolution():
    create_plant_image()
    create_cross_image()
    while True:
        # try-except is required for the start button to work as a refresh button if the evolution is currently going
        try:
            evolution_status.description = CONTROL_PREPARATION
            handle_checkbuttons(DISABLED)
            disable_checkbuttons_checkmarks()
            start_pause_button_change_state(DISABLED)
            evolution_status.description = DELETE_EVERYTHING
            delete_progress_bar()
            show_tip('')
            erase_information()
            erase_body_properties()
            erase_circles()
            # Nothing in DELETE_EVERYTHING is done if there was no preceding evolution
            delete_all_bodies()
            update_bodies()
            delete_all_plants()
            update_plants()
            delete_all_crosses()
            update_crosses()
            update_arrows()
            evolution_status.description = EVOLUTION_PREPARATION
            create_zero_generation()
            create_initial_plants()
            update_bodies()
            update_plants()
            shape_ai_guess()
            update_bodies()
            start_pause_button_change_state(ENABLE)
            pause_mode(False)
            if window_commands['hold-evolution-start-back']:
                evolution_status.description = USER_SELECTING_BODY
                evolution_status.selected_body = None
                mouse_bind()
                pause_mode(True)
                restore_checkbuttons_checkmarks()
                user_select_body()
                mouse_unbind()
                erase_information()
            evolution_status.description = EVOLUTION
            evolution_status.survivor = None
            set_checkbuttons_for_evolution()
            global_items.evolution_number += 1
            show_evolution_number()
            one_evolution()
            start_pause_button_change_state(DISABLE)
            handle_checkbuttons(DISABLED)
            disable_checkbuttons_checkmarks()
            '''get_survivor_progenitor_properties() changes the status with "draw" or "won"'''
            get_survivor_progenitor_properties()
            if window_commands['display-properties']:
                display_results()
        except ExceptionToRestart:
            continue