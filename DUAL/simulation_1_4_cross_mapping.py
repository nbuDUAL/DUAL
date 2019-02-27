
################################
# Simulation_1_4_cross-mapping #
################################

# DEFINES Simulation 1.4. a cross-mapping case.
# PROGRAMERS: Yolina Petrova, YEAR 2018
# Last updated: Yolina Petrova, October, 2018

"""
This simulation aims to demonstrate that when presented with cross-mapping situations:
"The triangle is to the left of the square" and "The square is to the left of the triangle",
the model prefers the relational mappings (as people do).

For this simulation – initially we have the relational concept “left_of”.
with concept arguments  "left_object" and "right_object".
There are also concepts for “square” and "triangle".
Predefined are also:
    BASE situation: “The square is to the left of the triangle.”
        (the relational instance agent "left_of_1" with instance agents "square_1" and "triangle_1" as arguments)
    TARGET situation “The triangle is to the left of the square.”.
        (the relational instance agent "left_of_2" with instance agents "square_2" and "triangle_2" as arguments)

When two relations are mapped (like “left_of_1” and “left_of_2”),
through structure correspondence mechanism their arguments/roles should be/are also mapped:
(“square_1” and “triangle_1”; “triangle_2” and “square_2”).

Because of the marker passing mechanism (the mechanisms searching for semantic similarity):
there will be an additional pressure to map:
    “square_1” and “square_2” (because they are squares)
    “triangle_1” and “triangle_2” (they are both instances of the concept "triangle").
"""

from agents_manipulation import *


def load_kb():
    add_agent("square", agent_type=ConceptAgent)
    add_agent("triangle", agent_type=ConceptAgent)

    add_agent("left_object", agent_type=ConceptAgent)
    add_agent("right_object", agent_type=ConceptAgent)
    add_agent("left_of", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("left_object"), find_agent("right_object")])

    # BASE
    add_agent("square_1", agent_type=InstanceAgent, instance_of=[find_agent("square")])
    add_agent("triangle_1", agent_type=InstanceAgent, instance_of=[find_agent("triangle")])
    add_agent("left_of_1", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("square_1"), find_agent("triangle_1")],
              instance_of=[find_agent("left_of")])

    # TARGET EPISODE
    add_agent("triangle_2", agent_type=InstanceAgent, instance_of=[find_agent("triangle")])
    add_agent("square_2", agent_type=InstanceAgent, instance_of=[find_agent("square")])
    add_agent("left_of_2", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("triangle_2"), find_agent("square_2")],
              instance_of=[find_agent("left_of")])

# END of KB file: simulation_1_4.py #
