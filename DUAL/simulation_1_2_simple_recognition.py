
##################
# SIMULATION 1_2 #
##################

# DEFINES Simulation 1.2. Recognition of relation-based concepts.
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



                                                                             ________
      ___________    ________                                               | animal |
     |grandmother|  | feeder |                                            __|________|
     |___________|_ |________|                                           /   |      \
         |         \/___                                             ___/    |      _\______
     ____|_______  /    \_____                                    __/        |     | mammal |
    |grandmother_|/           \__                        ________/_          |     |________|
    |in_the_yard |               \                      | domestic |     ____|_______/    |
    |____________|                \                     |  animal  |    / ___|___         |
         |       \                 \                    |__________|  _/ | bird |         |
          \       \                 \                     /    \     /   |______|         |
          |        \                 \                   |   ___\___/   /                _|___
          |         \                 \                __|__/   _\_____/                | cow |
          |          \                 \              | pig |  |chicken|                |_____|
          |           \                 \             |_____|  |_______|                   |
          _\______     \                 \_                /       \                       |
         | grand  |     \________        __\_____      ___/__      _\_________           __|____
         |mother_1|     | grand  |      | grand  |    | pig_1|    | chicken_1 |         | cow_1 |
         |________|     |mother_2|      |mother_3|    |______|    |___________|         |_______|
            \           |________|      |________|      /           /                    /
             \            \                     \      /        ___/               _____/ 
              \            \                 ____\____/        /                  /
               \            \               /     \           /                  /
                \            \             /       \         /                  / 
                 \            \           /         \       /                  /
                  \            \  _______/           \     /                  /
                   \            \/                    \   /                  /
                    \  _______  /\             ________\_/                  /
                     \/feeds_1\/  \  _______  /         \________  ________/
                      \_______/    \/feeds_2\/                   \/ feeds_3\
                           \        \_______/                     \________/
                            \          /                          _/ 
                             \________/                          /
                              /animal_\                    _____/
                              \ feeds /                   /
                               \_____/                   /
                                   \                    /  
                                    \         _______  /
                                     \_______/ feeds \/
                                             \_______/

                                             
New categories were created in simulation_1_1 (for example "domestic_animal" and "grandmother_in_the_yard").
Let us say that a third situation is evident:
    TARGET situation “The grandmother feeds the cow.”.
        (the relational instance agent "feeds_3" with instance agents "grandmother_3" and "cow_1" as arguments)
Predefined agents in the Long-term-memory are all the agents from simulation_1_1 as well as "cow",
which is a subclass of "mammal".

The relation instances "feeds_3" and "feeds_2"/"feeds_1" are mapped through the marker passing mechanism.
Because both “cow_1” and “chicken_1” are in the same role of the two situations mapping between is created.
The mapping receives additional justification because they are also animals.
Because of the anticipatory mechanism,
after the mapping the already created category “domestic animal” is anticipated as a superclass of the new mapping.
"""


# Imports agents_manipulation without any other previous knowledge.
from agents_manipulation import *


def load_kb_1():
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

def load_kb_2():
    add_agent("cow", agent_type=ConceptAgent, superclasses=[find_agent("mammal")])
    add_agent("grandmother_3", agent_type=InstanceAgent, instance_of=[find_agent("grandmother")])
    add_agent("cow_1", agent_type=InstanceAgent, instance_of=[find_agent("cow")])
    add_agent("feeds_3", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("grandmother_3"), find_agent("cow_1")],
              instance_of=[find_agent("feeds")])

               
# END of KB file: simulation_1_2_simple_recognition.py #
