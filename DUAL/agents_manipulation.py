
#######################
# AGENTS MANIPULATION #
#######################

# DEFINES VARIOUS FUNCTIONS FOR MANIPULATION OF THE DUAL AGENTS.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last update: Yolina Petrova, December, 2018


# TO DO: Fix the function for creating agent from console.
# TO DO: def update_threshold (agent, function = parameters.new_threshold ())
# ??? When the agent is frequently activated, its threshold is updated with a higher value.

"""
# Generating unique names  #
############################
Each agent has an unique name which means that two different agents cannot have the same name.
The name of each agent is assigned to the agent at the moment of its creation.

* check_for_free_name(string) --> Returns True if no agent with name STRING or False otherwise.

* ask_for_a_name(string) --> The function asks the user for a name until he or she gives one which is free.

* gen_name_sit(focus_name) --> Returns string which is not a name of another agent. The string is based on FOCUS_NAME.
The just created situations will take this name.

* gen_name_sit_from_zero(focus_name) --> Returns string which is not a name of another agent starting with 0.
The string is based on FOCUS_NAME. The just created situations will take this name.
        
* gen_name_instance(concept_name) --> Returns string which is not a name of any agent.
The string is based on CONCEPT_NAME.
The just created instances will take this name.

* gen_name_mapping(target_name, base_name) --> Returns string which is not a name of any agent.
The string is based on TARGET_NAME and BASE_NAME.
The just created mappings will take this name.

* gen_name_anticipation(base_name) --> Returns string which is not a name of any agent. The string is based on BASE_NAME.
The just created anticipation will take this name.

* name_in_requests(name) --> Returns TRUE if there is a request with the same name.

# Manipulate agents  #
######################

* describe_req(request) --> Prints the values of all slots of REQUEST.

# Manipulate agents  #
######################

* describe_agent(agent) --> Prints the values of all slots of AGENT.
        
* get_agent(name) --> Returns the agent with the respective NAME or False if there is no agent with the given NAME.

* agent_check(agent) --> Returns True if AGENT is an agent, or False otherwise.
        
* find_agent(agent) --> Returns AGENT both by Agent and by Agent Name.
If such an agent does not exist, the function raises a dual error.

* get_slot_by_string(agent, string) --> Returns the slot of AGENT that has the name STRING.

* get_opposite_slot(slot_name) --> Returns the "opposite" slot name, i.e "instance-of" --> "instances", etc.

* remove_instances(list) --> Returns a list, containing only the Semantic Agents which were in LIST.

* add_agent_in_slot(holder_agent, slot_label, filler) --> The function just adds the agent FILLER into the slot
SLOT_LABEL of agent HOLDER_AGENT.

* add_in_slot(holder_agent, slot_label, filler)
--> In addition to adding FILLET in SLOT_LABEL of HOLDER_AGENT, the function creates the appropriate links.

* get_weight_from_label(string) --> By giving a slot label as STRING,
the function returns the pre-defined weight of the connections that usually those slots hold.

* remove_agent_from_slot(holder_agent, slot_label, filler)
--> The function just removes agent FILLER from the slot SLOT_LABEL of agent HOLDER_AGENT.

* remove_from_slot(holder_agent, slot_label, filler)
--> In addition to removing FILLET in SLOT_LABEL of HOLDER_AGENT, the function destroys the appropriate links.

* check_and_exchange_superclasses(mapping, concept)
--> Checks whether CONCEPT is above or bellow MAPPING through the hierarchy and adds slots if necessary.

# Collecting information #
##########################

* collect_subclasses_in_stm(agent) --> Collects the direct subclasses of AGENT.

* collect_all_active_subclasses(agent) --> Collects all active subclasses of AGENT.

* collect_subclasses_including_itself(agent) --> The function returns the result form
collect_all_active_subclasses(agent) as a list including AGENT.

* collect_superclasses_in_stm(agent) --> Collects the active DIRECT superclasses of AGENT.

* collect_all_active_superclasses(agent) --> Collects all active superclasses of AGENT.

* collect_instance_of_in_stm(agent) --> Collects the active DIRECT concept of the InstanceAgent AGENT.

* get_instances_of_concept(concepts) --> Collects the active DIRECT instances of the ConceptsAgent AGENT.

* get_all_instances_of_concept(concepts) --> Collects the active instances (not only the direct ones) of the CONCEPTS.
NOTE: CONCEPTS should be a list!

* collect_agents_from_slot(agent, slot)
--> The function returns a list of all agents taking place into the slot.
If AGENT does not contain SLOT, the function returns an empty list.

* collect_agents_and_weights(agent, slot)
--> The function returns a list of dictionaries.
Each dictionary contains an agent which receives a link from AGENT (as key) and the weight of that link (as value).
SLOT refers to which agent-weight pairs should be extracted.
If there are no links or the SLOT is not valid, an empty list is returned.

# Functions checking if there are paths up and down #
#####################################################

* find_all_above_intersections(agent1, agent2)
--> The function returns all active intersections between the superclasses of AGENT1 and AGENT2 (not only the first one).
Works both with concepts and with instances.

* search_path_above(sub, superc)
--> Checks whether there is a path above through the superclass hierarchy from SUB to SUPER. Returns BOOLEAN.
SUB could be an instance; SUPERC should be a concept!

* give_the_first_intersection_only(list_of_concepts):
--> Removes the agents from LIST_OF_CONCEPTS that are superclasses of other agents from the same list.

* marker_passing(agent1, agent2) --> Gives the first intersection between AGENT1 and AGENT2.

* check_mapping(agent1, agent2) --> If there is a mapping between AGENT1 and AGENT2, the function returns if.
If there is no mapping between AGENT1 and AGENT2, the function returns False.

# Functions for creating agents through various sources #
#########################################################

* integrity_agent(name, agents_to_activate, incoming_links, threshold, level_of_activation,
                  speed_of_change, part_of, has_parts, argument_of, superclasses, subclasses,
                  instances, arity, arguments, target_instance, base_instance, justifications,
                  inhibitions, situations, instance_of, mappings)
--> Checks the integrity of the agent - more specifically, if the given values fulfill the slots' requirements.
If any of the requirements is violated, it  signals an error depending on the violated requirement.

* add_agent(name, agent_type = DualAgent, comment = "", threshold = parameters.threshold_agent_activation,
            level_of_activation = parameters.initial_agent_activation,
            speed_of_change = parameters.default_speed_of_change,
            agents_to_activate = [], incoming_links = [], has_parts = [], part_of = [], instances = [], instance_of = [],
            target_instance = [], base_instance = [], situations = [], superclasses = [], subclasses = [],
            arity = 0, arguments = [], mappings = [], argument_of = [], justifications = []) -->
Creates a new agent with the specified arguments. NAME and AGENT_TYPE are the only arguments that are a must.
NAME must be string. If NAME is already in use, integrity_agent(...) signals an error.
AGENT_TYPE must satisfy a valid type of agent from the 7 types that can be usually created.
All arguments that are provided (including the given name) are passed to integrity_agent(...) for verification.
If all requirements are satisfied, a new agent is created and it is added into the global variable variables.all_agents;
it is integrated to the other knowledge with links according to the specification.
In addition, the new agent is added to the global variable variables.agents_not_in_STM.

* add_agent_from_console() --> Should be upgraded.
Basically, should call add_agent with the same arguments but one by one from the console.

* create_agent_by_str_agent_type(agent) --> The function creates an AGENT through an information given in a file,
which does not need pre-processing. For that purpose, it uses the agent_type information gives as string.

* adjust_links_and_weights(agent) --> After AGENT is created through load_kb_from_file(file_name),
this function deals with the connections of the agents that activate AGENT and the agents that are activated by AGENT.

* class Str2(str) --> The class turns strings with single quotes into strings with double quotes.
Allows str.__repr__() to do the hard work of how a string would be represented.
Then, the outer two characters, single quotes, and replace them with double quotes.
This is explicitly needed when working with json data format.

* save_kb_to_file(file_name) --> The function saves the current KB to a file with name FILE_NAME,
so it could be exactly reproduced in any time. The function MUST be run before any cycles.
FILE_NAME should be a string ending with '.csv'.

* load_kb_from_file(file_name) --> The function that loads a KB from a file with name FILE_NAME.
FILE_NAME should be a string ending with '.csv'.
"""

