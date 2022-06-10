from typing import Callable
from tkinter import LAST, S

from config import *
from global_items import evolution_status, distance_between_objects, bodies, plants, window_commands
from crosses import crosses_list

import config
import global_items

def create_shape_bodies(body: object, shape: Callable) -> int:
    center_x, center_y = body.x+CANVAS_BORDER, body.y+CANVAS_BORDER
    return shape(
        center_x - HALF_BODY_SIZE,
        center_y - HALF_BODY_SIZE,
        center_x + HALF_BODY_SIZE,
        center_y + HALF_BODY_SIZE,
        fill='#%02x%02x%02x' % body.species,
        width=0,
        tags='body'
    )

# Bodies
def update_bodies():
    global_items.canvas.delete('body')
    for body in bodies:
        match body.shape:
            case config.CIRCLE:
                body.image_reference = create_shape_bodies(body, global_items.canvas.create_oval)
            case config.SQUARE:
                body.image_reference = create_shape_bodies(body, global_items.canvas.create_rectangle)
            case config.TRIANGLE:
                draw_body_triangle(body)
            case config.RHOMBUS:
                draw_body_rhombus(body)

# Plants
drawn_plants: set[object] = set()

def update_plants():
    global drawn_plants

    for plant in drawn_plants - plants:
        global_items.canvas.delete(plant.image_reference)

    for plant in plants - drawn_plants:
        plant.image_reference = global_items.canvas.create_image(
            plant.x+CANVAS_BORDER,
            plant.y+CANVAS_BORDER,
            image=global_items.plant_shape,
            tags='plant'
        )

    drawn_plants = plants.copy()

# Crosses
drawn_crosses: set[object] = set()

def update_crosses():
    global drawn_crosses

    crosses_set: set[object] = set(crosses_list) # Creating a separate set for it to be handy to subtract a set from a set. Set of crosses that are due on the evolution field

    for cross in drawn_crosses - crosses_set:
        global_items.canvas.delete(cross.image_reference)

    for cross in crosses_set - drawn_crosses:
        cross.image_reference = global_items.canvas.create_image(
            cross.x+CANVAS_BORDER,
            cross.y+CANVAS_BORDER,
            image=global_items.cross_shape,
            tags='cross'
        )
    drawn_crosses = crosses_set.copy()

# Arrows
def append_arrow(body: object):
    prey = body.status.parameter
    prey_is_body = body.status.description == FOLLOWING_BODY
    dist = distance_between_objects(body, prey)
    min_distance = HALF_BODY_SIZE if prey_is_body else global_items.half_plant_min_size
    if dist < min_distance:
        return
    sinus = (prey.y - body.y)/dist
    cosine = (prey.x - body.x)/dist
    arrow_start_x = body.x + HALF_BODY_SIZE*cosine
    arrow_start_y = body.y + HALF_BODY_SIZE*sinus
    global_items.canvas.create_line(
        arrow_start_x+CANVAS_BORDER, arrow_start_y+CANVAS_BORDER,
        prey.x+CANVAS_BORDER, prey.y+CANVAS_BORDER,
        arrow=LAST, arrowshape=(5, 5, 5), tags='arrow', dash=(4, 1))

def update_arrows():
    global_items.canvas.delete('arrow')
    for body in bodies:
        if body.status.description in (FOLLOWING_BODY, FOLLOWING_PLANT):
            if body.status.description == FOLLOWING_BODY and body.status.parameter.wrap:
                continue
            append_arrow(body)

def draw_triangle(x: float, y: float, color: tuple) -> int:
    return global_items.canvas.create_polygon(
        x, y-R_TRIANGLE, x+TRIANGLE_WIDTH_2,
        y+D_TIANGLE, x-TRIANGLE_WIDTH_2, y+D_TIANGLE,
        fill='#%02x%02x%02x' % color,
        tags='body')

def draw_rhombus(x: float, y: float, color: tuple):
    return global_items.canvas.create_polygon(
        x, y+HALF_RHOMBUS_SIZE, x+HALF_RHOMBUS_SIZE, y,
        x, y-HALF_RHOMBUS_SIZE, x-HALF_RHOMBUS_SIZE, y, 
        fill='#%02x%02x%02x' % color,
        tags='body')

def draw_body_rhombus(body: object):
    return draw_rhombus(body.x+CANVAS_BORDER, body.y+CANVAS_BORDER, body.species)

def draw_body_triangle(body: object):
    return draw_triangle(body.x+CANVAS_BORDER, body.y+CANVAS_BORDER, body.species)

def change_shape(body: object, into: int):
    global_items.canvas.delete(body.image_reference)
    match into:
        case config.CIRCLE:
            body.image_reference = create_shape_bodies(body, global_items.canvas.create_oval)
        case config.TRIANGLE:
            body.image_reference = draw_body_triangle(body)
        case config.RHOMBUS:
            body.image_reference = draw_body_rhombus(body)
        case config.SQUARE:
            body.image_reference = create_shape_bodies(body, global_items.canvas.create_rectangle)
    body.shape = into

# Vision distance circle
def draw_one_vision_distance_circle(body: object):
    center_x, center_y = body.x+CANVAS_BORDER, body.y+CANVAS_BORDER
    radius = body.vision_distance-global_items.half_image_size
    global_items.canvas.create_oval(
        center_x-radius, center_y-radius,
        center_x+radius, center_y+radius,
        outline='#%02x%02x%02x' % body.species,
        tags='circle'
    )

def erase_circles():
    global_items.canvas.delete('circle')

def update_vision_distance_circles():
    for body in bodies:
        draw_one_vision_distance_circle(body)

# Writing properties of bodies over them
def display_property(body: object,text: str):
    center_x, center_y = body.x+CANVAS_BORDER, body.y+CANVAS_BORDER
    global_items.canvas.create_text(
        center_x, center_y-HALF_BODY_SIZE,
        text=text,
        tags='property',
        anchor=S
    )    

def handle_body_properties():    
    erase_body_properties()
    erase_circles()
    for body in bodies:
        match window_commands['to-show-selected-property']:  
            case '"Newly born" if newly born':
                display_property(body=body, text='Newly born' if body.current_lifetime < NEWLY_BORN_PERIOD and body.generation_n != 0 else '')
            case 'Current energy':
                display_property(body=body, text=round(body.energy))
            case 'Speed':
                display_property(body=body, text=round(body.speed*RATIO))
            case 'Procreation threshold':
                display_property(body=body, text=round(body.procreation_threshold))
            case 'Food preference':
                display_property(body=body, text=body.food_preference)
            case 'Generation number':
                display_property(body=body, text=body.generation_n)
            case 'Amount of bodies with this species':
                display_property(body=body, text=len(tuple(filter(lambda body_: body_.species == body.species, bodies))))
            case 'ID of the species':
                display_property(body=body, text = body.species_id)
            case 'Vision distance':
                update_vision_distance_circles()
                return

def erase_body_properties():
    global_items.canvas.delete('property')