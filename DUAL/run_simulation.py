
##################
# RUN SIMULATION #
##################

# DEFINES THE NECESSARY CONDITIONS FOR RUNNING A SIMULATION.
# PROGRAMERS: Yolina Petrova, YEAR 2018
# Last update: Yolina Petrova, October, 2018

#####################
# External protocol #
#####################

"""
* initialize_kb(knowledge_base)
--> KNOWLEDGE BASE should be string expressing the name of a python file
(without the extension '.py' containing the wanted knowledge).

* run_simulation(knowledge_base, target, n_cycles,
                 l_variance=0.0, a_variance=0.0)
--> KNOWLEDGE BASE should be string expressing the name of a python file
(without the extension '.py' containing the wanted knowledge).
TARGET should be a string of an agent in the KB.
L_VARIANCE (links' weight variance) and A_VARIANCE (agents' level of activation variance) are not mandatory.
If provided, they should be of type float.

* run_simulation_n_times(knowledge_base, target, n_cycles, n_times,
                         l_variance=0.0, a_variance=0.0):
--> KNOWLEDGE BASE should be string expressing the name of a python file
(without the extension '.py' containing the wanted knowledge).
TARGET should be a string of an agent in the KB.
N_TIMES refers to the number of times for performing the simulation.
L_VARIANCE (links' weight variance) and A_VARIANCE (agents' level of activation variance) are not mandatory.
If provided, they should be of type float.

* run_cont_simulation_n_times(knowledge_base_1, target_1, knowledge_base_2, target_2,
                              n_cycles, n_times, l_variance=0.0, a_variance=0.0):
--> KNOWLEDGE BASE should be string expressing the name of a python file
(without the extension '.py' containing the wanted knowledge).
TARGET should be a string of an agent in the KB.
N_TIMES refers to the number of times for performing the simulation.
L_VARIANCE (links' weight variance) and A_VARIANCE (agents' level of activation variance) are not mandatory.
If provided, they should be of type float.

* save_sim_to_file(sim=1, sim_number=1, custom_header, file_name)
--> The function saves all newly created agents from variables.just_created in a file with name FILE_NAME.
SIM refers to the number of simulation if there is more than 1 simulations
(i.e. simulation_1_2 which is built on top of simulation_1_1).
SIM_NUMBER is included for the cases in which the simulation is repeated several times in a row).

"""

# Imports the whole DUAL architecture/model (without any previous knowledge).
from main_cycle import *

# EXAMPLE runs:
"""
run_simulation("simulation_1_1_role_governed", "feeds_2", 20, base=0)
run_simulation_n_times("simulation_1_1_role_governed", "feeds_2", 20, 2)

run_cont_simulation_n_times("simulation_1_2_simple_recognition", "feeds_2",
                            "simulation_1_2_simple_recognition", "feeds_3",
                            20, 1, base_1=1, base_2=2)

run_simulation("simulation_1_1_role_governed_higher_order", "causes_2", 20, base=1)
run_simulation("simulation_1_1_role_governed_higher_order", "causes_3", 1, base=2)

run_simulation("simulation_1_4_cross_mapping", "left_of_2", 6)

run_cont_simulation_n_times("simulation_2_1_same_situations", "feeds_2",
                            "simulation_2_1_same_situations", "feeds_3",
                            20, 1, base_1=1, base_2=2)

run_simulation("simulation_2_2_diff_Bases_same_Target", "milks_2", 20, base=1)
run_simulation("simulation_2_2_diff_Bases_same_Target", "feeds_3", 1, base=2)
run_cont_simulation_n_times("simulation_2_2_diff_Bases_same_Target", "milks_2",
                            "simulation_2_2_diff_Bases_same_Target", "feeds_3",
                            20, 1, base_1=1, base_2=2)

run_simulation("simulation_2_3_diff_Bases_mixed_Target", "milks_2", 20, base=1)
run_simulation("simulation_2_3_diff_Bases_mixed_Target", "feeds_3", 1, base=2)

run_simulation("simulation_2_4_diff_Base_new_Target", "milks_2", 20, base=1)
run_simulation("simulation_2_4_diff_Base_new_Target", "cuts_3", 1, base=2)
                            
"""


def initialize_kb(knowledge_base, base=0):
    # KNOWLEDGE BASE should be string expressing the name of a python file
    # (without the extension '.py' containing the wanted knowledge).
    if base == 0:
        module = __import__(knowledge_base, fromlist=["load_kb"])
        module.load_kb()
    elif base == 1:
        module = __import__(knowledge_base, fromlist=["load_kb_1"])
        module.load_kb_1()
    elif base == 2:
        module = __import__(knowledge_base, fromlist=["load_kb_2"])
        module.load_kb_2()
    else:
        dual_raise("initialize_kb",
                   "Unrecognized base type: '{}'.".format(base))


def run_simulation(knowledge_base, target, n_cycles, base=0, 
                   l_variance=0.0, a_variance=0.0):
    # KNOWLEDGE BASE should be string expressing the name of a python file
    # (without the extension '.py' containing the wanted knowledge).
    # TARGET should be a string of an agent in the KB.
    # L_VARIANCE (links' weight variance) and A_VARIANCE (agents' level of activation variance) are not mandatory.
    # If provided, they should be of type float.
    initialize_dual()
    initialize_kb(knowledge_base, base)
    if target:
        add_to_input(find_agent(target))
    if l_variance != 0.0:
        add_noise_in_all_links(l_variance)
    if a_variance != 0.0:
        add_noise_in_all_activations(a_variance)
    cycles(n_cycles)


