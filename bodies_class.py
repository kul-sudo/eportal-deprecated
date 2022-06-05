from random import random
from crosses import add_cross

from config import *
from global_items import data_for_smart_body, handle, distance_between_objects, random_attribute, bodies, plants, window_commands
import global_items

class BodyStatus:
    def __init__(self):
        self.description = None
        self.parameter = None

class Body: # The class of the Bodies
    def __init__(
        self,
        generation_n: int,
        energy: float,
        shape: str,
        food_preference: str,
        vision_distance: float,
        speed: float,
        procreation_threshold: float,
        color: tuple,
        species_id: int,
        x: float,
        y: float
    ):
        self.species_id = species_id
        self.status = BodyStatus()
        self.status.description = SLEEPING
        self.wrap = False # A boolean which says whether the body has just done a Wrap or not
        self.image_reference = None

        # Setting up the inborn properties of a body:
        self.species = color
        self.food_preference = food_preference
        self.vision_distance = vision_distance
        self.speed = speed
        self.procreation_threshold = procreation_threshold

        # Non-inborn properties
        self.x, self.y = x, y
        self.generation_n = generation_n
        self.current_lifetime = 0 # Calculated with the number of calls of one_action()
        self.energy = energy
        self.shape = shape

    @handle
    def one_action(self):
        '''Maintaining the behaviour of the bodies.'''
            
        # Increasing the lifetime by one every time the program uses one_action()
        self.current_lifetime += 1

        # Using energy of the body for a better vision distance
        self.energy -= self.vision_distance*ENERGY_FOR_VISION

        if self.status.description != SLEEPING: # If the body is not sleeping then it is moving (which is obvious)
            self.energy -= self.speed*ENERGY_FOR_MOVING

        # Checking whether it is time for body to die or not
        if self.energy <= 0:
            if window_commands['time-lapse-term'] == 0:
                add_cross(self.x, self.y)
            bodies.remove(self)
            return
        # Check if Wrap is needed (the action of moving a body into the opposite side of the evolution field)
        self.wrap = False # Wrapping is not going right now because wrap might be True on a new one_action() call
        if self.status.description == RUNNING_AWAY: # Only do the Wrap if the body we are working with is running away from another body
            x_new = self.x
            y_new = self.y

            if self.x > CANVAS_WIDTH:
                x_new = HALF_BODY_SIZE
            elif self.x < 0:
                x_new = CANVAS_WIDTH-HALF_BODY_SIZE
            
            if self.y > CANVAS_HEIGHT:
                y_new = HALF_BODY_SIZE
            elif self.y < 0:
                y_new = CANVAS_HEIGHT-HALF_BODY_SIZE
                
            if (x_new, y_new) != (self.x, self.y): # Making sure Wrap is needed
                self.wrap = True # Making draw_lines not draw lines across all the field when the prey has gone through a Wrap
                self.x, self.y = x_new, y_new
                self.status.description = SLEEPING
                return
        
        # Escaping pursuers
        visible_pursuers = tuple(filter(
            lambda body: body.status.description == FOLLOWING_BODY and body.status.parameter is self and distance_between_objects(self, body) <= self.vision_distance,
            bodies)) # visible_pursuers is a tuple which consists of all of the visible pursuers

        if visible_pursuers != ():
            if self.shape in SMART_BODY_SHAPES and data_for_smart_body['actions'] > data_for_smart_body['steps']:
                dangerous_pursuers = [] # All of the objects of visible_pursuers that can get to the place where self current is not dying on the way towards this
                for pursuer in visible_pursuers:
                    distance = distance_between_objects(self, pursuer)
                    time = distance/pursuer.speed
                    final_energy = pursuer.energy - time*total_energy_loss(pursuer)
                    if final_energy > 0: 
                        dangerous_pursuers.append(pursuer)
                if dangerous_pursuers != []: # Escaping the closest pursuers
                    closest_pursuer = min(dangerous_pursuers, key=lambda pursuer: distance_between_objects(self, pursuer))
                    self.one_step_from(closest_pursuer)
                    self.status.description = RUNNING_AWAY
                    self.status.parameter = closest_pursuer
                    return
            else:
                if not (self.shape == TRIANGLE and window_commands['ignore-chasers']):
                    closest_pursuer = min(visible_pursuers, key=lambda pursuer: distance_between_objects(self, pursuer))
                    self.one_step_from(closest_pursuer)
                    self.status.description = RUNNING_AWAY
                    self.status.parameter = closest_pursuer
                    return

        # Selecting food
        if self.shape == TRIANGLE:
            if window_commands['dont-eat-bodies']:
                found_body = None
            else:
                found_body = self.find_body()
            if window_commands['dont-eat-plants']:
                found_plant = None
            else:
                found_plant = self.find_plant()
        else:
            found_body = self.find_body()
            found_plant = self.find_plant()

        if found_body is None and found_plant is None:
            self.status.description = SLEEPING
            return
        elif found_body is None and found_plant is not None:
            self.status.description, self.status.parameter = found_plant
        elif found_body is not None and found_plant is None:
            self.status.description, self.status.parameter = found_body
        else:
            if self.food_preference == BODY:       
                self.status.description, self.status.parameter = found_body
            else:
                self.status.description, self.status.parameter = found_plant    

        # If the body chased another body and caught it along with the energy of the prey being lower that the energy of the catcher, then the prey is eaten by the catcher
        if self.status.description == FOLLOWING_BODY:
            prey = self.status.parameter
            self.one_step_to(prey)
            if distance_between_objects(self, prey) <= self.speed:
                if self.energy > prey.energy:
                    self.energy += prey.energy
                    bodies.remove(prey)
                    self.procreate()
                else:
                    self.status.description = SLEEPING   

        # If the body is going towards a plant and reaches it, then the plant it eaten
        if self.status.description == FOLLOWING_PLANT:
            plant_prey = self.status.parameter
            self.one_step_to(plant_prey)
            if distance_between_objects(self, plant_prey) <= self.speed:
                self.energy += PLANT_ENERGY
                plants.remove(plant_prey)
                self.procreate()
    
    def one_step(self, object_: object, direction: str):
        '''Stepping from/to an object.'''
        dx, dy = object_.x - self.x, object_.y - self.y
        distance = distance_between_objects(self, object_)
        coeff = self.speed/distance
        if direction == TO:
            self.x, self.y = self.x + coeff*dx, self.y + coeff*dy
        else:
            self.x, self.y = self.x - coeff*dx, self.y - coeff*dy   

    def one_step_from(self, pursuer: object):
        '''Stepping from the pursuer.'''
        self.one_step(pursuer, FROM)

    def one_step_to(self, pursued: object):
        '''Stepping to the pursued body.'''
        self.one_step(pursued, TO)

    def find_plant(self) -> tuple[str, object] | None:
        '''Finding the plant which is suitable for self.'''
        feasible_plants = []
        # feasible_plants consists of plants that are qualified as suitable for self by the following conditions:
        # Condition1: The plant is within the vision distance
        # Condition2: The plant is not going to be eaten by any of the bodies with the same species
        other_bodies = set(bodies) - {self}
        for plant in global_items.plants:
            Condition1 = distance_between_objects(self, plant) -\
                        global_items.half_plant_size <= self.vision_distance
            if not Condition1:
                continue

            Condition2 = not any(
                body.status.description == FOLLOWING_PLANT and
                body.status.parameter is plant and
                body.species == self.species
                for body in other_bodies
            )
            if not Condition2:
                continue
            # If all of the conditions are False, the plant can be appended to feasible_plants
            feasible_plants.append(plant)

        if feasible_plants == []:
            return None 
              
        if (self.shape in SMART_BODY_SHAPES and data_for_smart_body['actions'] > data_for_smart_body['steps']) \
            or (self.shape == TRIANGLE and window_commands['smart-plant']):
            profitable_plants = [] # The plants that are worth being eaten because the energy which is received from them can make up the energy that was spent to catch them
            for plant in feasible_plants:
                distance = distance_between_objects(self, plant)
                time = distance/self.speed
                self_final_energy = self.energy - time*total_energy_loss(self)
                if self_final_energy <= 0:
                    continue # Self will die before the plant is caught because of a low level of energy
                if self_final_energy + PLANT_ENERGY <= self.energy - time*self.vision_distance*ENERGY_FOR_VISION:
                    continue # It is not worth it to attempt to catch the plant in terms of the energy
                profitable_plants.append(plant)
            
            matchless_plants = [] # The plants from profitable_plants that can be caught by self faster than the competitors without dying
            for plant in profitable_plants:
                self_distance = distance_between_objects(self, plant)
                self_time = self_distance/self.speed

                competitors = filter(
                    lambda body: body.status.description == FOLLOWING_PLANT and body.status.parameter is plant,
                    other_bodies) # The bodies that are going towards the plant

                faster_competitors = [] # The bodies from competitors that will catch the plant earlier than self (the possibility of them dying on the path towards to plant is not taken into account)
                for body in competitors:
                    body_distance = distance_between_objects(body, plant)
                    body_time = body_distance/body.speed
                    if body_time <= self_time:
                        faster_competitors.append({'body': body, 'time': body_time})

                successful_competitors = [] # The bodies from faster_competitors that will catch the plant without dying
                for item in faster_competitors:
                    body = item['body']
                    if body.energy >= item['time']*total_energy_loss(body):
                        successful_competitors.append(body)
                
                if successful_competitors == []:
                    matchless_plants.append(plant) 
            
            if matchless_plants == []:
                return None
            return (
                FOLLOWING_PLANT,
                min(matchless_plants, key=lambda p: distance_between_objects(self, p))
            )
        else:
            return (
                FOLLOWING_PLANT,
                min(feasible_plants, key=lambda p: distance_between_objects(self, p)))

           
    def find_body(self) -> tuple[str, object] | None:
        '''Finding the body which is suitable for self.'''
        feasible_bodies = []
        # feasible_bodies consists of bodies that are qualified as suitable for self by the following conditions:
        # Condition1: The body has different species
        # Condition2: The body has a lower amount of energy
        # Condition3: The body is within the vision distance
        # Condition4: The body is not being chased by any of the bodies with the same species
        other_bodies = set(bodies) - {self}

        for another_body in other_bodies:
            Condition1 = another_body.species != self.species
            if not Condition1:
                continue

            Condition2 = self.energy > another_body.energy
            if not Condition2:
                continue

            Condition3 = distance_between_objects(self, another_body)-HALF_BODY_SIZE <= self.vision_distance
            if not Condition3:
                continue

            Condition4 = not any(
                body.status.description == FOLLOWING_BODY and
                body.status.parameter is another_body and
                body.species == self.species
                for body in other_bodies 
            )
            if not Condition4:
                continue
            
            feasible_bodies.append(another_body)

        if feasible_bodies == []:
            return None

        if (self.shape in SMART_BODY_SHAPES and data_for_smart_body['actions'] > data_for_smart_body['steps'])\
             or (self.shape == TRIANGLE and window_commands['smart-body']):
            wholesome_bodies = [] # Bodies that are worth being caught by self in terms of the energy (the difference of lost and achieved energy)
            for body in filter(lambda body: body.speed < self.speed, feasible_bodies):
                catch_time = time_to_reach(self, body) # Estimation of time which is needed for self to catch body
                body_final_energy = body.energy - catch_time*total_energy_loss(body) # Energy of the prey when it is caught (the chance of the prey dying is not considered)
                self_final_energy = self.energy - catch_time*total_energy_loss(self) # Energy of self when it catches the body (the chance of self dying is not considered)
                if body_final_energy <= 0:
                    continue # The body will die before it's caught because of a low level of energy
                if self_final_energy <= 0:
                    continue # Self will die before it's caught because of a low level of energy
                if self_final_energy + body_final_energy <= self.energy - catch_time*self.vision_distance*ENERGY_FOR_VISION: # Left part of the calculation contains the energy of self when it eats the body, and the right part contains the energy of self if it does not attempt to catch the body after the same time as if it would attempt to
                    continue # It is not worth it to attempt to catch the body in terms of the energy
                wholesome_bodies.append(body)
            
            profitable_bodies = [] # Bodies from wholesome_bodies that can be caught by self quicker than by the rest of the bodies that are current pursuing this body
            for body in wholesome_bodies:
                self_catch_time = time_to_reach(self, body)

                competitors = filter(
                    lambda b: b.status.description == FOLLOWING_BODY and b.status.parameter is body,
                    other_bodies) # Competitors for self
                
                if all(c for c in competitors if time_to_reach(c, body) > self_catch_time):
                    profitable_bodies.append(body)
            
            if profitable_bodies == []:
                return None
            return (FOLLOWING_BODY, min(profitable_bodies, key=lambda b: distance_between_objects(self, b)))
        else:
            return (
                FOLLOWING_BODY,
                min(feasible_bodies, key=lambda b: distance_between_objects(self, b))
            )
            
    def one_procreation(self, gap: int):
        '''Creating one child. This function is hereafter used for creating two children.'''
        body = Body(
            generation_n=self.generation_n+1,
            energy=self.energy/2,
            shape=self.shape,
            food_preference=self.food_preference if random() < FOOD_PREFERENCE_CHANCE_CHILD else BODY if self.food_preference == PLANT else PLANT,
            vision_distance=random_attribute(self.vision_distance, deviation=DEVIATION_OF_RANDOM_PROPERTIES),
            speed=random_attribute(self.speed, deviation=DEVIATION_OF_RANDOM_PROPERTIES),
            procreation_threshold=random_attribute(self.procreation_threshold, deviation=DEVIATION_OF_RANDOM_PROPERTIES),
            color=self.species,
            species_id=self.species_id,
            x=self.x+(0 if self.shape == RHOMBUS else gap),
            y=self.y+gap
        )

        bodies.append(body)

    def procreate(self):
        '''The process of procreating twice.'''
        if self.energy > self.procreation_threshold:
            # Creating 2 children with different gaps
            self.one_procreation(gap=PLACEMENT_GAP)
            self.one_procreation(gap=-PLACEMENT_GAP)
            bodies.remove(self) # The parent is removed from the array of the bodies as it has been split into its two children
        else: # If there isn't enough energy, the body falls asleep
            self.status.description = SLEEPING

def time_to_reach(pursuer: object, pursued: object) -> float: 
    '''
    Approximate estimation of time which is needed for pursuer to catch pursued.\n
    The estimation implies that throughout the pursuit pursuer chases pursued and pursued runs away.\n
    It is possible for pursued not to see pursuer at the beginning of the pursuit. This is what is not considered by this function.\n
    This function is only called when the speed of pursuer is greater than the speed of pursued.
    '''
    distance = distance_between_objects(pursuer, pursued)
    return distance/(pursuer.speed - pursued.speed)

def total_energy_loss(body: object) -> float: # Energy loss every time one_action() is called
    '''This function is never called alone. The output of it is always multiplied by a value of time.'''
    return ENERGY_FOR_VISION*body.vision_distance + ENERGY_FOR_MOVING*body.speed