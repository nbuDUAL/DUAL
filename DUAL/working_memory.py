
##################
# WORKING MEMORY #
##################

# DEFINES FUNCTIONS DEALING WITH THE WORkING MEMORY OF THE ARCHITECTURE.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018

# TO DO: define the Abstract/Second focus!
# --> check the change_focus() function.

"""
According to DUAL's specification, the working memory of the system consists of all (and only) the active agents.
(Note that this includes all temporary agents above the activation threshold at the time.) It also requires that
the activation level of an agent should be above certain pre-specified threshold (parameters.threshold_agent_activation)
in order to enter the working memory. Whenever the activation level of some agent exceeds the threshold, the agent is
automatically included into the working memory. In reverse, whenever the activation level drops below the threshold,
the agent is automatically excluded from the working memory. Exclusion from WM has certain consequences:
the contents of the volatile memory is lost - temporary links (and agents) are destroyed, etc.
By definition, the most active DUAL-agent at any given moment is called to be 'in the focus' at that moment.

.......

.......WHAT HAPPENS WHEN AN AGENT ENTERS THE WM. ........

The structure-correspondence (SC) mechanism generates new mappings/correspondences on the basis of existing ones.
It also creates excitatory links between corresponding/coherent mappings.
Even though there are two major types of SC, conventionally termed BOTTOM-UP and TOP-DOWN SC,
for now the architecture is implemented only with the TOP-DOWN one.
The essence of TOP-DOWN SC is that if two propositions are mapped their arguments should also be mapped.
This is in line with Gentner's (1983) systematicity principle.
In the case of the DUAL architecture the SC is carried out by mappings between relational instance agents.
It frequently happens that the SC-generated hypotheses are not really new,
meaning that the same agents have been already put into correspondence.
In such cases a new justification of the correspondence is added (in case it is a duplicate it is just ignored).

* add_to_working_memory()
--> A generic function that adds all agents above the predefined threshold for entering the WM,
provided those agents are not in the WM already. he function returns a list of those agents.

* add_to_agents_not_in_STM()
--> All agents, which are not in the global lists: variables.input_list and variables.goal_list,
are added to the global variable variables.agents_not_in_STM, thus initialized as agents not in the Short-Term Memory.

* remove_from_working_memory()
--> A generic function that collects all agents from the working memory whose activation level drops
below the predefined threshold. Then for each of those agents the function clean_after_removing_from_wm(AGENT)
is called so the WM can be cleaned from those agents.

* clean_after_removing_from_wm(agent)
--> Whenever the activation level of a certain agent drops below the WM threshold,
the contents of the working memory is cleared of that agent and all traces that this agent has - such as mappings.
The function removes AGENT from the following global variables: variables.target_agents, variables.short_term_memory;
variables.focus_of_attention; variables.abstract_focus_of_attention; variables.list_of_anticipations.
At the end, AGENT is added to the global variable variables.agents_not_in_STM.

* handle_just_entered_in_wm_agents(agent)
--> Depending on the AGENT's type, AGENT is send to its corresponding function.
If AGENT is Concept Agent or Relation Concept Agent, the function concept_into_wm(AGENT) is called.
If AGENT is Mapping Agent, the function mapping_into_wm(AGENT) is called.
If AGENT is Episodic Agent, the function target_episode_into_wm(AGENT) or base_episode_into_wm(AGENT) is called.
If AGENT is Unreal Episodic Agent, the function inhibit_competing_anticipations(AGENT) is called in addition.

# Collecting agents in the working memory #
###########################################

* collect_superclasses_in_stm(agent)
--> Returns a list of all direct superclasses of AGENT, which are in the Working Memory.

* collect_all_active_superclasses(agent)
--> Returns a list of all superclasses of AGENT, which are in the Working Memory.

* collect_instance_of_in_stm(agent)
--> Returns a list containing the direct concept of AGENT if it is in the Working Memory.

* get_instances_of_concept(list)
--> Returns a list containing all instances, which are in the Working Memory, of all the LIST's concepts.
    
* collect_subclasses_in_stm(agent)
--> Returns a list containing the direct subclasses of AGENT if it is in the Working Memory.

* collect_all_active_subclasses(agent)
--> Returns a list of all subclasses of AGENT, which are in the Working Memory.

* collect_subclasses_including_itself (agent)
--> Returns a list containing AGENT and all subclasses of AGENT, which are in the Working Memory.

# Functions for Mapping checks #
################################

* check_mapping (agent1, agent2) --> Checks if there is a mapping between AGENT1 and AGENT2.
Returns the mapping/abstraction or False if there is no such.

* collect_mappings (agent)
--> Returns a list containing all the abstractions that AGENT takes part in.
If there is no such, the function returns [].

* check_intersection(agent1, agent2)
--> Returns a list containing all intersections between AGENT1 and AGENT2. If there is no such, the function returns [].

* is_abstraction (agent) --> Returns True if AGENT is an abstraction/mapping, otherwise returns False.

# Functions dealing with AGENT after it enters the Working Memory #
###################################################################

* divide_target_and_base(list)
--> Divides LIST into Target agents and Base agents and returns them as two lists.

* concept_into_wm(agent)
--> Checks all instances of AGENT, which are in the working memory.
Returns a list of mapping requests between all of the AGENT's instances.
If there is already a mapping between some, additional links between AGENT and the mapping are added.

* base_episode_into_wm (agent)
--> The function iterates through the global variable variables.target_agents and looks for instances
that can be mapped with AGENT. Returns a list of mapping requests.

* target_episode_into_wm (agent)
--> The function iterates through all instance agents in the Working Memory and checks if they can be mapped with AGENT.
Returns a list of mapping requests.

* mapping_into_wm (mapping)
-->  First the function finds the base and the target elements.
Sets bidirectional inhibitory links for between MAPPING and all mappings that contradict/inhibit each other.
If the base and the target elements are arguments of relations, a "bottom-up structural correspondence" is activated.
If the relations are mapped, additional links are added. Otherwise, ?check_relation_anticipation(b_relation)?
If the base and the target elements are relations themselves, a top-down structural correspondence is set.
At the end, the function looks for possible superclasses of MAPPING, which can be anticipated.
If there are such, requests are added to the global variable variables.list_of_all_requests.

* structural_correspondence (target_relation, base_relation, upper_mapping)
--> The function checks if the arguments of TARGET_RELATION and BASE_RELATION are already mapped.
If they are, additional justification links are added from the UPPER_MAPPING.
Otherwise, a new mapping is created, and it inherits the common relational role as a superclass.

# FOCUS functions #
###################

change_focus (agent) --> TO BE DEFINED!

linear_focus(activation, speed)
"""

