
from main_cycle import *

add_agent("sit_baba_1", agent_type=ConceptAgent, word="nqkva baba")
add_agent("sit_baba_1_1", agent_type=InstanceAgent,
          instance_of=[find_agent("sit_baba_1")])
add_agent("sit_baba_1_2", agent_type=InstanceAgent,
          instance_of=[find_agent("sit_baba_1")])
# add_agent("papa", agent_type=ConceptAgent)
# a = add_agent("az", agent_type=ConceptAgent, superclasses=[find_agent("mama"), find_agent("dada")])
# 
# add_agent("az", agent_type=ConceptAgent, superclasses=[find_agent("mama"), find_agent("dada")])
# add_agent("az_1", agent_type=InstanceAgent, instance_of=[find_agent("az")])



add_agent("girl", agent_type=ConceptAgent)
add_agent("mama", agent_type=ConceptAgent, superclasses=[find_agent("girl")])
add_agent("baba", agent_type=ConceptAgent, superclasses=[find_agent("girl")])
add_agent("boy", agent_type=ConceptAgent)
add_agent("dada", agent_type=ConceptAgent, superclasses=[find_agent("boy")])
add_agent("papa", agent_type=ConceptAgent, superclasses=[find_agent("boy")])

add_agent("lover", agent_type=ConceptAgent)
add_agent("loved", agent_type=ConceptAgent)
add_agent("loves", agent_type=RelationConceptAgent,
          arguments=[find_agent("lover"), find_agent("loved")])
add_agent("lover_boy", agent_type=ConceptAgent, superclasses=[find_agent("lover"), find_agent("boy")])
add_agent("loved_girl", agent_type=ConceptAgent, superclasses=[find_agent("loved"), find_agent("girl")])
add_agent("human_love", agent_type=RelationConceptAgent, superclasses=[find_agent("loves")],
          arguments=[find_agent("lover_boy"), find_agent("loved_girl")])

add_agent("love_schema", agent_type=ConceptAgent, has_parts=[find_agent("lover_boy"),
                                                             find_agent("loved_girl"),
                                                             find_agent("human_love")])

add_agent("mama_1", agent_type=InstanceAgent, instance_of=[find_agent("loved_girl")])
add_agent("dada_1", agent_type=InstanceAgent, instance_of=[find_agent("lover_boy")])
add_agent("loves_1", agent_type=RelationInstanceAgent, instance_of=[find_agent("human_love")],
          arguments=[find_agent("mama_1"), find_agent("dada_1")])

add_agent("sit_human_love_1", agent_type=InstanceAgent, instance_of=[find_agent("love_schema")],
          has_parts=[find_agent("mama_1"), find_agent("dada_1"), find_agent("loves_1")])

add_agent("baba_2", agent_type=InstanceAgent, instance_of=[find_agent("loved_girl")])
add_agent("papa_2", agent_type=InstanceAgent, instance_of=[find_agent("lover_boy")])
add_agent("loves_2", agent_type=RelationInstanceAgent, instance_of=[find_agent("human_love")], 
          arguments=[find_agent("baba_2"), find_agent("papa_2")])

add_agent("sit_human_love_2", agent_type=InstanceAgent, instance_of=[find_agent("love_schema")],
          has_parts=[find_agent("baba_2"), find_agent("papa_2"), find_agent("loves_2")])

# TARGET
add_agent("teen_boy", agent_type=ConceptAgent, superclasses=[find_agent("boy")])
add_agent("teen_girl", agent_type=ConceptAgent, superclasses=[find_agent("girl")])
add_agent("john_3", agent_type=InstanceAgent, instance_of=[find_agent("teen_boy")])
add_agent("marry_3", agent_type=InstanceAgent, instance_of=[find_agent("teen_girl")])
add_agent("loves_3", agent_type=RelationInstanceAgent, instance_of=[find_agent("loves")],
          arguments=[find_agent("john_3"), find_agent("marry_3")])