from links import *
import variables

# Pandas and json are needed when working with csv files.
import pandas
import json
    

# Generating unique names  #
############################


def check_for_free_name(string):
    if string in variables.all_agents.keys():
        return False
    else:
        return True


def ask_for_a_name(string):
    name = input("What is this called: '{}'? ".format(string))
    while True:
        if check_for_free_name(name):
            break
        else:
            print("There is an agent with the same name already.")
            name = input("Can you give me another name for '{}', please: ".format(string))
    return name
    
# The gen_name functions bellow may be used to generate names for various types of agents.
# The names are guaranteed to be 'safe' (meaning that there are no other agents with the same name).


def gen_name_sit(concept_name):
    # It could also be FOCUS_NAME
    # (i.e. the situation is created bottom-up, which is not implemented yet).
    i = 1
    if "sit" in concept_name:
        affix = ""
    else:
        affix = "sit_"
    new_name = "{}{}_{}".format(affix, concept_name, i)
    while get_agent(new_name):
        i += 1
        new_name = "{}{}_{}".format(affix, concept_name, i)
    return new_name


def gen_name_sit_from_zero(focus_name):
    i = 1
    new_name = "sit_" + focus_name
    while get_agent(new_name):
        new_name = new_name + "_" + str(i)
        i += 1
    return new_name


def gen_name_instance(concept_name):
    i = 1
    new_name = "inst_" + concept_name + "_"
    while get_agent(new_name + str(i)):
        i += 1
    return new_name + str(i)    


def gen_name_mapping(target_name, base_name):
    i = 1
    new_name = "abst_" + target_name + "_" + base_name + "_"
    while (get_agent(new_name + str(i))) or (name_in_requests(new_name + str(i))):
        i += 1
    return new_name + str(i)


def gen_name_anticipation(base_name):
    i = 1
    new_name = "anticip_" + base_name + "_"
    while (get_agent(new_name + str(i))) or (name_in_requests(new_name + str(i))):
        i += 1
    return new_name + str(i)


def name_in_requests(name):
    # Returns TRUE if there is a request with the same name.
    flag = False
    for r in variables.list_of_all_requests:
        if r.name == name:
            flag = True
    return flag


# Manipulate requests  #
########################


def describe_req(request):
    if isinstance(request, Request):
        request.describe_itself()
    else:
        dual_raise("describe_req",
                   "The request: '{}' does not exist.".format(request))


# Manipulate agents  #
######################


def describe_agent(ag):
    agent = find_agent(ag)
    agent.describe_itself()
        

def get_agent(name):
    # If there is an agent with the name NAME (which is a string), the function returns it.
    l = variables.all_agents.get(name)
    if l:
        return l
    else:
        return False


def agent_check(agent):
    # The function checks if AGENT is an agent/whether it is in variables.all_agents.
    if agent in variables.all_agents.values():
        return True
    else:
        return False


def find_agent(agent):
    # Returns AGENT both by Agent and by Agent Name.
    if isinstance(agent, DualAgent):
        return agent
    elif get_agent(agent):
        return get_agent(agent)
    else:
        dual_raise("find_agent",
                   "The agent: '{}' does not exist.".format(agent))


