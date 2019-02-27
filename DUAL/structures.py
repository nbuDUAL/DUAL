
##############
# STRUCTURES #
##############

# DEFINES FUNCTIONS CONSIDERING THE STRUCTURE OF DUAL's KNOWLEDGE.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018

"""

* find_agent_by_structure_in_all_agents (agent_type, structure) -->
Returns list of agents of type AGENT_TYPE that have STRUCTURE.
STRUCTURE should be of type [["instance-of", <concept>], ["part-of", <agent>],...].

* find_agent_by_structure_in_all_requests (request_type, structure) -->
Returns list of requests for agents of type REQUEST_TYPE that have STRUCTURE.
STRUCTURE should be of type [["instance-of", <concept>], ["part-of", <agent>],...].

* find_agent_or_request_by_structure (agent_type, structure) -->
Returns a list of two elements - list of agents and list of requests that share the STRUCTURE.

* get_structure (agent) --> Returns the slots with pointers to agents of the AGENT in the following format
[["instance-of", <concept>], ["part-of", <agent>],...].

* remove_agent (agent) --> Deletes the AGENTS and all traces to it by structure!!!
A generic function that removes the agent from the general registry (variables.all_agents).
All other traces - such as links - are also removed.
After an agent has been removed, it is not accessible via FIND_AGENT or any other function.
The name can be used for the creation of another agent.

* combine_anticipations (anticipation1, anticipation2) --> Compares the structure of ANTICIPATION1 and ANTICIPATION2.
All that is evident in ANTICIPATION2, but missing in ANTICIPATION1 is added to ANTICIPATION1.
In addition, the links to and from ANTICIPATION2 are changed links to and from ANTICIPATION1.
Correspondingly, ANTICIPATION2 is permanently deleted.

"""

from requests import *
import variables

# Finding agents by structure #
###############################


def find_agent_by_structure_in_all_agents(agent_type, structure):
    # Finds agent by STRUCTURE. STRUCTURE should be of type [["instance-of", <concept>], ["part-of", <agent>],...].
    list_of_duplicates = []
    list_of_same_type = []
    for agent in variables.all_agents.values():
        if isinstance(agent, agent_type):
            list_of_same_type = list_of_same_type + [agent]
    for agent in list_of_same_type:
        flag = True
        for pointer in structure:
            slot = pointer[0]
            direction = pointer[1]
            if direction not in get_slot_by_string(agent, slot):
                flag = False
        if flag:
            list_of_duplicates = list_of_duplicates + [agent]
    return list_of_duplicates


def find_agent_by_structure_in_all_requests(request_type, structure):
    # Finds agent by STRUCTURE. STRUCTURE should be of type [["instance-of", <concept>], ["part-of", <agent>],...].
    list_of_duplicates = []
    list_of_same_type = []
    for rec in variables.list_of_all_requests:
        if isinstance(rec, request_type):
            list_of_same_type = list_of_same_type + [rec]
    for rec in list_of_same_type:
        flag = True
        for pointer in structure:
            slot = pointer[0]
            direction = pointer[1]
            if direction not in get_slot_by_string(rec, slot):
                flag = False
        if flag:
            list_of_duplicates = list_of_duplicates + [rec]
    return list_of_duplicates


def find_agent_or_request_by_structure(agent_type, structure):
    # Returns a list of two elements - list of agents and list of requests that share the STRUCTURE.
    return find_agent_by_structure_in_all_agents(agent_type, structure), find_agent_by_structure_in_all_requests(
        request_type_from_agent_type(agent_type), structure)


