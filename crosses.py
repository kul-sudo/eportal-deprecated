from tkinter import PhotoImage
from time import time

from config import *
from images import CROSS_IMAGE
from global_items import handle

import global_items

class Cross:
    def __init__(self, x: float, y: float, birth_time: float):
        self.x = x
        self.y = y
        self.birth_time = birth_time
        self.image_reference = None

crosses_list: list[Cross] = []

def create_cross_image():
    global_items.cross_shape = PhotoImage(data=CROSS_IMAGE).subsample(CROSS_SIZE_RATIO, CROSS_SIZE_RATIO) # Registering a new shape with the plant_base64

def delete_old_cross(): # Deleting the cross
    if crosses_list != []:
        first_cross = crosses_list[0] # If it is required have to remove a cross, then this stamp is supposed to be the first one
        if first_cross.birth_time + CROSS_LIFETIME <= time():
            crosses_list.remove(first_cross)

def add_cross(x: float, y: float):
    crosses_list.append(Cross(x, y, time()))

def delete_all_crosses():
    global crosses_list
    crosses_list.clear()