def get_slot_by_string(agent, string):
    if string == "agents_to_activate":
        return agent.agents_to_activate
    if string == "instance_of":
        return agent.instance_of
    elif string == "instances":
        return agent.instances
    elif string == "part_of":
        return agent.part_of
    elif string == "has_parts":
        return agent.has_parts
    elif string == "subclasses":
        return agent.subclasses
    elif string == "superclasses":
        return agent.superclasses
    elif string == "justifications":
        return agent.justifications
    elif string == "inhibitions":
        return agent.inhibitions
    elif string == "mappings":
        return agent.mappings
    elif string == "arguments":
        return agent.arguments
    elif string == "argument_of":
        return agent.argument_of
    elif string == "situations":
        return agent.situations
    elif string == "target_instance":
        return agent.target_instance
    elif string == "base_instance":
        return agent.base_instance
    else:
        dual_raise("Get_slot_by_string: ",
                   "Unrecognized slot name: {}.".format(string))


def get_opposite_slot(slot):
    if slot == "instance_of":
        return "instances"
    elif slot == "instances":
        return "instance_of"
    elif slot == "superclasses":
        return "subclasses"
    elif slot == "subclasses":
        return "superclasses"
    elif slot == "has_parts":
        return "part_of"
    elif slot == "part_of":
        return "has_parts"
    elif slot == "arguments":
        return "argument_of"
    elif slot == "argument_of":
        return "arguments"
    elif slot == "justifications":
        return "justifications"
    elif slot == "inhibitions":
        return "inhibitions"
    else:
        dual_raise("Get_opposite_slot: ",
                   "Unrecognized slot name: {}.".format(slot))


def remove_instances(l):
    # Removes all EpisodicAgents from L.
    l1 = []
    for a in l:
        if isinstance(a, SemanticAgent):
            l1 = l1 + [a]
    return l1


def add_agent_in_slot(holder_agent, slot_label, filler):
    # Support procedure for add_in_slot().
    # Adds agent FILLER into the slot SLOT_LABEL of agent HOLDER_AGENT.
    if slot_label == "instance_of":
        holder_agent.instance_of = holder_agent.instance_of + [filler]
    elif slot_label == "instances":
        holder_agent.instances = holder_agent.instances + [filler]
    elif slot_label == "superclasses":
        holder_agent.superclasses = holder_agent.superclasses + [filler]
    elif slot_label == "subclasses":
        holder_agent.subclasses = holder_agent.subclasses + [filler]
    elif slot_label == "has_parts":
        holder_agent.has_parts = holder_agent.has_parts + [filler]
    elif slot_label == "part_of":
        holder_agent.part_of = holder_agent.part_of + [filler]
    elif slot_label == "arguments":
        holder_agent.arguments = holder_agent.arguments + [filler]
    elif slot_label == "argument_of":
        holder_agent.argument_of = holder_agent.argument_of + [filler]
    elif slot_label == "justifications":
        holder_agent.justifications = holder_agent.justifications + [filler]
    elif slot_label == "inhibitions":
        holder_agent.inhibitions = holder_agent.inhibitions + [filler]
    else:
        dual_raise("add_agent_in_slot: ",
                   "Unrecognized slot name: {}.".format(slot_label)) 


def add_in_slot(holder_agent, slot_label, filler):
    # In addition to adding FILLET in SLOT_LABEL of HOLDER_AGENT, the function creates the appropriate links.
    holder = find_agent(holder_agent)
    new_agent = find_agent(filler)
    holder_slot = get_slot_by_string(holder, slot_label)
    if new_agent not in holder_slot:
        add_agent_in_slot(holder, slot_label, new_agent)
        add_agent_in_slot(new_agent, get_opposite_slot(slot_label), holder)
        create_link(new_agent, holder, get_weight_from_label(slot_label))
        create_link(holder, new_agent, get_weight_from_label(get_opposite_slot(slot_label)))


def get_weight_from_label(string):
    # By giving a slot label as STRING,
    # the function returns the pre-defined weight of the connections that usually those slots hold.
    if string == "instance_of":
        return default_instance_of_weight
    elif string == "instances":
        return default_class_instance_weight
    elif string == "part_of":
        return default_part_of_weight
    elif string == "has_parts":
        return default_has_part_weight
    elif string == "subclasses":
        return default_class_subclass_weight
    elif string == "superclasses":
        return default_is_a_weight
    elif string == "justifications":
        return default_justification_weight
    elif string == "inhibitions":
        return default_inhibitory_weight
    elif string == "mappings":
        return default_mapping_to_mapping_support_weight
    elif string == "arguments":
        return default_argument_predicate_weight
    elif string == "argument_of":
        return default_predicate_argument_weight
    elif string == "situations":
        return part_of_group_weight
    else:
        dual_raise("get_weight_from_label: ",
                   "Unrecognized slot name: {}.".format(string))


def remove_agent_from_slot(holder_agent, slot_label, filler):
    # Support procedure for remove_from_slot().
    # Removes agent FILLER from the slot SLOT_LABEL of agent HOLDER_AGENT.
    if slot_label == "instance_of":
        holder_agent.instance_of = [x for x in holder_agent.instance_of if x != filler]
    elif slot_label == "instances":
        holder_agent.instances = [x for x in holder_agent.instances if x != filler]
    elif slot_label == "superclasses":
        holder_agent.superclasses = [x for x in holder_agent.superclasses if x != filler]
    elif slot_label == "subclasses":
        holder_agent.subclasses = [x for x in holder_agent.subclasses if x != filler]
    elif slot_label == "has_parts":
        holder_agent.has_parts = [x for x in holder_agent.has_parts if x != filler]
    elif slot_label == "part_of":
        holder_agent.part_of = [x for x in holder_agent.part_of if x != filler]
    elif slot_label == "arguments":
        holder_agent.arguments = [x for x in holder_agent.arguments if x != filler]
    elif slot_label == "argument_of":
        holder_agent.argument_of = [x for x in holder_agent.argument_of if x != filler]
    elif slot_label == "justifications":
        holder_agent.justifications = [x for x in holder_agent.justifications if x != filler]
    elif slot_label == "inhibitions":
        holder_agent.inhibitions = [x for x in holder_agent.inhibitions if x != filler]
    else:
        dual_raise("remove_agent_from_slot: ",
                   "Unrecognized slot name: {}.".format(slot_label))


