from tkinter.messagebox import showinfo
from statistics import fmean

from config import *
from global_items import handle, bodies, evolution_status

@handle
def display_results():
    write_text_eventual = ''
    if bodies != []:
        bodies_amount = len(bodies)
        bodies_zero_element_shape = bodies[0].shape

        averaged = {
            'generation_n': round(fmean(body.generation_n for body in bodies)),
            'plant_preference': round(fmean(1 if body.food_preference == PLANT else 0 for body in bodies)), # Percent of bodies preferring plants
            'vision_distance': round(fmean(body.vision_distance for body in bodies)),
            'body_speed': round(fmean(body.speed for body in bodies)*RATIO),
            'procreation_threshold': round(fmean(body.procreation_threshold for body in bodies)),
            'energy': round(fmean(body.energy for body in bodies)),
            'descendants left': bodies_amount,
        }

        averaged_analysis = {}

        one_species_survived_line = 'One of the species has survived'
        average_generation_number = f'The average generation number of the bodies of the survived species: {averaged["generation_n"]}'
        
        user_predicted_line = 'You predicted the survivor of the evolution correctly' if bodies_zero_element_shape in (TRIANGLE, RHOMBUS) else ''

        ai_predicted_line = 'The AI guessed the survivor of the evolution' if bodies_zero_element_shape in (SQUARE, RHOMBUS) else ''

        def ending() -> str: # Handling the 's' at the end of the word 'descendant'
            return f"{bodies_amount} descendant{'s' if bodies_amount > 1 else ''} left"

        descendants_left_line = ending()

        initial_values = {
            'vision_distance': VISION_DISTANCE,
            'body_speed': BODY_SPEED,
            'procreation_threshold': PROCREATION_THRESHOLD,
            'energy': INITIAL_ENERGY
        }

        plant_preference_chance_text_turtle = round(sum(1 if body.food_preference == PLANT else 0 for body in bodies)/bodies_amount*100) # Percent of bodies preferring plants
        for property in averaged:
            if property not in ('generation_n', 'descendants left'):
                if property == 'plant_preference':
                    averaged_analysis['plant_preference-now'] = f'The chance that the food preference is "plant" for the survived species now: {plant_preference_chance_text_turtle}%'
                    averaged_analysis['plant_preference-initial'] = f'The chance that the food preference is "plant" for every species initially: {round(PLANT_PREFERENCE_CHANCE*RATIO)}%\n'
                    averaged_analysis['body_preference-now'] = f'The chance that the food preference is "body" for the survived species now: {100-plant_preference_chance_text_turtle}%'
                    averaged_analysis['body_preference-initial'] = f'The chance that the food preference is "body" for every species initially: {100-round(PLANT_PREFERENCE_CHANCE*RATIO)}%\n'
                else:
                    averaged_analysis[property+'-now'] = f'The average {property.replace("_", " ")} of the survived species now:\xa0{averaged[property]}'
                    value_ = initial_values[property]*100 if float(initial_values[property]) != int(initial_values[property]) else initial_values[property]
                    averaged_analysis[property+'-initial'] = f'The average {property.replace("_", " ")} for every species initially:\xa0{int(value_)}\n'

        write_text = [
            one_species_survived_line,
            user_predicted_line,
            ai_predicted_line,
            descendants_left_line+'\n',
            average_generation_number+'\n'] + [averaged_analysis[text] for text in averaged_analysis]
        
        for text in write_text:
            if text != '':
                write_text_eventual += text+'\n'
    else:
        write_text_eventual = 'Neither of the species\nhas survived'

    showinfo(title=TITLE, message=write_text_eventual)