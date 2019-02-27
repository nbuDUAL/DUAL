
##################
# main C Y C L E #
##################


# DEFINES FUNCTIONS CONNECTED TO THE MAIN CYCLE OF DUAL. 
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018

#####################
# External protocol #
#####################

"""
DUAL's principle postulates that the exchange of activation between the DUAL agents is continuous
(like the activation itself). In the architecture this continuous exchange is approximated by a sequence of 'cycles'.
During each cycle, the activation levels of all agents are updated. This leads to inclusion and exclusion of agents
from the working memory, as activation levels go above and below the threshold.

* cycles (number)
--> The function calls the function "main_cycle" NUMBER of times.
At the end, the function prints information about:
Total activation; the content of the Goal list; the content of the Input list; which agent is the focus of attention;
all the mappings, which are in the STM; all current requests and all anticipated agents.

* initialize_dual()
--> When DUAL is initiated, the function sets the global variable variables.dual_time to 0;
the level of activation of all agents is annulled; all temporary agents are deleted;
the global variables: input_list, goal_list, short_term_memory, focus_of_attention,
abstract_focus_of_attention, list_of_anticipations and agents_not_in_STM are emptied.
At the end, the agents which are not in the Short-Term Memory are initialized.

* re_initialize_dual()
--> The function resets all variables and destroys all existing agents.

* main_activation_cycle ()
--> A generic function that implements one cycle of the built-in routine/the work of the architecture.
Each cycle performs the following steps:
adds 1 time step in addition to Dual's time; sends for updating of the activation of all agents;
sends for dealing with the agents that just entered the WM and the agents that left the WM;
sends for handling the requests for the creation of new mappings and anticipations and
sends for transforming the anticipations into new instances and the mappings into concepts
if their activation is above the threshold. First reviewed are the anticipations
(starting from the most active one), then reviewed are the mappings (also starting from the most active one).
"""

from memory_consolidation import *
import variables


def cycles(number):
    # The function calls function "main_cycle" NUMBER of times.
    # If the the global variable variables.verbose == True, summary information is printed.
    for i in range(number):
        main_activation_cycle()
    if variables.verbose:
        print("THE DUAL TIME IS: {}".format(variables.dual_time))
        print("Total activation is: {}".format(total_activation()))
        print("GOAL list is: ", ", ".join(str(x) for x in variables.goal_list.keys()))
        print("INPUT list is: ", ", ".join(str(x) for x in variables.input_list.keys()))
        active_agents = [x for x in variables.short_term_memory if not isinstance(x, MappingAgent)]
        print("The length of the STM is: {} with permanent agents: {}".format(len(variables.short_term_memory),
                                                                              active_agents))        
        print("The requests in are: ", ", ".join(str(x) for x in variables.list_of_all_requests))
        print("The mappings agents are: ", ", ".join(str(x) for x in variables.list_of_mappings))
        print("The anticipated agents are: ", ", ".join(str(x) for x in variables.list_of_anticipations))
        print("New concepts: ", ", ".join(str(x) for x in variables.just_created if isinstance(x, ConceptAgent) or isinstance(x, RelationConceptAgent)))


def initialize_dual():
    # When DUAL is initiated, the level of activation of all agents is annulled; all temporary agents are deleted.
    # In addition, the global variables are emptied.
    variables.dual_time = 0
    removed = []
    for agent in variables.all_agents.values():
        agent.level_of_activation = 0.00
        if isinstance(agent, MappingAgent):
            removed = removed + [agent]
        if isinstance(agent, UnrealAgent):
            removed = removed + [agent]
    for a in removed:
        if a in variables.all_agents.values():
            remove_agent(a)
        if a in variables.all_agents.values():
            variables.all_agents.pop(a.name)
    remove_from_working_memory()
    variables.input_list = {}
    variables.goal_list = {}
    variables.list_of_anticipations = []
    variables.short_term_memory = []
    variables.focus_of_attention = []
    variables.abstract_focus_of_attention = []
    variables.just_created = []
    variables.list_of_all_requests = []
    variables.target_situation = []
    variables.target_agents = []
    variables.agents_not_in_STM = []
    add_to_agents_not_in_STM()


def re_initialize_dual():
    # The function resets all variables and destroys all existing agents.
    initialize_dual()
    for ag in variables.all_agents.values():
        del ag
    variables.all_agents = {}


def main_activation_cycle():
    # The work of the architecture is done in cycles. Each cycle performs the following steps:
    variables.dual_time += 1
    update_incoming_activation()
    update_activations()
    change_weights_and_thresholds()
    remove_from_working_memory()
    list_of_just_entered_the_wm = add_to_working_memory()
    update_incoming_activation()
    update_activations()
    change_weights_and_thresholds()
    # update_focus()
    update_input_goal()
    for t in variables.target_agents:
        if t not in variables.working_memory:
            variables.working_memory = variables.working_memory + [t]
    for a in list_of_just_entered_the_wm:
        handle_just_entered_in_wm_agents(a)
    handle_the_list_of_requests(variables.list_of_all_requests)
    # Think about whether the activation levels of the anticipations and the mappings
    # should be recalculated twice in one cycle.
    # for a in variables.list_of_anticipations:
    #    a.level_of_activation = update_activation(a, a.input_activation)
    # for m in variables.list_of_mappings:
    #    m.level_of_activation = update_activation(m, m.input_activation)
    variables.list_of_anticipations = sorted(variables.list_of_anticipations,
                                             key=lambda x: x.level_of_activation)
    variables.list_of_anticipations.reverse()
    variables.list_of_mappings = sorted(variables.list_of_mappings,
                                        key=lambda x: x.level_of_activation)
    variables.list_of_mappings.reverse()
    if variables.enable_classification:
        for ant in variables.list_of_anticipations:
            if ant.level_of_activation >= anticipation_into_instance_threshold:
                if ant.justifications:  # CHECK IN WHICH CASES THERE WILL BE A WINNING ANTICIPATION WITHOUT JUSTIFICATION.
                    anticipation_into_instance(ant)
    if variables.enable_concept_learning:
        for m in variables.list_of_mappings:
            if m.level_of_activation >= mapping_into_concept_threshold:
                mapping_into_concept(m)
    
# END OF FILE MAIN_CYCLE.PY #
