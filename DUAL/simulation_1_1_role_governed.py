
##################
# SIMULATION 1_1 #
##################

# DEFINES Simulation 1.1. Creation of a relation-based concepts.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018

"""
                                                                 ______________
                                _______                         | living_thing |
                               / cares \                        |______________|         
                              /\_______/\                              |    
     ________         _______/     |     \___________             _____|_____         
    | person |       | carer |     |     | the_cared |           |  animal   |  
    |________|       |_______|  ___|___  |___________|           |___________|             
     ___|____                  / feeds \                          /          \ 
    | female |                /\_______/\                        /            \
    |________|       ________/    / \    \_______        _______/__         ___\__
         |          | feeder |   /   \   | eater |      |  mammal  |       | bird |
     ____|______    |________|  /     \  |_______|      |__________|       |______|                
    |grandmother|              / ______\________________/                 /
    |___________|    _______  / | pig | \  _______             _________ /
         |       \  /feeds_1\/  |_____|  \/feeds_2\           | chicken |  
          \       \/\_______/\     /      \_______/           |_________| 
          _\______/ \_       _\___/       /       \           /
         | grand  |   \     |pig_1|   ___/____    _\_________/
         |mother_1|    \__  |_____|  | grand  |  | chicken_1 |
         |________|       \_________ |mother_2|  |___________|
                                    \|________|

This simulation aims to demonstrate that when presented with two similar situations:
"A grandmother feeding a pig" and "A neighbour feeding a chicken",
the model can indeed create relation-based concepts.

For this simulation – initially we have relational concepts for "cares" and “feeds”.
Both have concept arguments  "carer", "the_cared" and "feeder", "eater" respectively.
There are also concepts for “grandmother” with its superclass "female" and the female's superclass "person".
Predefined concepts are also:
    “pig” with its superclass "mammal", the mammal's superclass "animal" and the animal's superclass "living_thing"
    “chicken” with its superclass "bird" (which is also a subclass of "animal").
Defined are also:
    BASE situation: “The grandmother feeds the pig.”
        (the relational instance agent "feeds_1" with instance agents "grandmother_1" and "pig_1" as arguments)
    TARGET situation “The grandmother feeds the chicken.”.
        (the relational instance agent "feeds_2" with instance agents "grandmother_2" and "chicken_2" as arguments)

When two relations are mapped (like “feeds_1” and “feeds_2”),
through structure correspondence mechanism their arguments/roles should be/are also mapped:
(“chicken_2” and “pig_1”; “grandmother_1” and “grandmother_2”).
The mapping between “chicken_1” and “pig_1” becomes a new concept.
It may receive a user defined name – for example “domestic animal”.

Because of the marker passing mechanism (the mechanisms searching for semantic similarity):
there will be an additional pressure to map:
    “chicken_2” and “pig_1” (because they are both animals)
    “grandmother_1” and “grandmother_2” (they are both instances of "grandmother").
    
The mappings between “feeds_1” and “feeds_2” and between “grandmother_1” and “grandmother_2” are:
    variant 1) not expected to become new concepts,
        because they are already direct instances of the already existing concepts “feeds” and “grandmother”.
    variant 2) become new concepts, which can receive a name by the user.
        For example, when the mapping between "grandmother_1" and "grandmother_2" becomes a concept,
        it may receive the user defined name "grandmother_in_the_yard".
        Respectively, when the mapping between "feeds_1" and "feeds_2" becomes a concept,
        it may receive the user defined name "animal_feeding".
"""

# Imports the whole DUAL architecture/model (without any previous knowledge).
from agents_manipulation import *


def load_kb():
    add_agent("living_thing", agent_type=ConceptAgent)
    add_agent("animal", agent_type=ConceptAgent, superclasses=[find_agent("living_thing")])
    add_agent("mammal", agent_type=ConceptAgent, superclasses=[find_agent("animal")])
    add_agent("bird", agent_type=ConceptAgent, superclasses=[find_agent("animal")])
    add_agent("pig", agent_type=ConceptAgent, superclasses=[find_agent("mammal")])
    add_agent("chicken", agent_type=ConceptAgent, superclasses=[find_agent("bird")])

    add_agent("person", agent_type=ConceptAgent)
    add_agent("female", agent_type=ConceptAgent, superclasses=[find_agent("person")])
    add_agent("grandmother", agent_type=ConceptAgent, superclasses=[find_agent("female")])

    add_agent("carer", agent_type=ConceptAgent)
    add_agent("the_cared", agent_type=ConceptAgent)
    add_agent("cares", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("carer"), find_agent("the_cared")])

    add_agent("feeder", agent_type=ConceptAgent, superclasses=[find_agent("carer")])
    add_agent("eater", agent_type=ConceptAgent, superclasses=[find_agent("the_cared")])
    add_agent("feeds", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("feeder"), find_agent("eater")], superclasses=[find_agent("cares")])

    # BASE
    add_agent("grandmother_1", agent_type=InstanceAgent, instance_of=[find_agent("grandmother")])
    add_agent("pig_1", agent_type=InstanceAgent, instance_of=[find_agent("pig")])
    add_agent("feeds_1", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("grandmother_1"), find_agent("pig_1")],
              instance_of=[find_agent("feeds")])

    # TARGET
    add_agent("grandmother_2", agent_type=InstanceAgent, instance_of=[find_agent("grandmother")])
    add_agent("chicken_2", agent_type=InstanceAgent, instance_of=[find_agent("chicken")])
    add_agent("feeds_2", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("grandmother_2"), find_agent("chicken_2")],
              instance_of=[find_agent("feeds")])

# END of KB file: simulation_1_1.py #
