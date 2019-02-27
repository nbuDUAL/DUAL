
##################
# SIMULATION 2_2 #
##################

# DEFINES Simulation 2_2: Recogniton or reation of relation-based concepts among:
# slightly different base episodes and a target similar to one of the bases.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2018.
# Last update: Yolina Petrova, October, 2018

"""
# The goal of the simulation is to demonstrate the ability of the model to create
# role-governed categories through different bases (inirially forming a sparcer concept)
# Then, with the presentation of the second target (similar situation to the first one),
# a new sub-ordinate concept is created:
# 	The grandmother feeds the chicken.     - as base episode
#	The neighbour milks the cow.           - as target episode/base episode 2
#	The grandmother feeds the horse.       - as target episode 2
"""

# Imports agents_manipulation without any previous knowledge.
from agents_manipulation import *


def load_kb_1():
    add_agent("living_thing", agent_type=ConceptAgent)
    add_agent("animal", agent_type=ConceptAgent, superclasses=[find_agent("living_thing")])
    add_agent("mammal", agent_type=ConceptAgent, superclasses=[find_agent("animal")])
    add_agent("bird", agent_type=ConceptAgent, superclasses=[find_agent("animal")])
    add_agent("cow", agent_type=ConceptAgent, superclasses=[find_agent("mammal")])
    add_agent("horse", agent_type=ConceptAgent, superclasses=[find_agent("mammal")])
    add_agent("chicken", agent_type=ConceptAgent, superclasses=[find_agent("bird")])

    add_agent("person", agent_type=ConceptAgent)
    add_agent("female", agent_type=ConceptAgent, superclasses=[find_agent("person")])
    add_agent("male", agent_type=ConceptAgent, superclasses=[find_agent("person")])
    add_agent("grandmother", agent_type=ConceptAgent, superclasses=[find_agent("female")])
    add_agent("neighbour", agent_type=ConceptAgent, superclasses=[find_agent("male")])

    add_agent("carer", agent_type=ConceptAgent)
    add_agent("cared", agent_type=ConceptAgent)
    add_agent("cares", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("carer"), find_agent("cared")])

    add_agent("feeder", agent_type=ConceptAgent, superclasses=[find_agent("carer")])
    add_agent("eater", agent_type=ConceptAgent, superclasses=[find_agent("cared")])
    add_agent("feeds", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("feeder"), find_agent("eater")],
              superclasses=[find_agent("cares")])

    add_agent("milker", agent_type=ConceptAgent, superclasses=[find_agent("carer")])
    add_agent("milked", agent_type=ConceptAgent, superclasses=[find_agent("cared")])
    add_agent("milks", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("milker"), find_agent("milked")],
              superclasses=[find_agent("cares")])

    #BASE EPISODE
    add_agent("grandmother_1", agent_type=InstanceAgent, instance_of=[find_agent("grandmother")])
    add_agent("chicken_1", agent_type=InstanceAgent, instance_of=[find_agent("chicken")])
    add_agent("feeds_1", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("grandmother_1"), find_agent("chicken_1")],
              instance_of=[find_agent("feeds")])

    #TARGET EPISODE 1
    add_agent("neighbour_2", agent_type=InstanceAgent, instance_of=[find_agent("neighbour")])
    add_agent("cow_2", agent_type=InstanceAgent, instance_of=[find_agent("cow")])
    add_agent("milks_2", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("neighbour_2"), find_agent("cow_2")],
              instance_of=[find_agent("milks")])


def load_kb_2():
    #TARGET EPISODE 2
    add_agent("grandmother_3", agent_type= InstanceAgent, instance_of=[find_agent("grandmother")])
    add_agent("horse_3", agent_type=InstanceAgent, instance_of=[find_agent("horse")])
    add_agent("feeds_3", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("grandmother_3"), find_agent("horse_3")],
              instance_of=[find_agent("feeds")])
    
    
# END of file: simulation_2_2_diff_Bases_same_Target.py #