from structures import *


def add_to_agents_not_in_STM():
    # Initializes the agents, which are not in the Short-Term Memory.
    for agent in variables.all_agents.values():
        if (not (agent in variables.input_list.keys())) and (not (agent in variables.goal_list.keys())):
            variables.agents_not_in_STM = variables.agents_not_in_STM + [agent]


def add_agent_to_working_memory(ag):
    agent = find_agent(ag)
    if agent in variables.working_memory:
        if variables.flag_error:
            print("add_agent_to_working_memory: {} is already in the WM.".format(agent))
    else:
        if agent:
            variables.short_term_memory = variables.short_term_memory + [agent]
            variables.agents_not_in_STM.remove(agent)
            variables.working_memory = variables.working_memory + [agent]
        else:
            dual_raise("add_agent_to_working_memory",
                       "Not existing agent: {}.".format(ag))


def add_to_working_memory():
    # Returns a list of agents, which just entered into the Working memory.
    list_of_agents = []
    for agent in variables.agents_not_in_STM:
        if agent.level_of_activation >= threshold_agent_activation:
            list_of_agents = list_of_agents + [agent]
            variables.short_term_memory = variables.short_term_memory + [agent]
    for ag in list_of_agents:
        variables.agents_not_in_STM.remove(ag)   
    return list_of_agents


def remove_from_working_memory():
    list_of_agents = []
    for agent in variables.working_memory:
        if agent.level_of_activation < threshold_agent_activation:
            if agent not in variables.target_agents:
                list_of_agents = list_of_agents + [agent]
    for ag in list_of_agents:
        clean_after_removing_from_wm(ag)


