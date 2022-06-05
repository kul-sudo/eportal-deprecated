TEST_MODE = False

from math import sqrt

# Common settings for windows
TITLE = 'eportal'

# Window settings
WINDOW_SIZE = {'width': 1100, 'height': 550}
FPS = 80

# Scale
SCALE_MAX = 500
NONE_SPACES = ' '*13
SHORT_TERM_SPACES = ' '*9
LONG_TERM_SPACES = ' '*9

NONE_LABEL = NONE_SPACES + 'none'
SHORT_TERM_LABEL = SHORT_TERM_SPACES + 'short term'
LONG_TERM_LABEL = LONG_TERM_SPACES + 'long term'

SHORT_TERM_SEC = 0.3
LONG_TERM_SEC = 3

ENABLE = 1
DISABLE = 0

# Buttons
START_TEXT = '▷'
PAUSE_TEXT = '⏸︎'
RUN = 0
PAUSE = 1

# Help maintenance
GEOMETRY_RATIO = 0.7
POPULATED_ROOM = 80 # Room populated by the bottom items of the help window (defined experimentally)
HELP_SCROLLED_TEXT_FONT_SIZE = 10 # The initial height of the letters in points
SCROLLED_TEXT_FONT_SIZE_IN_PIXELS = HELP_SCROLLED_TEXT_FONT_SIZE*1.3333 # Retrieving the text with its size being transformed from points into pixels (1.333 must not be changed)
SCROLLED_FONT_SIZE_GAP_HEIGHT = SCROLLED_TEXT_FONT_SIZE_IN_PIXELS*1.13 # Retrieving the height of lines (the factor must not be changed)
LETTER_WIDTH = SCROLLED_TEXT_FONT_SIZE_IN_PIXELS/2 # Retrieving the width of letters (the divisior must not be changed)
TEXT_COLOR = '#ffffff'
HELP_WINDOW_BG = '#303030'

# Canvas
CANVAS_BORDER = 2 # Width of the outline of canvas
RIGHT_BUTTON_AREA_SIZE = 150
BOTTOM_BUTTON_AREA_SIZE = 50
CANVAS_WIDTH = WINDOW_SIZE['width'] - RIGHT_BUTTON_AREA_SIZE # Width of canvas
CANVAS_HEIGHT = WINDOW_SIZE['height'] - BOTTOM_BUTTON_AREA_SIZE # Height of canvas

HALF_EVOLUTION_FIELD_SIZE = {
    'width': CANVAS_WIDTH/2,
    'height': CANVAS_HEIGHT/2
}
    
# The canvas border enframes the canvas while the evolution field (the field where the graphics are painted) saves the size of the canvas. The (0, 0) coordinates for the evolution field equal the (CANVAS_BORDER, CANVAS_BORDER) coordinates for the canvas. While the evolution is going, nominal coordinates of the evolution field are used. While displaying the evolution, nominal coordinates are transformed into coordinates that are suitable for canvas


# Bodies
# Shapes
BODY_SIZE = 10 # Size of the Bodies
DOUBLE_BODY_SIZE = BODY_SIZE*2

NEWLY_BORN_PERIOD = FPS*1.2 # When time-lapse is 'none', 1.2 seconds is the period of time when the body is newly born

TRIANGLE = 0
CIRCLE = 1
SQUARE = 2
RHOMBUS = 3
SMART_BODY_SHAPES = (SQUARE, RHOMBUS)

# Triangle shape
TRIANGLE_WIDTH = BODY_SIZE*1.1 # Width of the triangle base
# The further constants are only calculations
TRIANGLE_WIDTH_2 = TRIANGLE_WIDTH/2
SQRT_OF_THREE = sqrt(3)
R_TRIANGLE = TRIANGLE_WIDTH/SQRT_OF_THREE # Radius of the circumscribed circle
D_TIANGLE = (TRIANGLE_WIDTH*SQRT_OF_THREE)/2 - R_TRIANGLE # Triangle height - R_TRIANGLE

# Rhombus shape
RHOMBUS_SIZE = BODY_SIZE*1.4
HALF_RHOMBUS_SIZE = RHOMBUS_SIZE/2

# Food preference
BODY = 'bodies'
PLANT = 'plants'

# Status
SLEEPING = 0
RUNNING_AWAY = 1
FOLLOWING_PLANT = 2
FOLLOWING_BODY = 3

CONTROL_PREPARATION = 0
DELETE_EVERYTHING = 1
EVOLUTION_PREPARATION = 2
EVOLUTION = 3
USER_SELECTING_BODY = 4
ON_PAUSE = 5

FROM = 0
TO = 1

# Related to plants
PLANT_ENERGY = 100
PLANT_PREFERENCE_CHANCE = 0.5 # The chance that the body will prefer eating plant
PROCREATION_THRESHOLD = 5*PLANT_ENERGY

# Appearance
VISION_DISTANCE = 75
HALF_BODY_SIZE = BODY_SIZE/2
MAXIMUM_COLOUR = 220
MAX_COLOUR_DISTANCE = sqrt(3*MAXIMUM_COLOUR**2) # This is the maximum of sqrt((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)

# First generation
PLANT_ENERGY = 100 # Energy to a body for eating a plant
INITIAL_ENERGY = 4*PLANT_ENERGY # Initial energy at the start for the body not to die immediately

# Procreating
FOOD_PREFERENCE_CHANCE_CHILD = 0.9 # The chance that the child will inherit the food preference of the parent
DEVIATION_OF_RANDOM_PROPERTIES = 0.1 # Proportionates to standard deviation
DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION = 0.4 # Proportionates to standard deviation for the zero generation
PLACEMENT_GAP = 2.5

BODY_SPEED = 0.6
BODIES_AMOUNT = 20 if TEST_MODE is False else 1 # Amount of Bodies on the window
ENERGY_FOR_VISION = 0.0001*PLANT_ENERGY if TEST_MODE is False else 534354534*PLANT_ENERGY # Energy spent for vision
ENERGY_FOR_MOVING = 0.0001*PLANT_ENERGY if TEST_MODE is False else 534354534*PLANT_ENERGY # Energy spent for moving

# Plants
PLANT_COLOUR = (14, 209, 69) # Not defining the colour, but saying that the RGB of the plant is this one
TIMES_ATTEMPTED = 1000 # Limit of times for trying to place a plant on the window
PLANT_SIZE_RATIO = 25 # Higher => smaller
PLANT_CHANCE = 0.2 if TEST_MODE is False else 0 # The chance (percent = PLANT_CHANCE * 100) of Plant emerging
INITIALLY_PLANTED = BODIES_AMOUNT*3 if TEST_MODE is False else 100 # Amount of plants that have to be planted initially

# Crosses
CROSS_LIFETIME = 3 # Lifetime of a cross

# Cross appearance
CROSS_SIZE_RATIO = 3 # Higher => smaller

# AI
# Standard deviations
RATIO_BODY_PROPERTIES = DEVIATION_OF_RANDOM_PROPERTIES_ZERO_GENERATION/sqrt(3)
SIGMA_VISION_DISTANCE = RATIO_BODY_PROPERTIES*VISION_DISTANCE
SIGMA_BODY_SPEED = RATIO_BODY_PROPERTIES*BODY_SPEED
SIGMA_PROCREATION_THRESHHOLD = RATIO_BODY_PROPERTIES*PROCREATION_THRESHOLD

WON = 0
DRAW = 1

# Display results
RATIO = 100 # Making the results that are displayed more readable

# Other
DELTA = 0.1 # Window update every DELTA seconds

AI_THINKS = 5 # In seconds