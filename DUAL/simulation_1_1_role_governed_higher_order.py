
####################
# SIMULATION 1_1_1 #
####################

# DEFINES Simulation 1.1.1 Creation of a relation-based concepts
# through episodes with higher-order relations.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018

# Imports the whole DUAL architecture/model (without any previous knowledge).
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
    add_agent("meat", agent_type=ConceptAgent)
    add_agent("eggs", agent_type=ConceptAgent)

    add_agent("carer", agent_type=ConceptAgent)
    add_agent("the_cared", agent_type=ConceptAgent)
    add_agent("cares", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("carer"), find_agent("the_cared")])

    add_agent("feeder", agent_type=ConceptAgent, superclasses=[find_agent("carer")])
    add_agent("eater", agent_type=ConceptAgent, superclasses=[find_agent("the_cared")])
    add_agent("feeds", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("feeder"), find_agent("eater")], superclasses=[find_agent("cares")])

    add_agent("giver", agent_type=ConceptAgent)
    add_agent("given", agent_type=ConceptAgent)
    add_agent("gives", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("giver"), find_agent("given")])

    # Causal relaition
    add_agent("reason", agent_type=ConceptAgent)
    add_agent("consequence", agent_type=ConceptAgent)
    add_agent("causes", agent_type=RelationConceptAgent, arity=2,
              arguments=[find_agent("reason"), find_agent("consequence")])

    # BASE
    add_agent("meat_1", agent_type=InstanceAgent, instance_of=[find_agent("meat")])
    add_agent("grandmother_1", agent_type=InstanceAgent, instance_of=[find_agent("grandmother")])
    add_agent("pig_1", agent_type=InstanceAgent, instance_of=[find_agent("pig")])
    add_agent("feeds_1", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("grandmother_1"), find_agent("pig_1")],
              instance_of=[find_agent("feeds")])
    add_agent("gives_1", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("pig_1"), find_agent("meat_1")],
              instance_of=[find_agent("gives")])

    add_agent("causes_1", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("feeds_1"), find_agent("gives_1")],
              instance_of=[find_agent("causes")])

    # TARGET
    add_agent("eggs_2", agent_type=InstanceAgent, instance_of=[find_agent("eggs")])
    add_agent("grandmother_2", agent_type=InstanceAgent, instance_of=[find_agent("grandmother")])
    add_agent("chicken_2", agent_type=InstanceAgent, instance_of=[find_agent("chicken")])
    add_agent("feeds_2", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("grandmother_2"), find_agent("chicken_2")],
              instance_of= [find_agent("feeds")])
    add_agent("gives_2", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("chicken_2"), find_agent("eggs_2")],
              instance_of=[find_agent("gives")])

    add_agent("causes_2", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("feeds_2"), find_agent("gives_2")],
              instance_of=[find_agent("causes")])
    

def load_kb_2():
    add_agent("cow", agent_type=ConceptAgent, superclasses=[find_agent("mammal")])
    add_agent("milk", agent_type=ConceptAgent)
    # TARGET
    add_agent("milk_3", agent_type=InstanceAgent, instance_of=[find_agent("milk")])
    add_agent("grandmother_3", agent_type=InstanceAgent, instance_of=[find_agent("grandmother")])
    add_agent("cow_3", agent_type=InstanceAgent, instance_of=[find_agent("cow")])
    add_agent("feeds_3", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("grandmother_3"), find_agent("cow_3")],
              instance_of=[find_agent("feeds")])
    add_agent("gives_3", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("cow_3"), find_agent("milk_3")],
              instance_of=[find_agent("gives")])
    add_agent("causes_3", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("feeds_3"), find_agent("gives_3")],
              instance_of=[find_agent("causes")])


# END of file: simulation_1_1_role_governed_higher_order.py #