def clean_after_removing_from_wm(agent):
    # if agent in target_situation:
    #    target_situation.remove(agent)
    # if agent in variables.target_agents:
        # variables.target_agents.remove(agent)
    if agent in variables.short_term_memory:
        variables.short_term_memory.remove(agent)
    # if agent == focus_of_attention:
    #    focus_of_attention = []
    # if agent == .abstract_focus_of_attention:
    #    abstract_focus_of_attention = []
    if not (agent in variables.agents_not_in_STM):
        variables.agents_not_in_STM = variables.agents_not_in_STM + [agent]
    if isinstance(agent, EpisodicAgent):
        for m in agent.mappings:
            remove_agent(m)
        if isinstance(agent, UnrealAgent):
            remove_agent(agent)
    if isinstance(agent, MappingAgent):
        # JUST TEST IT THAT WAY. I think that for now is better;
        # Think about making the anticipation the same way
        variables.deactivated_agents = variables.deactivated_agents + [agent]
        # remove_agent(agent)


def handle_just_entered_in_wm_agents(agent):
    if (isinstance(agent, ConceptAgent)) or (isinstance(agent, RelationConceptAgent)):
        concept_into_wm(agent)
    elif isinstance(agent, MappingAgent):
        mapping_into_wm(agent)
    elif isinstance(agent, EpisodicAgent):
        if isinstance(agent, UnrealAgent):
            return[]
        elif agent in variables.target_agents:
            target_episode_into_wm(agent)
        else:
            base_episode_into_wm(agent)
    else:
        dual_raise("Handle_just_entered_in_wm_agents: ",
                   "Unrecognized type of agent: '{}' entered the WM.".format(agent))


# Steps after the Agent enters the working memory #
###################################################

def divide_target_and_base(list_of_agents):
    # Takes a list of agents. Divides the list into Target agents and Base agents.
    # It returns them as two lists.
    list_of_target_agents = []
    list_of_base_agents = []
    for agent in list_of_agents:
        if agent in variables.target_agents:
            list_of_target_agents = list_of_target_agents + [agent]
        else:
            list_of_base_agents = list_of_base_agents + [agent]
    return list_of_target_agents, list_of_base_agents


def concept_into_wm(agent):
    # A function which checks the agent's instances for eventual mapping creations.
    if agent in variables.just_created:
        return []
    orders_for_new_agents = []
    if not ((agent, ConceptAgent) or (agent, RelationConceptAgent)):
        dual_raise("Concept_into_wm: ",
                   "The agent: '{}' is not a Semantic agent/or it is a MappingAgent.".format(agent))
    else:
        target_base = divide_target_and_base(get_instances_of_concept(collect_subclasses_including_itself(agent)))
        target_elements = target_base[0]
        base_elements = target_base[1]
        if isinstance(target_elements, UnrealAgent) or isinstance(base_elements, UnrealAgent):
            return []
        for t in target_elements:
            for b in base_elements:
                if isinstance(t, UnrealAgent) or isinstance(b, UnrealAgent):
                    return []
                mapping = check_mapping(t, b)
                if mapping:
                    check_and_exchange_superclasses(mapping, agent)
                else:
                    check = [x for x in t.instance_of if x in b.instance_of]  # Checks only the direct class
                    if check:
                        for sub in check:
                            if sub in variables.just_created:
                                return []  # The job is already done!
                            else:
                                comment = "Created by {} in time {}.".format(agent, variables.dual_time)
                                # [] are the justifications
                                orders_for_new_agents = orders_for_new_agents + make_request_for_mapping(agent, [], t, b, comment)
                                
                    else:
                        t_sup = [t.instance_of[0]]
                        t_sup = t_sup + collect_all_active_superclasses(t.instance_of[0])
                        b_sup = [b.instance_of[0]]
                        b_sup = b_sup + collect_all_active_superclasses(b.instance_of[0])
                        for sub in [x for x in t_sup if x in b_sup]:
                            if sub in variables.just_created:
                                return []  # The job is already done!
                            else:
                                comment = "Created by {} in time {}.".format(agent, variables.dual_time)
                                orders_for_new_agents = orders_for_new_agents + make_request_for_mapping(agent, [], t, b, comment)  # [] are the justifications

    for superc in collect_all_active_superclasses(agent):
        concept_into_wm(superc)
    return orders_for_new_agents