def run_simulation_n_times(knowledge_base, target, n_cycles, n_times,
                           base=0, l_variance=0.0, a_variance=0.0):
    # KNOWLEDGE BASE should be string expressing the name of a python file
    # (without the extension '.py' containing the wanted knowledge).
    # TARGET should be a string of an agent in the KB.
    # N_TIMES refers to the number of times for performing the simulation.
    # L_VARIANCE (links' weight variance) and A_VARIANCE (agents' level of activation variance) are not mandatory.
    # If provided, they should be of type float.
    variables.user_interaction = False
    custom_header = True
    file_name = "{}_results.csv".format(knowledge_base)
    for i in range(n_times):
        re_initialize_dual()
        run_simulation(knowledge_base, target, n_cycles, base, l_variance, a_variance)
        for new_agent in variables.just_created:
            superclasses = collect_agents_from_slot(new_agent, "superclasses")
            subclasses = collect_agents_from_slot(new_agent, "subclasses")
            instances = collect_agents_from_slot(new_agent, "instances")
            instance_of = collect_agents_from_slot(new_agent, "instance_of")
            mappings = collect_agents_from_slot(new_agent, "mappings")
            arguments = collect_agents_from_slot(new_agent, "arguments")
            save = {'sim_number': i, 'name': new_agent.name,
                    'agent_type': type(new_agent).__name__, 'comment': new_agent.comment,
                    'level_of_activation': new_agent.level_of_activation,
                    'argument_of': [new_agent.argument_of], 'part_of': [new_agent.part_of],
                    'has_parts': [new_agent.has_parts], 'superclasses': [superclasses],
                    'subclasses': [subclasses], 'instances': [instances], 'instance_of': [instance_of],
                    'mappings': [mappings], 'arguments': [arguments]}
            df = pandas.DataFrame(save, columns=['sim_number', 'name', 'agent_type', 'comment',
                                                 'level_of_activation', 'argument_of', 'part_of',
                                                 'has_parts', 'superclasses', 'subclasses', 'instances',
                                                 'instance_of', 'mappings', 'arguments'])

            # Appends AGENT to the existing file with FILE_NAME.
            with open(file_name, 'a') as file:
                df.to_csv(file, header=custom_header)
            # custom_header = False so the columns' names will not be appended again;
            custom_header = False
        print("END OF SIMULATION NUMBER {}.".format(i))


def run_cont_simulation_n_times(knowledge_base_1, target_1, knowledge_base_2, target_2, n_cycles,
                                n_times, base_1=1, base_2=2, l_variance=0.0, a_variance=0.0):
    # KNOWLEDGE BASE should be string expressing the name of a python file
    # (without the extension '.py' containing the wanted knowledge).
    # TARGET should be a string of an agent in the KB.
    # N_TIMES refers to the number of times for performing the simulation.
    # L_VARIANCE (links' weight variance) and A_VARIANCE (agents' level of activation variance) are not mandatory.
    # If provided, they should be of type float.
    variables.user_interaction = False
    custom_header = True
    file_name = "{}_results.csv".format(knowledge_base_2)
    for i in range(n_times):
        re_initialize_dual()
        run_simulation(knowledge_base_1, target_1, n_cycles, base_1, l_variance, a_variance)
        print("JUST: ", variables.just_created)
        save_sim_to_file(sim=1, sim_number=i, custom_header=custom_header, file_name=file_name)
        # initialize_dual() - run_simulation() already does it.
        custom_header = False
        run_simulation(knowledge_base_2, target_2, n_cycles, base_2, l_variance, a_variance)
        save_sim_to_file(sim=2, sim_number=i, custom_header=False, file_name=file_name)
        print("END OF SIMULATION NUMBER {}.".format(i))


def save_sim_to_file(sim=1, sim_number=1, custom_header=True, file_name="results.csv"):
    # The function saves all newly created agents from variables.just_created in a file with name FILE_NAME.
    # SIM refers to the number of simulation if there is more than 1 simulations
    # (i.e. simulation_1_2 which is built on top of simulation_1_1).
    # SIM_NUMBER is included for the cases in which the simulation is repeated several times in a row).
    for new_agent in variables.just_created:
            superclasses = collect_agents_from_slot(new_agent, "superclasses")
            subclasses = collect_agents_from_slot(new_agent, "subclasses")
            instances = collect_agents_from_slot(new_agent, "instances")
            instance_of = collect_agents_from_slot(new_agent, "instance_of")
            mappings = collect_agents_from_slot(new_agent, "mappings")
            arguments = collect_agents_from_slot(new_agent, "arguments")
            save = {'sim': sim, 'sim_number': sim_number, 'name': new_agent.name,
                    'agent_type': type(new_agent).__name__, 'comment': new_agent.comment,
                    'level_of_activation': new_agent.level_of_activation,
                    'argument_of': [new_agent.argument_of], 'part_of': [new_agent.part_of],
                    'has_parts': [new_agent.has_parts], 'superclasses': [superclasses],
                    'subclasses': [subclasses], 'instances': [instances], 'instance_of': [instance_of],
                    'mappings': [mappings], 'arguments': [arguments]}
            df = pandas.DataFrame(save, columns=['sim', 'sim_number', 'name', 'agent_type', 'comment',
                                                 'level_of_activation', 'argument_of', 'part_of',
                                                 'has_parts', 'superclasses', 'subclasses', 'instances',
                                                 'instance_of', 'mappings', 'arguments'])

            # Appends AGENT to the existing file with FILE_NAME.
            with open(file_name, 'a') as file:
                df.to_csv(file, header=custom_header)
            # custom_header = False so the columns' names will not be appended again;
            custom_header = False

# END of file run_simulation.py #