def remove_from_slot(holder_agent, slot_label, filler):
    # In addition to removing FILLET in SLOT_LABEL of HOLDER_AGENT, the function destroys the appropriate links.
    holder = find_agent(holder_agent)
    old_agent = find_agent(filler)
    remove_agent_from_slot(holder, slot_label, old_agent)
    remove_agent_from_slot(old_agent, get_opposite_slot(slot_label), holder)
    for l in holder.incoming_links:
        if l.sender == old_agent:
            remove_link(l, holder)
    for l in old_agent.incoming_links:
        if l.sender == holder:
            remove_link(l, old_agent)
        

def check_and_exchange_superclasses(mapping, concept):
    # Checks whether CONCEPT is above or bellow MAPPING through the hierarchy and adds slots if necessary.
    for superc in mapping.superclasses:
        if superc in collect_all_active_superclasses(concept):  # CONCEPT is somewhere bellow MAPPING.
            remove_from_slot(mapping, "superclasses", superc)
    flag = True
    for superc in mapping.superclasses:
        if superc in collect_all_active_subclasses(concept):  # CONCEPT is somewhere above MAPPING.
            flag = False  # It should not do anything!
    if flag:
        add_in_slot(mapping, "superclasses", concept)


# Collecting information #
##########################

def collect_subclasses_in_stm(agent):
    # Collects the direct subclasses.
    collected_agents = []
    if isinstance(agent, SemanticAgent):
        for ag in agent.subclasses:
            if ag in variables.working_memory:
                if not (isinstance(ag, MappingAgent)):
                    collected_agents = collected_agents + [ag]
    else:
        dual_raise("Collect_subclasses_in_stm",
                   "The agent: '{}' is not a Semantic agent.".format(agent))
    return collected_agents


def collect_all_active_subclasses(agent):
    # Collects all active subclasses.
    list_to_be_checked = remove_instances(collect_subclasses_in_stm(agent))
    all_subclasses = collect_subclasses_in_stm(agent)
    flag = True
    while flag:
        if list_to_be_checked:
            sub = list_to_be_checked[0]
            collected = collect_subclasses_in_stm(sub)
            list_to_be_checked = list_to_be_checked + remove_instances(collected)
            for subclass in collected:
                if isinstance(subclass, SemanticAgent):
                    all_subclasses = all_subclasses + [subclass]
            list_to_be_checked = list_to_be_checked[1:]
        else:
            flag = False
    return all_subclasses


def collect_subclasses_including_itself(agent):
    return collect_all_active_subclasses(agent) + [agent]


def collect_superclasses_in_stm(agent):
    # Collects the active DIRECT superclasses.
    collected_agents = []
    for ag in agent.superclasses:
        if ag in variables.working_memory:
            collected_agents = collected_agents + [ag]
    return collected_agents


def collect_all_active_superclasses(agent):
    # Collects all active superclasses.
    list_to_be_checked = collect_superclasses_in_stm(agent)
    all_superclasses = collect_superclasses_in_stm(agent)
    flag = True
    while flag:
        if list_to_be_checked:
            sup = list_to_be_checked[0]
            collected = collect_superclasses_in_stm(sup)
            list_to_be_checked = list_to_be_checked + collected
            all_superclasses = all_superclasses + collected
            list_to_be_checked = list_to_be_checked[1:]
        else:
            flag = False
    return all_superclasses


def collect_instance_of_in_stm(agent):
    # Collects the active DIRECT concept of the InstanceAgent.
    collected_agents = []
    for ag in agent.instance_of:
        if ag in variables.working_memory:
            collected_agents = collected_agents + [ag]
    if collected_agents:
        return collected_agents[0]
    else:
        return collected_agents


def get_instances_of_concept(concepts):
    # Collects the active DIRECT instances of the ConceptsAgent.
    instances = []
    for conc in concepts:
        for inst in conc.instances:
            if inst not in instances:
                if inst in variables.working_memory:
                    instances = instances + [inst]
    return instances


def get_all_instances_of_concept(concepts):
    # Collects the active instances (not only the direct ones) of the CONCEPTS.
    # NOTE: CONCEPTS should be a list!
    all_instances = []
    all_concepts = []
    for concept in concepts:
        all_concepts = all_concepts + [
            x for x in collect_subclasses_including_itself(concept) if x not in all_concepts]
    for concept in all_concepts:
        all_instances = all_instances + get_instances_of_concept([concept])
    return all_instances


def collect_agents_from_slot(agent, slot):
    # The function returns a list of all agents taking place into the slot.
    # If AGENT does not contain SLOT, the function returns an empty list.
    slot_list = []
    if hasattr(agent, slot):
        for a in get_slot_by_string(agent, slot):
            slot_list = slot_list + [a]
    return slot_list


def collect_agents_and_weights(agent, slot):
    # The function returns a list of dictionaries.
    # Each dictionary contains an agent which receives a link from AGENT (as key) and the weight of that link (as value).
    # SLOT refers to which agent-weight pairs should be extracted.
    # If there are no links or the SLOT is not valid, an empty list is returned.
    slot_list = []
    # hasattr() checks if the agent's class and the given slot/attribute are compatible.
    if hasattr(agent, slot):
        for a in get_slot_by_string(agent, slot):
            name = Str2(a.name)
            slot_list = slot_list + [{name: get_outgoing_link_weight(agent, a)}]
    return slot_list