def base_episode_into_wm(agent):
    # Looks for a partner in the TARGET_AGENTS list.
    if agent in variables.just_created:
        return []
    order_for_new_agents = []
    for t in variables.target_agents:
        if isinstance(t, UnrealAgent) or isinstance(agent, UnrealAgent):
            return []
        if (isinstance(t, InstanceAgent)) or (isinstance(t, RelationInstanceAgent)) and (t in variables.working_memory):
            mapping = check_mapping(t, agent)
            if mapping:
                dual_raise("base_episode_into_wm",
                           "'{}' just entered the wm, and it is already mapped '{}'.". format(agent, mapping))
            else:    
                intersections = marker_passing(t, agent)
                if intersections:
                    comment = "Created by {} in time {}.".format(agent, variables.dual_time)
                    order_for_new_agents = order_for_new_agents + make_request_for_mapping(intersections[0], [], t, agent, comment)  # [] are the justifications
    for relation in agent.argument_of:
        for mapp in relation.mappings:
            if (mapp in variables.working_memory) and (mapp.target_instance[0] in variables.working_memory) and (relation in variables.working_memory):
                structural_correspondence(mapp.target_instance[0], relation, mapp)
    return order_for_new_agents


def target_episode_into_wm(agent):
    if agent in variables.just_created:
        return []
    order_for_new_agents = []
    base_agents = [ag for ag in variables.short_term_memory if (ag not in variables.target_agents) and (isinstance(ag, EpisodicAgent))]
    for b in base_agents:
        if isinstance(b, UnrealAgent):
            return []
        intersections = marker_passing(agent, b)
        if intersections:
            if check_mapping(agent, b):
                dual_raise("target_episode_into_wm",
                           "'{}' just entered the wm, and it is already mapped '{}'.".format(agent, check_mapping(agent, b)))
            else:
                comment = "Created by {} in time {}.".format(agent, variables.dual_time)
                order_for_new_agents = order_for_new_agents + make_request_for_mapping(intersections[0], [], agent, b, comment)  # [] are the justifications
    for relation in agent.argument_of:
        for mapp in relation.mappings:
            if (mapp in variables.working_memory) and (mapp.base_instance[0] in variables.working_memory) and (relation in variables.working_memory):
                structural_correspondence(relation, mapp.base_instance[0], mapp)
    return order_for_new_agents


def mapping_into_wm(agent):
    # AGENT should be MappingAgent.
    # AGENT is a mapping (abstraction) between a target and base element.
    if not isinstance(agent, MappingAgent):
        dual_raise("Mapping into wm: ",
                   "The agent: '{}' is not an abstraction.".format(agent))
    else:
        # 1. Find BaseElement and TargetElement.
        t = agent.target_instance[0]
        b = agent.base_instance[0]
        # Setting inhibitory links for all mappings that contradict/inhibit each other.
        inhibit_competitory_mappings(agent)
        # Bottom-up structural correspondence.
        for b_relation in b.argument_of:
            for t_relation in t.argument_of:
                m = check_mapping(b_relation, t_relation)
                if m:
                    if [i for i, x in enumerate(b_relation.arguments) if x == b] == [i for i, x in enumerate(t_relation.arguments) if x == t]:
                        create_link(m, agent, default_mapping_to_mapping_support_weight)
                        create_link(agent, m, default_mapping_to_mapping_support_weight)
                        if m not in agent.justifications:
                            agent.justifications = agent.justifications + [m]
                        if agent not in m.justifications:
                            m.justifications = m.justifications + [agent]
                else:
                    # If there is a relation without corresponding one,
                    # check if its arguments are all mapped to something in the target.
                    # For now, we think that the function needs only the relation as an argument.
                    check_relation_anticipation(b_relation)
        # Top-down structural correspondence.
        if (isinstance(t, RelationInstanceAgent)) and (isinstance(b, RelationInstanceAgent)):
            if t.arity != b.arity:
                dual_raise("Mapping into wm: ",
                           "'{}' and '{}' are mapped, even though they are with different arity.".format(t, b))
            else:
                # 2. If BaseElement and TargetElement are Relations, go to function for Structural Correspondence.
                structural_correspondence(t, b, agent)
        # Looks for possible superclasses, which can be anticipated.
        variables.list_of_all_requests = variables.list_of_all_requests + check_common_part_of_concept(agent)


