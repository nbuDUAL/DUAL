from main_cycle import *

add_agent("dog", agent_type = ConceptAgent)
add_agent("leg", agent_type = ConceptAgent)
add_agent("mouth", agent_type = ConceptAgent)
add_agent("tail", agent_type = ConceptAgent)



def generate_instances(number_of_instances, start_number, base_name, inst_of, has_parts = []):
    if type (number_of_instances) != int:
        dual_raise("Generate_instances: ",
                   "'{}' is not an integer number.".format(number_of_instances))
    if type (start_number) != int:
        dual_raise("Generate_instances: ",
                   "'{}' is not an integer number.".format(start_number))
    if type (base_name) != str:
        dual_raise("Generate_instances: ",
                   "'{}' is not a string.".format(base_name))
    if not isinstance (find_agent(inst_of), ConceptAgent):
        dual_raise("Generate_instances: ",
                   "'{}' is not a Concept Agent.".format(inst_of))
    for part in has_parts:
        if not isinstance(find_agent(part), ConceptAgent):
            dual_raise("Generate_instances: ",
                       "The part: '{}' you want to instantiate is not a Concept Agent.".format(part))
    instan_of = find_agent(inst_of)
    for i in range(number_of_instances):
        name = str(base_name) + "_" + str(start_number+i+1)
        parts = []
        for part in has_parts:
            part_name = str(part) + "_" + str(start_number+i+1)
            current_part = add_agent(part_name, agent_type = InstanceAgent, instance_of = [find_agent(part)])
            parts = parts + [current_part]
        add_agent(name, agent_type = InstanceAgent, instance_of = [instan_of], has_parts = parts) 
    

# generate_instances(100, 0, "dog", "dog", has_parts = [find_agent("mouth"), find_agent("leg"), find_agent("tail")])
