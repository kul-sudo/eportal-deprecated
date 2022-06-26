from math import dist
from random import randrange, random

from bodies_class import Body
from config import *
from global_items import distance_between_objects, handle, random_attribute, random_place, bodies, progenitor_properties, handle

def create_zero_generation():
    '''Creating the zeroth generation of bodies.'''
    global used_colours
    used_colours = [PLANT_COLOUR]
    for id_ in range(BODIES_AMOUNT):
        create_one_body(id_)

@handle
def suitable_colours(expected_colour: tuple[int, int, int], used_colour: tuple[int, int, int], distance: int | float) -> bool:
    '''Making sure expected_colour is different enough from used_colour using the distance formula.'''
    return dist(expected_colour, used_colour) >= distance

@handle
def create_one_body(id_: int):
    distance = MAX_COLOUR_DISTANCE
    while True:
        expected_colour = (randrange(0, MAXIMUM_COLOUR), randrange(0, MAXIMUM_COLOUR), randrange(0, MAXIMUM_COLOUR))
        if expected_colour in used_colours:
            continue
        if all(suitable_colours(expected_colour, used_colour, distance) for used_colour in used_colours):
            break
        distance -= 0.04

    used_colours.append(expected_colour)

    body = Body(
        generation_n=0,
        energy=random_attribute(INITIAL_ENERGY, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        shape=CIRCLE,
        food_preference=PLANT if random() < PLANT_PREFERENCE_CHANCE else BODY,
        vision_distance=random_attribute(VISION_DISTANCE, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        speed=random_attribute(BODY_SPEED, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        procreation_threshold=random_attribute(PROCREATION_THRESHOLD, deviation=DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION),
        color=expected_colour,
        species_id=id_,
        x=0,
        y=0
    )

    while True:
        body.x, body.y = random_place(shape_size=BODY_SIZE)
        if all(distance_between_objects(body, another_body) > DOUBLE_BODY_SIZE for another_body in bodies):
            break
    bodies.append(body)
    
    progenitor_properties[body.species_id] = {
        'progenitor_food_preference': body.food_preference,
        'progenitor_vision_distance': body.vision_distance,
        'progenitor_body_speed': body.speed,
        'progenitor_procreation_threshold': body.procreation_threshold,
        'progenitor_energy': body.energy,
        'progenitor_x': body.x,
        'progenitor_y': body.y
    }

@handle
def delete_all_bodies():
    bodies.clear()
    progenitor_properties.clear()

def no_triangles():
    return tuple(filter(lambda body: body.shape == TRIANGLE, bodies)) == ()