def structural_correspondence(target_relation, base_relation, upper_mapping):
    for i in range(target_relation.arity):
        t = target_relation.arguments[i]
        b = base_relation.arguments[i]
        flag = True  # Searches for a path above to find the common conceptual role.
        for just in upper_mapping.superclasses:
            if (search_path_above(target_relation, just)) and (search_path_above(base_relation, just)):
                sup = just.arguments[i]
                flag = False
        
        if flag:
            if target_relation.instance_of[0] == base_relation.instance_of[0]:
                if target_relation.instance_of[0] not in upper_mapping.superclasses:
                    upper_mapping.superclasses = [target_relation.instance_of[0]]
                    if ((search_path_above(target_relation, target_relation.instance_of[0])) and (
                            search_path_above(base_relation, target_relation.instance_of[0]))):
                        sup = target_relation.instance_of[0].arguments[i]
                        flag = False
        
        if flag:
            dual_raise("structural_correspondence: ",
                       "We couldn't find a super_role for: {}, {}, mapping {} and its superclasses {} and current sup {}, argument {}". format(
                           target_relation, base_relation, upper_mapping, upper_mapping.superclasses, just, i))
        m = check_mapping(t, b)
        if m:
            create_link(m, upper_mapping, default_str_corr_weight)
            create_link(upper_mapping, m, default_str_corr_weight)
            if m not in upper_mapping.justifications:
                upper_mapping.justifications = upper_mapping.justifications + [m]
            if upper_mapping not in m.justifications:
                m.justifications = m.justifications + [upper_mapping]
            if sup not in m.superclasses:
                add_in_slot(m, "superclasses", sup)
        else:
            if (t in variables.working_memory) and (b in variables.working_memory):
                comment = "Created by {} in time {}.".format(upper_mapping, variables.dual_time)
                variables.list_of_all_requests = variables.list_of_all_requests + make_request_for_mapping(
                    sup, [upper_mapping], t, b, comment=comment)
            else:
                pass

            
# FOCUS functions #
###################

# def update_focus():

#    active_agents = short_term_memory
#    for agent in input_list.keys():
#        active_agents = active_agents + [agent]
#    for agent2 in goal_list.keys():
#        active_agents = active_agents + [agent2]
#    new_focus = focus_of_attention
#    if (not focus_of_attention):
#        strength_focus = 0.0
#    else:
#        active_agents.remove(focus_of_attention)
#        strength_focus = calculate_current_focus_strength (focus_of_attention)
#    for agent in active_agents:
#        focus_attempt = linear_focus (agent.level_of_activation, agent.speed_of_change)
#        if focus_attempt > update_focus_threshold:
#            if (not focus_of_attention or (focus_attempt > strength_focus)):
#                new_focus = agent
#                strength_focus = calculate_current_focus_strength (new_focus)
#    if (new_focus != focus_of_attention):  ## CHANGE FOCUS
#        if verbose:
#            print ()
#            print ("Change of the Focus: {}". format(new_focus.name))
#            print ()
#        grouping.change_focus (new_focus)
#    if strength_focus < update_focus_threshold:       ## Deletes focus
#        if verbose:
#            print (strength_focus)
#            print ()
#            print ("Change of the Focus: EMPTY")
#            print ()
#        focus_of_attention = []


def change_focus(agent):
    pass
"""
    old_target_situation = variables.target_situation
    variables.focus_of_attention = agent
    name = additions.gen_name_sit (agent.name)
    new_situation = classes.add_agent (name, classes.InstanceAgent)
    variables.target_agents = variables.target_agents + [new_situation]
    links.create_link (agent, new_situation, parameters.creator_group_weight)
    links.create_link (new_situation, agent, parameters.group_creator_weight)
    new_situation.level_of_activation = agent.level_of_activation * parameters.bootstrapping_activation_of_focus
    variables.target_situation = [new_situation]
    if old_target_situation:
        for old_sit in old_target_situation:
            for sit in additions.collect_agents_situations (old_sit):
                links.create_link (new_group, sit, parameters.new_focus_old_focus_weight)
"""


def linear_focus(activation, speed):
    return importance_coefficient * speed + new_activation_coefficient * activation

# END OF FILE WORKING_MEMORY.PY #