# Functions checking if there are paths up and down #
#####################################################
    
def find_all_above_intersections(agent1, agent2):
    # Function, which returns all active intersections between the agents' superclasses (not only the first one).
    # Works both with concepts and with instances.
    agents_intersection = []
    if (not isinstance(agent1, DualAgent)) or (not isinstance(agent2, DualAgent)):
        dual_raise("Find_all_above_intersections: ",
                   "The agent: {} or {} is not a DualAgent.".format(agent1, agent2))
    else:
        if ((isinstance(agent1, InstanceAgent)) and (isinstance(agent2, InstanceAgent)) or(
                    (isinstance(agent1, RelationInstanceAgent)) and (isinstance(agent2, RelationInstanceAgent)))):
            agent1_instance_of = collect_instance_of_in_stm(agent1)  # We assume that there is only one concept for every instance.
            agent2_instance_of = collect_instance_of_in_stm(agent2)
            if (not agent1_instance_of) or (not agent2_instance_of):
                return agents_intersection
            elif agent1_instance_of == agent2_instance_of:
                agents_intersection = [agent1_instance_of]
            else:
                agent1_superclasses = collect_all_active_superclasses(agent1_instance_of) + [agent1_instance_of]
                agent2_superclasses = collect_all_active_superclasses(agent2_instance_of) + [agent2_instance_of]
                agents_intersection = [val for val in agent1_superclasses if val in agent2_superclasses]
        elif (isinstance(agent1, ConceptAgent)) and (isinstance(agent2, ConceptAgent)):
            agent1_superclasses = collect_all_active_superclasses(agent1)
            agent2_superclasses = collect_all_active_superclasses(agent2)
            agents_intersection = [val for val in agent1_superclasses if val in agent2_superclasses]
        else:
            pass
            # print ("There is no intersection between the agents: {} and {}.".format(agent1, agent2))
    return agents_intersection


def search_path_above(sub, superc):
    # Checks whether it is a path above through the superclass hierarchy from SUB to SUPER. Returns BOOLEAN.
    # SUB could be an instance; SUPERC should be a concept!
    if not isinstance(superc, SemanticAgent):
        dual_raise("search_path_above: ", "The superclass {} is not a Semantic agent:".format(superc))
    flag = False
    if isinstance(sub, SemanticAgent):
        list_of_superclasses = sub.superclasses
    else:
        list_of_superclasses = sub.instance_of
    while list_of_superclasses and (not flag):
        total_list = []
        for c in list_of_superclasses:
            if c == superc:
                flag = True
            else:
                total_list = total_list + c.superclasses
                list_of_superclasses = [x for x in list_of_superclasses if x != c]
        list_of_superclasses = list_of_superclasses + total_list
    return flag
    

def give_the_first_intersection_only(list_of_concepts):
    # Removes the agents from LIST_OF_CONCEPTS that are superclasses of other agents from the same list.
    list_of_first_intersections = list_of_concepts
    list_of_other_concepts = list_of_concepts
    for concept in list_of_concepts:
        list_of_other_concepts = [x for x in list_of_other_concepts if x != concept]  # Removes!
        for other_concept in list_of_other_concepts:
            if other_concept in concept.superclasses:
                list_of_first_intersections = [x for x in list_of_first_intersections if x != other_concept]  # Removes!
            else:
                if concept in other_concept.superclasses:
                    list_of_first_intersections = [x for x in list_of_first_intersections if x != concept]  # Removes!
    return list_of_first_intersections


def marker_passing(agent1, agent2):
    if (not isinstance(agent1, EpisodicAgent)) or (not isinstance(agent2, EpisodicAgent)):
        dual_raise("Marker_passing: ",
                   "The agent: {} or {} is not an EpisodicAgent.".format(agent1, agent2))
    else:
        return give_the_first_intersection_only(find_all_above_intersections(agent1, agent2))


def check_mapping(agent1, agent2):
    if not isinstance(agent1, EpisodicAgent) or not isinstance(agent2, EpisodicAgent):
        dual_raise("check_mapping",
                   "{} or/and {} is/are non Episodic argument/s.".format(agent1, agent2))
    else:
        agents_intersection = [val for val in agent1.mappings if val in agent2.mappings]
        if agents_intersection:
            return agents_intersection[0]
        else:
            return False
        
# Functions for creating agents through various sources #
#########################################################


