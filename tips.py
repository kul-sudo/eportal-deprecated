import global_items
from global_items import handle, bodies
from math import dist
from config import *
from tkinter import NE, NW, SE, SW
from time import time

def show_tip(tip: str):
    '''Setting the text of the area of tips to tip.'''
    global_items.tip_text.set(tip)

def show_evolution_number():
    '''Updating the tip with the number of the current evolution.'''
    show_tip(f'The number of the evolution is {global_items.evolution_number}.')

def show_tip_for_body(body: object):
    '''Display a tip according to the shape of body.'''
    match body.shape:
        case global_items.CIRCLE:
            tip = 'Click on the body the species of which you think will turn out to survive the evolution.\nThe body you select will become a triangle.'
        case global_items.TRIANGLE:
            tip = 'Click on this body to turn it back into a circle and cancel your guess.'
        case global_items.SQUARE:
            tip = 'Click on this body to turn it into a rhombus. This rhombus means that\nboth AI and you think the species of this body will survive the evolution.'
        case global_items.RHOMBUS:
            tip = 'Click on this body to turn it back into a square and cancel\nyour guess.'
    show_tip(tip)

def mouse_clicked_on_body(body: object):
    '''Altering the text of the tip instantaneously.'''
    show_tip_for_body(body)

GAP = 3
DELAY = 1

previous_display_time = float('-inf')

def erase_information():
    global_items.canvas.delete('information')

@handle
def info_handle(tips_for_pause: bool):
    '''Handling the mouse hovering upon bodies and displaying all of the needed info.'''
    global previous_display_time
    now = time()
    if now < previous_display_time + DELAY:
        if global_items.canvas.gettags('information') != (): # If there is already a box displayed on canvas, then it is not time to show another box
            return
    if not tips_for_pause:
        show_tip('Put your cursor on a body.\nYou can click the body the descendants of which you think will survive the evolution.')
    erase_information()
    # Finding the coordinates of the mouse
    canvas_mouse_x = global_items.canvas.winfo_pointerx() - global_items.canvas.winfo_rootx()
    canvas_mouse_y = global_items.canvas.winfo_pointery() - global_items.canvas.winfo_rooty()
    for body in bodies:
        if dist((canvas_mouse_x, canvas_mouse_y),
                (body.x+CANVAS_BORDER, body.y+CANVAS_BORDER)) <= HALF_BODY_SIZE*1.2:
            selected_body = body
            previous_display_time = now
            break
    else:  
        return
    if not tips_for_pause:    
        show_tip_for_body(selected_body)
    # Making some corrections to the x and the y of the information window because clicks on the body are considered clicks on the window whenever it overlaps the body, therefore the clicks are not registered
    if selected_body.x >= HALF_EVOLUTION_FIELD_SIZE['width'] and selected_body.y >= HALF_EVOLUTION_FIELD_SIZE['height']:
        corner, dx, dy = SE, -HALF_BODY_SIZE, -HALF_BODY_SIZE
    elif selected_body.x < HALF_EVOLUTION_FIELD_SIZE['width'] and selected_body.y > HALF_EVOLUTION_FIELD_SIZE['height']:
        corner, dx, dy = SW, HALF_BODY_SIZE, -HALF_BODY_SIZE
    elif selected_body.x <= HALF_EVOLUTION_FIELD_SIZE['width'] and selected_body.y <= HALF_EVOLUTION_FIELD_SIZE['height']:
        corner, dx, dy = NW, HALF_BODY_SIZE, HALF_BODY_SIZE
    else:
        corner, dx, dy = NE, -HALF_BODY_SIZE, HALF_BODY_SIZE
    
    information_tuple = (
        f"Energy: {round(selected_body.energy)}",
        f"Speed: {round(selected_body.speed*RATIO)}",
        f"Vision distance: {round(selected_body.vision_distance)}",
        f"Procreation threshold: {round(selected_body.procreation_threshold)}",
        f"Food preference: {selected_body.food_preference}",
        f"Generation number: {selected_body.generation_n}",
        f"Amount of bodies with this species: {len([body_ for body_ in global_items.bodies if body_.species == selected_body.species])}"
    )

    # Creating the information box
    information_text = global_items.canvas.create_text(
        selected_body.x + CANVAS_BORDER + dx,
        selected_body.y + CANVAS_BORDER + dy,
        text='\n'.join(information_tuple),
        tags='information',
        anchor=corner
    )

    estimated_info_box_size = global_items.canvas.bbox(information_text)
    border = global_items.canvas.create_rectangle(
        (estimated_info_box_size[0]-GAP,
        estimated_info_box_size[1]-GAP,
        estimated_info_box_size[2]+GAP,
        estimated_info_box_size[3]+GAP),
        tags='information', fill='white')
    global_items.canvas.tag_raise(information_text, border)