
##################
# SIMULATION 1_3 #
##################

# DEFINES Simulation 1.3. Recognition of a role-governed category in a large data base.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last update: Yolina Petrova, October, 2018

"""
             ________                         
            | animal |
            |________|
              /      \                   
             /        \
            /          \
     ______/___      ___\__
    | domestic |    | bird |
    |  animal  |    |______|        
    |__________|     /                                      
          \         /
           \       /
            \     /
            _\___/___
           | chicken |
           |_________|
           /
          /      
   ______/____                
  | chicken_1 |
  |___________|      



Because of the constraint satisfaction mechanism,
a new "domestic animal" is recognized out of 100 similar bases.

"""

# Imports the whole DUAL architecture/model (without any previous knowledge).
from main_cycle import *

# Example for running a single simulation:
# run_sim_1_3(0.05, 0.05, 100, 20)


def re_initialize():
    initialize_dual()
    for ag in variables.all_agents.values():
        del ag
    variables.all_agents = {}
    add_agent("living_thing", agent_type=ConceptAgent)
    add_agent("animal", agent_type=ConceptAgent, superclasses=[find_agent("living_thing")])
    add_agent("mammal", agent_type=ConceptAgent, superclasses=[find_agent("animal")])
    add_agent("bird", agent_type=ConceptAgent, superclasses=[find_agent("animal")])
    add_agent("reptile", agent_type=ConceptAgent, superclasses=[find_agent("animal")])

    add_agent("pig", agent_type=ConceptAgent, superclasses=[find_agent("mammal")])
    add_agent("cow", agent_type=ConceptAgent, superclasses=[find_agent("mammal")])
    add_agent("horse", agent_type=ConceptAgent, superclasses=[find_agent("mammal")])
    add_agent("chicken", agent_type=ConceptAgent, superclasses=[find_agent("bird")])
    add_agent("lizard", agent_type=ConceptAgent, superclasses=[find_agent("reptile")])

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


def create_kb(variance_links, variance_agents, n_bases):
    # N_SIMULATIONS should be integer. It refers to the desired number of separate simulations.
    re_initialize()
    for i in range(n_bases):
        name_role1 = "grandmother_" + str(i)
        role1 = add_agent(name_role1, agent_type=InstanceAgent, instance_of=[find_agent("grandmother")])
        if i % 4 == 0:
            name_role2 = "chicken_" + str(i)
            role2 = add_agent(name_role2, agent_type=InstanceAgent, instance_of=[find_agent("chicken")])
        elif i % 4 == 1:
            name_role2 = "pig_" + str(i)
            role2 = add_agent(name_role2, agent_type=InstanceAgent, instance_of=[find_agent("pig")])
        elif i % 4 == 2:
            name_role2 = "cow_" + str(i)
            role2 = add_agent(name_role2, agent_type=InstanceAgent, instance_of=[find_agent("cow")])
        else:
            name_role2 = "lizard_" + str(i)
            role2 = add_agent(name_role2, agent_type=InstanceAgent, instance_of=[find_agent("lizard")])
        name_rel = "feeds_" + str(i)
        add_agent(name_rel, agent_type=RelationInstanceAgent, arity=2,
                  arguments=[role1, role2], instance_of=[find_agent("feeds")])
    # TARGET
    add_agent("grandmother_t", agent_type=InstanceAgent, instance_of=[find_agent("grandmother")])
    add_agent("horse_t", agent_type=InstanceAgent, instance_of=[find_agent("horse")])
    add_agent("feeds_t", agent_type=RelationInstanceAgent, arity=2,
              arguments=[find_agent("grandmother_t"), find_agent("horse_t")],
              instance_of=[find_agent("feeds")])
    # Initializes weights
    for c in variables.all_agents.values():
        if isinstance(c, SemanticAgent):
            normalize_instance_links(c, variance_links)
    add_noise_in_all_links(0.25)
    add_noise_in_all_activations(variance_agents)
    add_to_input(find_agent("feeds_t"))

create_kb(0.05, 0.05, 100)


def run_sim_1_3(variance_links, variance_agents, n_bases, n_cycles):
    # N_BASES should be integer. It refers to the desired number of instance situations.
    # N_CYCLES should be integer. It refers to the desired number of cycles to run in a single simulation.
    create_kb(variance_links, variance_agents, n_bases)
    cycles(n_cycles)


def run_sim_1_3_n_times(n_simulations, variance_links, variance_agents):
    # N_SIMULATIONS should be integer. It refers to the desired number of separate simulations.
    variables.user_interaction = False
    variables.verbose = False
    file = open("results_1_3.dat", "w")
    file.write("number@variance_links@variance_agents@dual_time@total_activation@\n")
    for i in range(n_simulations):
        create_kb(variance_links, variance_agents, 100)
        name = "D:/Georgi/categorization_DUAL/weights/weights_" + str(i) + ".dat"
        file_weights = open(name, "w")
        for ag in variables.all_agents.values():
            if isinstance(ag, SemanticAgent):
                links = ""
                for inst in ag.instances:
                    for l in inst.incoming_links:
                        if l.sender == ag:
                            links = links + inst.name + " " + str(l.weight) + " !   "
                file_weights.write("{}   {}   {}".format(ag.name, ag.level_of_activation, links))
        file_weights.close()
        try:
            cycles(20)
            while variables.list_of_mappings or (variables.dual_time == 1000):
                cycles(1)
            for new in variables.just_created:
                new_list = ""
                new_list = new_list + new.name + "#@" + new.comment + "@"
                new_list = new_list.replace("grandmother_t_", "")
                new_list = new_list.replace("horse_t_", "")
                new_list = new_list.replace("feeds_t_", "")
                new_list = new_list.replace("_1_1#", "")
                new_list = new_list.replace("_1_2#", "")
                new_list = new_list.replace("_1#", "")
                new_list = new_list.replace("Created by: ", "")
                new_list = new_list.replace(" in dual time: ", "@")
                new_list = new_list.replace(" (which was Created by ", "@")
                new_list = new_list.replace(" in time ", "@")
                new_list = new_list.replace(").", "")
                new_list = new_list.replace("Created new situation by ", "")
                new_list = new_list.replace("Created new instance situation by ", "")
                new_list = new_list.replace("Created new base instance situation by ", "")
                new_list = new_list.replace("grandmother_", "grandmother@")
                new_list = new_list.replace("feeds_", "feeds@")
                new_list = new_list.replace("cow_", "cow@")
                new_list = new_list.replace("lizard_", "lizard@")
                new_list = new_list.replace("pig_", "pig@")
                new_list = new_list.replace("chicken_", "chicken@")

                time_str = str(variables.dual_time)
                time_str = time_str.replace(".", ",")

                var1_str = str(variance_links)
                var1_str = var1_str.replace(".", ",")

                var2_str = str(variance_agents)
                var2_str = var2_str.replace(".", ",")
             
                file.write("{}@{}@{}@{}@{}@{}\n".format(i, var1_str, var2_str, time_str,
                                                        str(total_activation()), new_list))
            print("END OF SIMULATION NUMBER {}".format(i))
        except Exception:
            pass
    file.close()

# END of file: simulation_1_3.py #