def integrity_agent(name, word, agents_to_activate, incoming_links, threshold, level_of_activation,
                    speed_of_change, part_of, has_parts, argument_of, superclasses, subclasses, instances, arity, arguments,
                    target_instance, base_instance, justifications, inhibitions, situations, instance_of, mappings):
    # Checks the integrity of the agent - more specifically whether the given values fulfill the slots requirements.
    # If any of the requirements is violated, it  signals an error accordingly.
    if name in variables.all_agents.keys():
        dual_raise("integrity_agent, name: ",
                   "The name '{}' of the agent you are trying to create already exists.".format(name))
    if word:
        if type(word) != str:
            dual_raise("integrity_agent, the word: ",
                       "'{}' is not of a str type.".format(word))
    if agents_to_activate:
        for act in agents_to_activate:
            if not (isinstance(act, DualAgent)):
                dual_raise("integrity_agent, the agent_to_activate: ",
                           "'{}', is not a Dual agent.".format(act))
    if incoming_links:
        for link in incoming_links:
            if not (isinstance(link, Link)):
                dual_raise("integrity_agent, in incoming_link: ",
                           "'{}' is not a link.".format(link))
    if threshold:
        if type(threshold) != float:
            dual_raise("integrity_agent, the threshold: ",
                       "'{}' is not a float number.".format(threshold))
    if level_of_activation:
        if type(level_of_activation) != float:
            dual_raise("integrity_agent, the level of activation: ",
                       "'{}' is not a float number.".format(level_of_activation))
    if speed_of_change:
        if type(speed_of_change) != float:
            dual_raise("integrity_agent, the speed_of_change: ",
                       "'{}' is not a float number.".format(speed_of_change))
    if part_of:
        for part in part_of:
            if not (isinstance(part, DualAgent)):
                dual_raise("integrity_agent, the part_of: ",
                           "'{}' is not a Dual agent.".format(part))
    if has_parts:
        for h_part in has_parts:
            if not (isinstance(h_part, DualAgent)):
                dual_raise("integrity_agent, the has_part: ",
                           "'{}' is not a Dual agent.".format(h_part))
    if argument_of:
        for arg in argument_of:
            if not (isinstance(arg, DualAgent)):
                dual_raise("integrity_agent, the argument_of: ",
                           "'{}' is not a Dual agent.".format(arg))
    if superclasses:
        for sup in superclasses:
            if not (isinstance(sup, DualAgent)):
                dual_raise("integrity_agent, the superclass: ",
                           "'{}' is not a Dual agent.".format(sup))      
    if subclasses:
        for sub in subclasses:
            if not (isinstance(sub, DualAgent)):
                dual_raise("integrity_agent, the subclass: ",
                           "'{}' is not a Dual agent.".format(sub))
    if instances:
        for inst in instances:
            if not (isinstance(inst, DualAgent)):
                dual_raise("integrity_agent, the instance: ",
                           "'{}' is not a Dual agent.".format(inst))
    if arity:
        if type(arity) != int:  # Checks if the arity is an integer number.
            dual_raise("integrity_agent, the arity: ",
                       "'{}' is not an integer number.".format(arity))
    if arguments:
        for arg in arguments:
            if not (isinstance(arg, DualAgent)):  # Checks if the arguments are Dual Agents.
                dual_raise("integrity_agent, the argument: ",
                           "'{}' is not a Dual agent.".format(arg))
    if arity and arguments:
        if (arity != 0) and (len(arguments) != arity):  # Checks if the number of arguments equals the arity.
            dual_raise("integrity_agent: ",
                       "The arity {} is not equal to the number of arguments '{}'.".format(arity, arguments))
    if target_instance:
        if (len(target_instance) != 1) or not (isinstance(target_instance[0], EpisodicAgent)):
            dual_raise("integrity_agent, the target_instance: ",
                       "'{}' is not an EpisodicAgent.".format(target_instance[0]))
    if base_instance:
        if (len(base_instance) != 1) or not (isinstance(base_instance[0], EpisodicAgent)):
            dual_raise("integrity_agent, the base_instance: ",
                       "'{}' is not an EpisodicAgent.".format(base_instance[0]))
    if situations:
        for sit in situations:
            if not isinstance(sit, DualAgent):
                dual_raise("integrity_agent, the situation: ",
                           "'{}' is not a Dual agent.".format(sit))
    if instance_of:
        for inst_of in instance_of:
            if not isinstance(inst_of, DualAgent):
                dual_raise("integrity_agent, the instance_of: ",
                           "'{}' is not a Dual agent.".format(inst_of))
    if justifications:
        for just in justifications:
            if not isinstance(just, DualAgent):
                dual_raise("integrity_agent, the justification: ",
                           "'{}' is not a Dual agent.".format(just))
    if inhibitions:
        for inh in inhibitions:
            if not isinstance(inh, DualAgent):
                dual_raise("integrity_agent, the inhibition: ",
                           "'{}' is not a Dual agent.".format(inh))
    if mappings:
        for mapp in mappings:
            if not isinstance(mapp, DualAgent):
                dual_raise("integrity_agent, the mapping: ",
                           "'{}' is not a Dual agent.".format(mapp))