def get_structure(new_agent):
    structure = []
    try:
        for sup in new_agent.superclasses:
            structure = structure + [["superclasses", sup]]
    except AttributeError:
        pass
            
    try:
        for sub in new_agent.subclasses:
            structure = structure + [["subclasses", sub]]
    except AttributeError:
        pass

    try:
        for inst in new_agent.instances:
            structure = structure + [["instances", inst]]
    except AttributeError:
        pass

    try:
        for inst_of in new_agent.instance_of:
            structure = structure + [["instance_of", inst_of]]         
    except AttributeError:
        pass

    try:
        for h_parts in new_agent.has_parts:
            structure = structure + [["has_parts", h_parts]]
    except AttributeError:
        pass

    try:
        for part_o in new_agent.part_of:
            structure = structure + [["part_of", part_o]]
    except AttributeError:
        pass

    try:
        for sit in new_agent.situations:
            structure = structure + [["situations", sit]]
    except AttributeError:
        pass

    try:
        for arg in new_agent.arguments:
            structure = structure + [["arguments", arg]]     
    except AttributeError:
        pass

    try:
        for arg_of in new_agent.argument_of:
            structure = structure + [["argument_of", arg_of]]     
    except AttributeError:
        pass

    try:
        for target in new_agent.target_instance:
            structure = structure + [["target_instance", target]]
    except AttributeError:
        pass

    try:
        for base in new_agent.base_instance:
            structure = structure + [["base_instance", base]]
    except AttributeError:
        pass

    try:
        for base in new_agent.justifications:
            structure = structure + [["justifications", base]]
    except AttributeError:
        pass
    return structure


def remove_agent(killing):
    # Brutal deletion of the agent KILLING by structure!!!
    for agent in variables.all_agents.values():
        links_for_delete = []                                 
        for link in agent.incoming_links:                  
            if link.sender == killing:                                          
                links_for_delete = link
        if links_for_delete:
            remove_link(links_for_delete, agent)
        if killing in agent.agents_to_activate:
            agent.agents_to_activate.remove(killing)
        for structure in get_structure(agent):
            if killing == structure[1]:
                get_slot_by_string(agent, structure[0]).remove(killing)
    if isinstance(killing, MappingAgent):
        killing.target_instance[0].mappings = [
            x for x in killing.target_instance[0].mappings if x != killing]
        killing.base_instance[0].mappings = [
            x for x in killing.base_instance[0].mappings if x != killing]
        
        for a in variables.list_of_anticipations:
            if killing in a.justifications:
                for l in a.incoming_links:
                    if l.sender == killing:
                        links_for_delete = l
                        if links_for_delete:
                            remove_link(links_for_delete, a)
                    
    if killing in variables.all_agents.values():
        variables.all_agents.pop(killing.name)
    if killing in variables.agents_not_in_STM:
        variables.agents_not_in_STM.remove(killing)
    if killing in variables.working_memory:
        variables.working_memory.remove(killing)
    if killing in variables.target_agents:
        variables.target_agents.remove(killing)
    if killing in variables.input_list.keys():
        variables.input_list.pop(killing.name)
    if killing in variables.goal_list.keys():
        variables.input_list.pop(killing.name)
    if killing in variables.list_of_mappings:
        variables.list_of_mappings.remove(killing)
    if killing in variables.list_of_anticipations:
        variables.list_of_anticipations.remove(killing)
    if killing in variables.short_term_memory:
        variables.short_term_memory.remove(killing)
    del killing
    
# Combining anticipations #
###########################


def combine_anticipations(anticipation1, anticipation2):
    for structure in get_structure(anticipation2):
        slot = structure[0]
        direction = structure[1]
        link_weight = 0.00
        for link in anticipation2.incoming_links:
            if link.sender == direction:
                link_weight = link.weight
        link_weight_to_direction = 0.00
        for link in direction.incoming_links:
            if link.sender == anticipation2:
                link_weight_to_direction = link.weight
        if direction not in get_slot_by_string(anticipation1, slot):
            # Change ANTICIPATION2 with ANTICIPATION1 in all neighbours.
            get_slot_by_string(anticipation1, slot).append(direction)
            if isinstance(direction, MappingAgent):
                if anticipation2 in direction.target_instance:
                    direction.target_instance = [anticipation1]
                elif anticipation2 in direction.base_instance:
                    direction.base_instance = [anticipation1]
                else:
                    print("In COMBINE_ANTICIPATIONS: Something very wrong!!")
            else:
                get_slot_by_string(direction, get_opposite_slot(slot)).remove(anticipation2)
                get_slot_by_string(direction, get_opposite_slot(slot)).append(anticipation1)
            # Changes the Links from Direction to ANTICIPATION2 with links to ANTICIPATION1.
            create_link(direction, anticipation1, link_weight)
        create_link(anticipation1, direction, link_weight_to_direction)
    remove_agent(anticipation2)


# END OF FILE STRUCTURES.PY #
