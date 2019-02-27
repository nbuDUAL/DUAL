
##############
# ACTIVATION #
##############

# DEFINES FUNCTIONS CONNECTED TO THE AGENTS' ACTIVATION AS WELL AS THE INPUT_LIST AND GOAL_LIST.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018

# TO DO: change_weights_and_thresholds() function - MAYBE THIS IS THE HEBBIAN LEARNING?

"""
Activation can enter the DUAL network from two special nodes called:
INPUT NODE and GOAL NODE - constant (and strong) sources of activation.
Those nodes model the influence of the environment.
The human user of the system attaches some agents to those node, thus allowing for the spread of activation.

* add_to_input (agent, activation)
--> Adds AGENT to the global variables variables.input_list.
If AGENT is relation, the relation's argument(s) are also added to the global variables variables.input_list
with the same ACTIVATION. The default value of ACTIVATION is 1.00
In addition, adds AGENT and all other agents that are related with argument-links, to the variables.target_agents.

* remove_from_input (agent) --> Removes AGENT from the global variables variables.input_list.

* add_to_goal (agent, activation) --> Adds AGENT to the global variables variables.goal_list.
If AGENT is relation, the relation's argument(s) are also added to the global variables variables.goal_list
with the same ACTIVATION. The default value of ACTIVATION is 1.00.

* remove_from_goal (agent) --> Removes AGENT from the global variables variables.goal_list.

* update_input_goal() --> If an agent has been added to the global variables variables.input_list
or goal_list on the previous cycle, the function removes it
from the global variables variables.short_term_memory and variables.agents_not_in_STM.

# Activation functions #
########################

* total_activation () --> Returns a float number expressing the total activation of all agents.

* update_incoming_activation() --> Updates the activation level of all existing agents.

* update_activations() --> Updates the activation level of all existing agents.
In addition, the speed of activation is also calculated.

* calculate_input (agent) --> Returns a float number expressing the activation that AGENT receives.

* update_activation (agent, input_activation, function) --> The INPUT_ACTIVATION of AGENT is calculated.
The default value of FUNCTION is "activation_function" and it can be seen in parameters.py

* change_weights_and_thresholds() --> TO BE PROGRAMED.

* add_noise_in_all_activations(variance)
--> Adds random noise to the level of activation of all agents in variables.all_agents with VARIANCE.

"""

from working_memory import *
from structures import collect_all_relational_interconnected
import variables
from random import gauss


def add_to_input(ag, activation=1.00):
    # Adds AG(agent) to INPUT_LIST and/or updates the agent's activation.
    # In addition, adds AG and all other agents that are related with argument-links, to the variables.target_agents
    agent = find_agent(ag)
    if not (isinstance(agent, EpisodicAgent)):
        dual_raise("ADD_TO_INPUT: ",
                   "The agent: {} is not an EpisodicAgent.".format(ag))
    else:
        variables.input_list.update({agent: activation})
        agent.level_of_activation = activation
        if agent not in variables.target_agents:
            variables.target_agents = variables.target_agents + [agent]
        related = collect_all_relational_interconnected(agent)
        if related:
            for rel in related:
                variables.input_list.update({rel: activation})
                rel.level_of_activation = activation
                # Adds all related agents in target_list.
                if rel not in variables.target_agents:
                    variables.target_agents = variables.target_agents + [rel]

                                                                                                      
def remove_from_input(ag):
    agent = find_agent(ag)
    if agent in variables.input_list.keys():
        variables.input_list.pop(agent)
    else:
        dual_raise("REMOVE_FROM_INPUT: ",
                   "The agent: '{}', is not in the INPUT_LIST.".format(ag))


def add_to_goal(ag, activation=1.00):
    # Adds AG(agent) to GOAL_LIST or updates AG's activation.
    agent = find_agent(ag)
    if not (isinstance(agent, DualAgent)):
        dual_raise("ADD_TO_GOAL: ",
                   "The agent: {} is not a DualAgent.".format(ag))
    else:
        variables.goal_list.update({agent: activation})
        agent.level_of_activation = activation
        if isinstance(agent, RelationInstanceAgent):
            for arg in agent.arguments:
                variables.goal_list.update({arg: activation})
                arg.level_of_activation = activation

        
def remove_from_goal(ag):
    agent = find_agent(ag)
    if agent in variables.goal_list.keys():
        variables.goal_list.pop(agent)
    else:
        dual_raise("REMOVE_FROM_GOAL: ",
                   "The agent: '{}' is not in the GOAL_LIST.".format(ag))


def update_input_goal():
    # If an agent has been added to INPUT or GOAL on the previous cycle, remove it from STM and not_in_STM.
    for agent in variables.input_list.keys():
        if agent in variables.short_term_memory:
            variables.short_term_memory.remove(agent)
        if agent in variables.agents_not_in_STM:
            variables.agents_not_in_STM.remove(agent)
    for agent in variables.goal_list.keys():
        if agent in variables.short_term_memory:
            variables.short_term_memory.remove(agent)
        if agent in variables.agents_not_in_STM:
            variables.agents_not_in_STM.remove(agent)
    variables.working_memory = variables.short_term_memory + list(variables.input_list.keys()) + list(variables.goal_list.keys())

# Activation functions #
########################


def total_activation():
    total = 0.0
    for ag in variables.all_agents.values():
        total = total + ag.level_of_activation
    return total


def activation_function(old_activation, new_input, threshold, speed):
    return linear_decay_input(old_activation, new_input, threshold, speed)


def linear_decay_input(old_activation, new_input, threshold, speed):
    new_activation = decay_rate * (old_activation_rate * old_activation + new_activation_rate * new_input) + speed*strength_of_increase
    if new_activation < 0.0:
        new_activation = 0.01  # Otherwise it will never be able to get activated again.
    return new_activation


def linear_decay_input_threshold(old_activation, new_input, threshold, speed):
    new_activation = linear_decay_input(old_activation, new_input, threshold, speed)
    if new_activation > threshold:
        return new_activation
    else:
        return 0.1


def update_incoming_activation():
    for agent in variables.all_agents.values():
        agent.input_activation = calculate_input(agent)  # Calculates the input activations.
    for inp in variables.input_list:
        inp.input_activation = inp.input_activation + input_node_activation*variables.input_list.get(inp)
    for inp in variables.goal_list:
        inp.input_activation = inp.input_activation + goal_node_activation*variables.goal_list.get(inp)


def update_activations():
    for agent in variables.all_agents.values():
        new_activation = update_activation(agent, agent.input_activation)  # Updates activation level.
        agent.speed_of_change = new_activation - agent.level_of_activation  # Calculates the speed of activation change.
        if agent in variables.deactivated_agents:
            pass
        else:
            agent.level_of_activation = new_activation  # Sets the new activation.


def calculate_input(agent):
    input_activation = 0.0
    for link in agent.incoming_links:
        input_activation = input_activation + link.sender.level_of_activation * link.weight
    return input_activation


def update_activation(agent, input_activation, function=activation_function):
    return function(agent.level_of_activation, input_activation, agent.threshold, agent.speed_of_change)


# TO DO:
def change_weights_and_thresholds():
    pass  

# def calculate_current_focus_strength (current_focus):
#    return (linear_focus (current_focus.level_of_activation, current_focus.speed_of_change) + resistance_of_old_focus)


def add_noise_in_all_activations(variance):
    for agent in variables.all_agents.values():
        agent.level_of_activation = agent.level_of_activation + gauss(0.00, variance)
        if agent.level_of_activation < 0.00:
            agent.level_of_activation = 0.01

# END OF FILE ACTIVATION.PY #