def add_agent(name, agent_type=DualAgent, word="", comment="", threshold=threshold_agent_activation,
              level_of_activation=initial_agent_activation, speed_of_change=default_speed_of_change,
              agents_to_activate=[], incoming_links=[], argument_of=[], part_of=[], has_parts=[],
              instances=[], instance_of=[], target_instance=[], base_instance=[], situations=[],
              superclasses=[], subclasses=[], arity=0, arguments=[], mappings=[],
              justifications=[], inhibitions=[]):
    # A function that creates an agent of AGENT_TYPE
    # and adds it to the general registry of all agents - variables.all_agents.
    integrity_agent(name, word, agents_to_activate, incoming_links, threshold, level_of_activation,
                    speed_of_change, argument_of, part_of, has_parts, superclasses, subclasses,
                    instances, arity, arguments, target_instance, base_instance, justifications,
                    inhibitions,  situations, instance_of, mappings)
    
    # If all requirements are fulfilled, a new agent is created according to the agent_type.
    if agent_type == ConceptAgent:
        new_agent = ConceptAgent(name=name, word=word, comment=comment, threshold=threshold,
                                 agents_to_activate=agents_to_activate, incoming_links=incoming_links,
                                 level_of_activation=level_of_activation, speed_of_change=speed_of_change,
                                 superclasses=superclasses, subclasses=subclasses, instances=instances,
                                 has_parts=has_parts, part_of=part_of, argument_of=argument_of)

    elif agent_type == MappingAgent:
        new_agent = MappingAgent(name=name, word=word, comment=comment, threshold=threshold,
                                 agents_to_activate=agents_to_activate, incoming_links=incoming_links,
                                 level_of_activation=level_of_activation, speed_of_change=speed_of_change,
                                 superclasses=superclasses, target_instance=target_instance,
                                 base_instance=base_instance, justifications=justifications)

    elif agent_type == RelationConceptAgent:
        new_agent = RelationConceptAgent(name=name, word=word, comment=comment, threshold=threshold,
                                         agents_to_activate=agents_to_activate, incoming_links=incoming_links,
                                         level_of_activation=level_of_activation, speed_of_change=speed_of_change,
                                         arity=arity, arguments=arguments, instances=instances,
                                         superclasses=superclasses, subclasses=subclasses, has_parts=has_parts,
                                         part_of=part_of, argument_of=argument_of)

    elif agent_type == InstanceAgent:
        new_agent = InstanceAgent(name=name, word=word, comment=comment, threshold=threshold,
                                  agents_to_activate=agents_to_activate, incoming_links=incoming_links,
                                  level_of_activation=level_of_activation, speed_of_change=speed_of_change,
                                  situations=situations, instance_of=instance_of,  has_parts=has_parts,
                                  part_of=part_of, mappings=mappings, argument_of=argument_of)

    elif agent_type == RelationInstanceAgent:
        new_agent = RelationInstanceAgent(name=name, word=word, comment=comment, threshold=threshold,
                                          agents_to_activate=agents_to_activate, incoming_links=incoming_links,
                                          level_of_activation=level_of_activation, speed_of_change=speed_of_change,
                                          situations=situations, arity=arity, arguments=arguments,
                                          instance_of=instance_of, has_parts=has_parts, part_of=part_of,
                                          mappings=mappings, argument_of=argument_of)

    elif agent_type == UnrealAgent:
        new_agent = UnrealAgent(name=name, word=word, comment=comment, threshold=threshold,
                                agents_to_activate=agents_to_activate, incoming_links=incoming_links,
                                level_of_activation=level_of_activation, speed_of_change=speed_of_change,
                                situations=situations, instance_of=instance_of, has_parts=has_parts,
                                part_of=part_of, mappings=mappings, argument_of=argument_of,
                                justifications=justifications)

    elif agent_type == UnrealInstanceAgent:
        new_agent = UnrealInstanceAgent(name=name, word=word, comment=comment, threshold=threshold,
                                        agents_to_activate=agents_to_activate, incoming_links=incoming_links,
                                        level_of_activation=level_of_activation, speed_of_change=speed_of_change,
                                        argument_of=argument_of, part_of=part_of, has_parts=has_parts,
                                        situations=situations, instance_of=instance_of, mappings=mappings,
                                        justifications=justifications)

    elif agent_type == UnrealRelationInstanceAgent:
        new_agent = UnrealRelationInstanceAgent(name=name, word=word, comment=comment, threshold=threshold,
                                                agents_to_activate=agents_to_activate, incoming_links=incoming_links,
                                                level_of_activation=level_of_activation,
                                                speed_of_change=speed_of_change, situations=situations,
                                                arity=arity, arguments=arguments, instance_of=instance_of,
                                                has_parts=has_parts, part_of=part_of, mappings=mappings,
                                                argument_of=argument_of, justifications=justifications)
            
    else:
        dual_raise("Add_agent",
                   "The agent_type: '{}', that you are trying to create, does not exists.".format(agent_type))

    create_links_of_the_new_agent(new_agent)
    variables.all_agents.update({name: new_agent})
    variables.agents_not_in_STM = variables.agents_not_in_STM + [new_agent]
    return new_agent


def create_agent_by_str_agent_type(agent):
    # The function creates an agent by the given in the file information,
    # which does not need pre-processing.
    # For now agents_to_activate=agent['agents_to_activate'] and
    # incoming_links=agent['incoming_links'] will not be added.
    # If there are situations in which we need them, update the functions.
    if agent['agent_type'] == 'ConceptAgent':
        new_agent = add_agent(name=agent['name'], word=agent['word'],
                              agent_type=ConceptAgent,
                              comment=agent['comment'],
                              threshold=agent['threshold'],
                              level_of_activation=agent['level_of_activation'],
                              speed_of_change=agent['speed_of_change'])
    elif agent['agent_type'] == 'RelationConceptAgent':
        new_agent = add_agent(name=agent['name'], word=agent['word'],
                              agent_type=RelationConceptAgent,
                              comment=agent['comment'],
                              threshold=agent['threshold'],
                              level_of_activation=agent['level_of_activation'],
                              speed_of_change=agent['speed_of_change'])
    elif agent['agent_type'] == 'MappingAgent':
        new_agent = add_agent(name=agent['name'], word=agent['word'],
                              agent_type=MappingAgent,
                              comment=agent['comment'],
                              threshold=agent['threshold'],
                              level_of_activation=agent['level_of_activation'],
                              speed_of_change=agent['speed_of_change'])
    elif agent['agent_type'] == 'InstanceAgent':
        new_agent = add_agent(name=agent['name'], word=agent['word'],
                              agent_type=InstanceAgent,
                              comment=agent['comment'],
                              threshold=agent['threshold'],
                              level_of_activation=agent['level_of_activation'],
                              speed_of_change=agent['speed_of_change'])
    elif agent['agent_type'] == 'RelationInstanceAgent':
        new_agent = add_agent(name=agent['name'], word=agent['word'],
                              agent_type=RelationInstanceAgent,
                              comment=agent['comment'],
                              threshold=agent['threshold'],
                              level_of_activation=agent['level_of_activation'],
                              speed_of_change=agent['speed_of_change'])
    elif agent['agent_type'] == 'UnrealInstanceAgent':
        new_agent = add_agent(name=agent['name'], word=agent['word'],
                              agent_type=UnrealInstanceAgent,
                              comment=agent['comment'],
                              threshold=agent['threshold'],
                              level_of_activation=agent['level_of_activation'],
                              speed_of_change=agent['speed_of_change'])
    elif agent['agent_type'] == 'UnrealRelationInstanceAgent':
        new_agent = add_agent(name=agent['name'], word=agent['word'],
                              agent_type=UnrealRelationInstanceAgent,
                              comment=agent['comment'],
                              threshold=agent['threshold'],
                              level_of_activation=agent['level_of_activation'],
                              speed_of_change=agent['speed_of_change'])
    else:
        dual_raise("create_agent_by_str_agent_type",
                   "Unrecognized agent type: {}.".format(agent['agent_type']))
    return new_agent


