![logo](https://user-images.githubusercontent.com/95244851/172011644-34148bdb-7509-4fec-8ba4-ce3158b5f1bf.png)

# What is eportal?
Eportal can be considered a simulator, because it demonstrates how evolution works, and a game, because you can compete with the [AI](#ai) in guessing which species will survive the evolution.
<br>

When the evolution begins, great battles begin along with it; bodies do their best to populate as much room as possible for their species to win; some of them become passive, eating plants and procreating, some of them become aggressive, trying to attack the bodies of other species.
<br>

And one of the most important things is that you don't have to struggle to make out which species is winning and which one is losing, because the graphics are extremely clear and plain.
<br>

# The process of evolution
Some of the bodies prefer eating plants and some of them prefer eating other bodies. The plant-eaters try to find a suitable plant, but if they don't find a suitable plant, then they try to find a suitable body, and the same, but vice versa, for body-eaters. After a body-eater finds a body, it makes sure that body is weaker (has a lower energy).

Note that the behaviour of the bodies of the selected species can be changed ([check out the "Selected species" section of Controls](#controls))
<br>

Properties is also an important part of the process of evolution, so it is recommended to check out [more about properties of bodies](#more-properties).

Whenever a body goes over a plant or another body, the body that did it gets 100 points to its energy if a plant was trodden, otherwise it gets the energy of the body that was trodden.

Whenever a body dies, a cross appears on its spot.

# The process of the whole program
At the start of the program, you can see a progress bar going onwards. While the progress bar is going onwards, the [AI](#ai) tries to figure out which species should survive the evolution.
<br>

After the progress bar finishes, you can click the body the species of which you think will survive the evolution.

If you click a circle, then this circle will turn into a triangle, and the bodies of further generations of the species of this body will also be triangles.

If you click a square-shaped body (the body the species of which the AI thinks will survive the evolution), then the shape of this body will become a rhombus and you will not able to adjust the behaviour of the species of this body. Just like with triangles, the further generations of the species of this body will retain the shape of their parents.

To select the right body, you can hover your mouse cursor over the body and see its properties. And, of course, you can rely upon the AI and select the body the species of which the AI thinks will survive the evolution.

To see the vision distance more clearly, in the checkbox beneath "Which body properties to display", you can select "Vision distance" and see the circles around bodies which feature the vision distance.
<br>

Press the triangle-shaped start button to start the evolution.
<br>

When the evolution finishes, you are informed whether it finished with a draw or with a win of one of the species.
<br>

# Controls <a id="controls"></a>
At the bottom part of the window, there can found three buttons and one drop-down list:

* the drop-down list beneath "Which body properties to display": use this drop-down list for selecting which property you want to be displayed near each body on the evolution field
* ? (question mark): calling the window with the guidance
* refresh: refreshing the evolution
* ▷/⏸︎: press ▷ to start/resume the evolution; press ⏸︎ to pause the evolution
<br>

At the right part of the window, there can be found two sections. The first one is "Selected species" and the second one is "Evolution":

* Selected species:

  ![image](https://user-images.githubusercontent.com/95244851/172018546-55176a49-2558-4ffd-bdea-7153da9df96d.png)
  
  _"Selected species" is only active if you have selected one of the species before the evolution._

  * Don't eat plants: that the species you think will survive the evolution must not eat plants
  * Don't eat bodies: the species you think will survive the evolution must not eat bodies
  * Ignore chasers: the species you think will survive the evolution must not flee from the bodies that are chasing them
  * Smart plant chasing: [check out "Smart behaviour"](#smart-behaviour)
  * Smart body chasing: [check out "Smart behaviour"](#smart-behaviour)

* Evolution:

  ![image](https://user-images.githubusercontent.com/95244851/172018578-b5f118f8-0d9d-4533-8463-d0d870171383.png)
  * Scale beneath "Time-lapse": adjusting the extent of time-lapse
  * Hold the evolution start back to select a body: holding the start of the further evolutions back for selecting the species you think will surive the evolution
  * Display averaged properties at the end of evolution: displaying averaged properties of the progenitor of the survived species

# More about properties of bodies <a id="more-properties"></a>
Inborn properties:
* [Food preference](#more-food-preference) (plants or bodies)
* [Speed](#more-speed)
* [Vision distance](#more-vision-distance)
* [Procreation threshold](#more-procreation-threshold)
* [Energy](#more-energy)

For the first generation, the properties are determined either equiprobably or as a deviation from average values. The further generations inherit the properties of their parents with certain deviations.

## Food preference <a id="more-food-preference"></a>
The algorithm of defining what is going to be eaten by a body:\
Plant-eaters try to find plants within their vision distance, but if there are no plants within their vision distance, then they try to find bodies within their vision distance, and the same, but vice versa, for body-eaters. Neither body-eaters nor plant-eaters betray bodies with the same species: if the plant or the body is already being followed by a body with the same species, then this body or plant is qualified as unsuitable.

## Speed <a id="more-speed"></a>
Speed is quite ambiguous: high speed makes bodies lose more energy on moving (the higher speed is, the more energy is spent on moving), but they can reach plants and other bodies faster; while low speed lets bodies lose a low amount of energy on moving, but they might sometimes not cope with escaping from a body which is chasing them or not be able to catch a body themselves.

## Vision distance <a id="more-vision-distance"></a>
Vision distance determines the distance from the body at which it can seek plants and other bodies. The algorithm that the higher value is, the more energy is spent, works for vision distance too.

## Procreation threshold <a id="more-procreation-threshold"></a>
Procreation threshold is the threshold of energy that has to be exceed for the body to procreate. A high procreation threshold might be good because children take a half of the energy of their parent, but a low procreation threshold might be good because the body procreates quite soon.

## Energy <a id="more-energy"></a>
Each time the body moves, the energy is spent for vision distance and speed (the higher value is, the more is spent).
Energy is gained by eating a plant or another body - plant gives 100 points to your energy, and a body gives the whole of its energy.

# Artificial Intelligence <a id="ai"></a>
## Where is the AI used?
AI is used for selecting the species it thinks will survive the evolution. One of the bodies has a shape of a square, and this square-shaped body is the one the AI thinks will have its species survive the evolution.

## How often does the AI predict the survivor species correctly?
The averaged percent from 2000 evolutions is 60% (note that this percent is taken from evolutions in which there was no species selected by the user).

## Is the AI used beyond the the process of selecting the species?
It's not. However, the species selected by the AI occasionally uses the algorithm described in [the "Selected species" section of Controls](#controls).

# Smart chasing <a id="smart-behaviour"></a>
* Smart plant chasing:
  * Bodies calculate if it is profitable to spend a certain amount of energy to get a certain amount of energy from a plant. If the spent energy is less than the energy that can be received, then the body does not attempt to catch that plant
  * if a body from a different species is following that plant, if it can catch that plant sooner, then nothing is done

* Smart body chasing:
  * Bodies calculate if it is profitable to spend a certain amount of energy to get a certain amount of energy from a body. If the spent energy is less than the energy that can be received, then the body does not attempt to catch that body
  * If the body which is meant to be caught will die while it is being caught, then nothing is done
  * If a body from a different species is following that body, if it can catch that body sooner, then nothing is done