def adjust_links_and_weights(agent):
    for slot in agent:
        # The slots are already dealt with.
        # If in further cases it is needed to allow to deal with
        # --> 'agents_to_activate' and 'incoming_links', upgrade the function.
        """
        if slot not in ['name', 'agent_type', 'comment', 'threshold',
                        'level_of_activation', 'speed_of_change',
                        'agents_to_activate', 'incoming_links', 'target', 'arity'] and not isinstance(agent[slot], int):
        """
        if slot not in ['name', 'word', 'agent_type', 'comment', 'threshold',
                        'level_of_activation', 'speed_of_change',
                        'agents_to_activate', 'incoming_links', 'target', 'arity'] and not isinstance(agent[slot], int):
            connections = json.loads(agent[slot])
            for conn in connections:
                for key, value in conn.items():
                    add_agent_in_slot(find_agent(agent['name']), slot, find_agent(key))
                    create_link(find_agent(agent['name']), find_agent(key), value)
        if slot == 'target' and agent['target'] == 1:
            variables.target_agents = variables.target_agents + [find_agent(agent['name'])]
        if slot == 'arity':
            find_agent(agent['name']).arity = agent['arity']


# The class below - Str2 - turns strings with single quotes into strings with double quotes.
# This is explicitly needed when working with json data format.


class Str2(str):
    def __repr__(self):
        # Allows str.__repr__() to do the hard work of how a string would be represented.
        # Then, the outer two characters, single quotes, and replace them with double quotes.
        return ''.join(('"', super().__repr__()[1:-1], '"'))


def save_kb_to_file(file_name):
    # A function that saves the current KB to a file with name FILE_NAME
    # so it could be exactly reproduced in any time.
    # The function MUST be run before any cycles.
    # FILE_NAME should be a string ending with '.csv'.
    custom_header = True
    for agent in variables.all_agents.values():
        if not agent.word:
            word = "no_word"
        elif agent.word == 'nan':
            word = "no_word"
        else:
            word = agent.word
        argument_of = collect_agents_and_weights(agent, "argument_of")
        part_of = collect_agents_and_weights(agent, "part_of")
        has_parts = collect_agents_and_weights(agent, "has_parts")
        superclasses = collect_agents_and_weights(agent, "superclasses")
        subclasses = collect_agents_and_weights(agent, "subclasses")
        instances = collect_agents_and_weights(agent, "instances")
        target_instance = collect_agents_and_weights(agent, "target_instance")
        base_instance = collect_agents_and_weights(agent, "base_instance")
        justifications = collect_agents_and_weights(agent, "justifications")
        inhibitions = collect_agents_and_weights(agent, "inhibitions")
        instance_of = collect_agents_and_weights(agent, "instance_of")
        mappings = collect_agents_and_weights(agent, "mappings")
        arguments = collect_agents_and_weights(agent, "arguments")
        if isinstance(agent, RelationConceptAgent) or isinstance(agent, RelationInstanceAgent):
            arity = agent.arity
        else:
            arity = []
        situations = collect_agents_and_weights(agent, "situations")
        if agent in variables.target_agents:
            target = 1
        else:
            target = 0
        line = {'name': agent.name, 'word': word, 'agent_type': type(agent).__name__, 'comment': agent.comment,
                'threshold': agent.threshold, 'level_of_activation': agent.level_of_activation,
                'speed_of_change': agent.speed_of_change, 'agents_to_activate': [[]],
                'incoming_links': [[]], 'argument_of': [argument_of],
                'part_of': [part_of], 'has_parts': [has_parts], 'superclasses': [superclasses],
                'subclasses': [subclasses], 'instances': [instances], 'instance_of': [instance_of],
                'target_instance': [target_instance], 'base_instance': [base_instance], 'justifications': [justifications],
                'inhibitions': [inhibitions], 'mappings': [mappings], 'arity': [arity], 'arguments': [arguments],
                'situations': [situations], 'target': [target]}

        df = pandas.DataFrame(line, columns=['name', 'word', 'agent_type', 'comment',
                                             'threshold', 'level_of_activation', 'speed_of_change',
                                             'agents_to_activate', 'argument_of', 'incoming_links', 'part_of', 'has_parts',
                                             'superclasses', 'subclasses', 'instances', 'instance_of',
                                             'target_instance', 'base_instance', 'justifications', 'inhibitions',
                                             'mappings', 'arity', 'arguments', 'situations', 'target'])

        # Appends AGENT to the existing file.
        with open(file_name, 'a') as file:
            df.to_csv(file, header=custom_header)
        # custom_header = False so the columns' names will not be appended again;
        custom_header = False


def load_kb_from_file(file_name):
    # A function that loads a KB from a file with name FILE_NAME.
    # FILE_NAME should be a string ending with '.csv'.  
    df = pandas.read_csv(file_name)
    # KB is a list of dictionaries where each dictionary is an agent with all of its information.
    kb = df.T.to_dict().values()
    kb = list(kb)
    for agent in kb:
        # The agent is created by the given parameters in the file.
        create_agent_by_str_agent_type(agent)
    for agent in kb:
        #print(agent)
        adjust_links_and_weights(agent)

        
# END OF FILE: agents_manipulation.py #
