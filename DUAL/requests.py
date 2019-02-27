
############
# REQUESTS #
############

# DEFINES FUNCTIONS FOR CREATION, REMOVAL AND MANIPULATION OF REQUESTS.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018

# TO DO: Make the eliminate_duplicate_mappings() BETTER.
# TO DO: MAKE THE MAKE_REQUESTS... FUNCTION BETTER.
# TO DO: ELIMINATE THE UNNECESSARY SLOTS FOR ALL REQUESTS
# --> SOME AGENTS_TO_ACTIVATE, ETC. - THEY WILL BE INITIALIZED DURING CREATION OF THE AGENT
# TO DO: THINK ABOUT JUSTIFICATIONS AND SUPERCLASS - IF CAT_1 AND DOG_1 ARE MAPPED BECAUSE ANIMAL GETS INTO THE WM,
# TO DO: eliminate_duplicate_relational_anticipations() function
# TO DO: Think about the check_relation_anticipation() function.
# TO DO: Think about remove_anticipations() function - is it needed?

"""
* request_type_from_agent_type (agent_type) --> Returns the corresponding request_type for the AGENT_TYPE.

# Making requests functions #
#############################

* make_request_for_mapping (justification, target_entity, base_entity, comment)
--> A generic function that constructs a request for a mapping on the basis of the potential agents that could be mapped
and the reason for their correspondence.
Returns MappingRequest with the specified arguments: JUSTIFICATION, TARGET_ENTITY, etc.
If a request with the same structure already exists, returns [].

* make_instance_request (justification, base_entity, target_entity)
--> Returns InstanceAnticipationRequest with the specified arguments: JUSTIFICATION, TARGET_ENTITY, etc.

* make_request_for_grouping (intersection, target1, target2) --> TO BE PROGRAMED.

* make_request_for_argument_anticipation (target_entity, base_entity) --> TO BE PROGRAMED.

* make_request_for_anticipations (base_argument, target_agent) --> TO BE PROGRAMED.

# Handling the requests functions #
###################################

When a mapping is created by the marker-passing mechanism, the justification field contains a reference
to the marker-intersection node. When an anticipation is created by the structure-correspondence mechanism,
the justification field contains a reference to the superordinate mapping.
There may be more than one justifications (e.g. two marker intersections and a superordinate hypothesis).
In this case, the justification field contains both. The connectionist aspect of the mapping agent sends (and receives)
excitatory activation to all justification agents.

* check_and_exchange_superclasses_in_requests(request, concept)
--> Look the function 'check_and_exchange_superclasses' in agent_manipulations.py
Checks whether CONCEPT is above or bellow MAPPING through the hierarchy and adds slots if necessary.

* eliminate_duplicate_mappings(requests_for_mappings)
--> TO BE DONE - UPDATE!!!
In addition to the deletion of the duplicate mappings, it should create new links where necessary!

* eliminate_duplicate_instance_anticipations(requests_for_instance_anticipations)
--> The function eliminates the requests for anticipations which already exist and transfers any lacking information.

* eliminate_duplicate_relational_anticipations(requests_for_relation_anticipations) --> TO DO!!!

* handle_the_list_of_requests(list_reqs) --> The function divides the requests in the LIST_REQS list by type
and sends them for further handling to the appropriate for their type functions.

* handle_the_list_of_instances_requests(new_instances):
--> The function creates new UnrealInstanceAgent on the bases of all InstanceAnticipationRequest
that are in the NEW_INSTANCES list.

* handle_the_list_of_relation_requests(new_relation_instances)
--> The function creates new UnrealRelationInstanceAgents on the bases of all RelationInstanceAnticipationRequests
that are in the NEW_RELATION_INSTANCES list.

* inhibit_competitory_mappings(agent) --> the function creates inhibitory links between AGENT which is a MappingAgent
and all of its competing mappings.

* handle_the_list_of_mapping_requests(new_mappings)

# Functions dealing with anticipations #
########################################

* check_common_part_of_concept(mapping) --> For each whole of the base element of the MAPPING checks
whether there is a corresponding whole of the target element. Returns a list of all necessary anticipation requests.

* handle_anticipation_for_relational_mapping (mapping, to_be_anticipated, relation)
--> If MAPPING is relational mapping, the TO_BE_ANTICIPATED RELATION's arguments are checked if they already
exist as request or anticipations. If they do, new links are added between RELATION
and the duplicate and the function returns [].
Otherwise, the function returns a list of instance requests for the missing arguments.

* handle_anticipation_for_instance_mapping (mapping, to_be_anticipated, instance) --> See above, but for INSTANCE.
Checks for consistencies and returns requests if the mapped element is an instance.

* check_relation_anticipation(relation) --> TO BE PROGRAMED.
If there is a relation without corresponding one, check if its arguments are all mapped to something in the target.
For now, we think that the function needs only the RELATION as an argument.

* inhibit_competing_anticipations(agent)
--> Bidirectional inhibition links are created between all contradicting to AGENT anticipations and AGENT.

* remove_anticipations() --> To be programed

# OTHER #
#########

* collect_all_relational_interconnected (agent)
--> Returns a list of all agents that have a path through argument -- argument_of links with the AGENT.

* collect_all_agents_with_a_common_structure(request)
--> Returns a list of all AnticipationAgents that share the same structure as REQUEST.
"""

from agents_manipulation import *


def request_type_from_agent_type(agent_type):
    if agent_type == InstanceAgent:
        return InstanceAnticipationRequest
    elif agent_type == MappingAgent:
        return MappingRequest
    elif agent_type == RelationInstanceAgent:
        return RelationInstanceAnticipationRequest
    else:
        dual_raise("Request_type_from_agent_type: ",
                   "Unrecognized agent_type: '{}'.".format(agent_type))


# Making requests functions #
#############################

def make_request_for_mapping(superclass, justifications, target_entity, base_entity, comment):
    
    name = gen_name_mapping(target_entity.name, base_entity.name)
    agents_to_activate = []
    incoming_links = []
    threshold = default_mapping_threshold
    # The level_of_activation will be calculated as the mean activation of:
    # the three agents: the superclass, target_instance and the base_instance
    level_of_activation = default_initial_mapping_activation
    speed_of_change = 0.0
    justifications = justifications
    target_instance = [target_entity]
    base_instance = [base_entity]
    superclasses = [superclass]
    for r in variables.list_of_all_requests:
        if r.name == name:
            dual_raise("make_request_for_mapping",
                       "Why '{}' hasn't been discarded as a duplicate?".format(r.name))
    return [(MappingRequest(name, comment, agents_to_activate,
                            incoming_links, threshold, level_of_activation, speed_of_change,
                            superclasses=superclasses, target_instance=target_instance,
                            base_instance=base_instance, justifications=justifications))]


def make_instance_request(just, base_entity, target_entity):
    name = gen_name_anticipation(base_entity.name)
    justifications = [just]
    instance_of = [base_entity.instance_of]
    has_parts = [target_entity] 
    threshold = default_instance_anticipation_threshold
    level_of_activation = default_initial_anticipation_activation
    speed_of_change = 0.0
    comment = "Created as anticipation by: {} for {} in dual time: {}.".format(base_entity, target_entity, variables.dual_time)
    situations = base_entity.situations
    for r in variables.list_of_all_requests:
        if r.name == name:
            dual_raise("make_instance_request",
                       "Why '{}' hasn't been discarded as a duplicate?".format(r.name))
    return [(InstanceAnticipationRequest(name, comment=comment, threshold=threshold,
                                         level_of_activation=level_of_activation,
                                         speed_of_change=speed_of_change, has_parts=has_parts, situations=situations,
                                         instance_of=instance_of, justifications=justifications))]

# TO DO!!!


def make_relation_instance_request(mapping, b_whole, mapping_target_instance):
    make_instance_request(mapping, b_whole, mapping_target_instance)  # TO DO!!!


def make_request_for_grouping(intersection, target1, target2):
    # Looks for a group between two targets and if not, creates one
    return []
    pass


def make_request_for_argument_anticipation(target_entity, base_entity):
    # TO DO: For now it is not very clear.
    return []
    pass


def make_request_for_anticipations(base_argument, target_agent):
    print("WELCOME IN MAKE_REQUEST_FOR_ANTICIPATION: {}, {}!".format(base_argument, target_agent))
    # Launch anticipations of BASE_ARGUMENT, being part_of TARGET_AGENT
    return []
    pass

# Handling the requests functions #
###################################


def check_and_exchange_superclasses_in_requests(request, concept):
    # Look the function 'check_and_exchange_superclasses' in agent_manipulations.py
    # Checks whether CONCEPT is above or bellow MAPPING through the hierarchy and adds slots if necessary.
    for superc in request.superclasses:
        if superc in collect_all_active_superclasses(concept):  # CONCEPT is somewhere bellow MAPPING
            request.superclasses = [x for x in request.superclasses if x != superc]
    flag = True
    for superc in request.superclasses:
        if superc in collect_all_active_subclasses(concept):  # CONCEPT is somewhere above MAPPING.
            flag = False  # It should not do anything!
    if flag:
        if concept not in request.superclasses:
            request.superclasses = request.superclasses + [concept]


def eliminate_duplicate_mappings(requests_for_mappings):
    mapping_requests = []
    for r in requests_for_mappings:
        flag = True
        for target_mapp in r.target_instance[0].mappings:
            if target_mapp.base_instance[0] == r.base_instance[0]:
                # A duplicate is found.
                flag = False
                check_and_exchange_superclasses(target_mapp, r.superclasses[0])
                for just in r.justifications:
                    add_in_slot(target_mapp, "justifications", just)
        for request in mapping_requests:
            if (r.target_instance[0] == request.target_instance[0]) and (r.base_instance[0] == request.base_instance[0]):
                # Duplicate mapping found.
                flag = False
                check_and_exchange_superclasses_in_requests(request, r.superclasses[0])
                for just in r.justifications:
                    if just not in request.justifications:
                        request.justifications = request.justifications + [just]
        if flag:
            mapping_requests = mapping_requests + [r]
        else:
            variables.list_of_all_requests.remove(r)
    return mapping_requests


def eliminate_duplicate_instance_anticipations(requests_for_instance_anticipations):
    instance_requests = []
    for r in requests_for_instance_anticipations:
        flag = True
        connected_parts = []
        for part in r.has_parts:
            connected_parts = connected_parts + collect_all_relational_interconnected(part)
        connected_parts = list(set(connected_parts))
        for others in connected_parts:
            for whole_part in others.part_of:
                if r.instance_of[0][0] in whole_part.instance_of:  # A duplicate is found!
                    flag = False
                    for p in r.has_parts:
                        add_in_slot(p, "part_of", whole_part)
                        if isinstance(whole_part, UnrealAgent):
                            for just in r.justifications:
                                add_in_slot(whole_part, "justifications", just)
            for old_req in instance_requests:
                if (r.instance_of[0][0] == old_req.instance_of[0][0]) and (others in old_req.has_parts):
                    flag = False
                    old_req.has_parts = list(set(old_req.has_parts + r.has_parts))
                    old_req.justifications = list(set(old_req.justifications + r.justifications))
        if flag:
            instance_requests = instance_requests + [r]
        else:
            variables.list_of_all_requests.remove(r)
    return instance_requests


# TO DO!!!
def eliminate_duplicate_relational_anticipations(requests_for_relation_anticipations):
    return eliminate_duplicate_instance_anticipations(requests_for_relation_anticipations)  # TO DO!!!


def handle_the_list_of_requests(list_reqs):
    new_mappings = []
    new_relational_instances = []
    new_instances = []
    for r in list_reqs:
        if isinstance(r, MappingRequest):
            new_mappings = new_mappings + [r]
        elif isinstance(r, RelationInstanceAnticipationRequest):
            new_relational_instances = new_relational_instances + [r]
        elif isinstance(r, InstanceAnticipationRequest):
            new_instances = new_instances + [r]
        else:
            dual_raise("handle_the_list_of_requests",
                       "Unrecognized request type: {}". format(r.name))
    # Deals with the Mapping requests.
    mappings_requests = eliminate_duplicate_mappings(new_mappings)
    handle_the_list_of_mapping_requests(mappings_requests)
    # Deals with the RelationInstancesRequests.
    relational_anticip_requests = eliminate_duplicate_relational_anticipations(new_relational_instances)
    handle_the_list_of_relation_requests(relational_anticip_requests)
    # Deals with the InstancesRequests.
    instance_anticipation_requests = eliminate_duplicate_instance_anticipations(new_instances)
    handle_the_list_of_instances_requests(instance_anticipation_requests)


def handle_the_list_of_instances_requests(new_instances):

    for r in new_instances:
        if isinstance(r, InstanceAnticipationRequest):
            flag = True
            anticipation = collect_all_agents_with_a_common_structure(r)
            if anticipation:
                flag = False
                # An additional excitatory link coming from the current mapping justification is added.
                # TO DO: keep track on the cases when we have anticipated "cat_1" and "cat_3" for example,
                # if it combines them ot not.
                create_link(r.has_parts[0], anticipation[0], default_part_of_weight)
                create_link(anticipation[0], r.has_parts[0], default_has_part_weight)
                anticipation[0].has_parts = anticipation[0].has_parts + [r.has_parts[0]]
                r.has_parts[0].part_of = r.has_parts[0].part_of + [anticipation[0]]
                anticipation[0].justifications = anticipation[0].justifications + r.justifications
                for just in r.justifications:
                    create_link(just, anticipation[0], default_justification_weight)
            # TO DO: THINK ABOUT THE HAS_PARTS. SHOULD WE ANTICIPATE THEM AS WELL OR?
            if flag:
                for agent in variables.all_agents.values():
                    if agent == get_agent(r.name):
                        print("Why didn't we find an existing anticipation,",
                              "even though there is one with identical name: '{}'?".format(r.name))
                new_agent = add_agent(r.name, agent_type=UnrealInstanceAgent, comment=r.comment,
                                      agents_to_activate=r.agents_to_activate, incoming_links=r.incoming_links,
                                      threshold=r.threshold, level_of_activation=r.level_of_activation,
                                      speed_of_change=r.speed_of_change, argument_of=r.argument_of,
                                      part_of=r.part_of, has_parts=r.has_parts,
                                      situations=r.situations, instance_of=r.instance_of[0],
                                      mappings=r.mappings, justifications=r.justifications)
                inhibit_competing_anticipations(new_agent)
                # Sets the link from the concept to the anticipation at parameter "default_class_anticipation_weight".
                create_link(new_agent.instance_of[0], new_agent,
                            default_class_anticipation_weight)
                # Sets the link from the anticipation to its justifications
                # at parameter "default_anticipation_mapping_just_weight".
                for j in new_agent.justifications:
                    create_link(new_agent, j, default_anticipation_mapping_just_weight)
                variables.target_agents = variables.target_agents + [new_agent]
            variables.list_of_all_requests.remove(r)
            

def handle_the_list_of_relation_requests(new_relation_instances):
    for r in new_relation_instances:
        if isinstance(r, RelationInstanceAnticipationRequest):
            flag = True
            for agent in variables.all_agents.values():
                if agent == get_agent(r.name):
                    flag = False
                    # An additional excitatory link coming from the current mapping justification is added.
                    create_link(r.has_parts[0], agent, default_justification_weight)
                    create_link(agent, r.has_parts[0], default_justification_weight)
                    agent.has_parts = agent.has_parts + [r.has_parts[0]]
                    r.has_parts[0].part_of = r.has_parts[0].part_of + [agent]
                    agent.justifications = agent.justifications + r.justifications
                    for just in r.justifications:
                        create_link(just, agent, default_justification_weight)
            if flag:
                new_agent = add_agent(r.name, agent_type=UnrealRelationInstanceAgent,
                                      comment=r.comment, agents_to_activate=r.agents_to_activate,
                                      incoming_links=r.incoming_links, threshold=r.threshold,
                                      level_of_activation=r.level_of_activation,
                                      speed_of_change=r.speed_of_change, situations=r.situations,
                                      instance_of=r.instance_of, part_of=r.part_of,
                                      has_parts=r.has_parts, mappings=r.mappings,
                                      arity=r.arity, arguments=r.arguments,
                                      argument_of=r.argument_of, justifications=r.justifications)
                inhibit_competing_anticipations(new_agent)
                variables.target_agents = variables.target_agents + [new_agent]
            variables.list_of_all_requests.remove(r)


def inhibit_competitory_mappings(agent):
    if not isinstance(agent, MappingAgent):
        dual_raise("Mapping into wm: ",
                   "The agent: '{}' is not an abstraction.".format(agent))
    else:
        # 1. Find BaseElement and TargetElement.
        t = agent.target_instance[0]
        b = agent.base_instance[0]
        # Setting inhibitory links for all mappings that contradict/inhibit each other.
        t_mapps = t.mappings
        b_mapps = b.mappings
        for t_m in t_mapps:
            if not t_m == agent:
                add_in_slot(agent, "inhibitions", t_m)
        for b_m in b_mapps:
            if not b_m == agent:
                add_in_slot(agent, "inhibitions", b_m)


def handle_the_list_of_mapping_requests(new_mappings):

    for r in new_mappings:
        if isinstance(r, MappingRequest):
            flag = True
            for agent in variables.all_agents.values():
                if agent == get_agent(r.name):
                    flag = False
                    dual_raise("Handle_the_list_of_mapping_requests: ",
                               "The request: '{}' is a duplicate.".format(r.name))
            if flag:
                # Checks if the target agent has been categorized already.
                """
                if len(r.target_instance[0].part_of) > 0:
                    if r.target_instance[0].part_of[0].instance_of:
                        #print("in handle_the_list_of_mapping_requests and something is wrong: {}".format(r.name))
                        variables.list_of_all_requests.remove (r)
                        return []
                """
                new_agent = add_agent(r.name, agent_type=MappingAgent, comment=r.comment,
                                      agents_to_activate=r.agents_to_activate,
                                      incoming_links=r.incoming_links, threshold=r.threshold,
                                      level_of_activation=r.level_of_activation,
                                      speed_of_change=r.speed_of_change, superclasses=r.superclasses,
                                      target_instance=r.target_instance, base_instance=r.base_instance,
                                      justifications=r.justifications)
                # Sets the link from the mapping to the concept (superclass) at parameter "default_mapping_class_weight".
                for c in new_agent.superclasses:
                    create_link(new_agent, c, default_mapping_class_weight)
                for c in new_agent.justifications:
                    if isinstance(c, UnrealAgent):
                        create_link(c, new_agent, default_anticipation_mapping_just_weight)
                inhibit_competitory_mappings(new_agent)
        variables.list_of_all_requests.remove(r)


def check_common_part_of_concept(mapping):
    # For each whole of the base element of THE MAPPING checks whether there is a correspondent whole of the target element.
    # Returns a list of all necessary requests.
    anticipated_requests = []
    for b_whole in mapping.base_instance[0].part_of:
        if mapping.target_instance[0].part_of:
            for t_whole in mapping.target_instance[0].part_of:
                anticipated_requests = anticipated_requests + make_instance_request(mapping, b_whole, mapping.target_instance[0])
        else:
            anticipated_requests = anticipated_requests + make_instance_request(mapping, b_whole, mapping.target_instance[0])
    return anticipated_requests


def handle_anticipation_for_relational_mapping(mapping, to_be_anticipated, relation):
    # Checks for consistencies and returns requests if the mapped element is a relation.
    # First, check in list_of_all_anticipations
    duplicates = []
    for arg in relation.arguments:
        for whole in arg.part_of:
            if (whole in variables.list_of_anticipations) and (whole.instance_of == to_be_anticipated.instance_of):
                duplicates = duplicates + [whole]
    for req in variables.list_of_all_requests:
        if (isinstance(req, InstanceAnticipationRequest)) and (req.instance_of[0] == to_be_anticipated.instance_of):
            duplicates = duplicates + [req]
    if len(duplicates) == 0:
        return make_instance_request(mapping, to_be_anticipated, relation)
    elif len(duplicates) == 1:
        if isinstance(duplicates[0], InstanceAnticipationRequest):
            duplicates[0].has_parts = duplicates[0].has_parts + [relation]
            duplicates[0].justifications = duplicates[0].justifications + [mapping]
            return []
        else:
            create_link(relation, duplicates[0], default_part_of_weight)
            create_link(duplicates[0], relation, default_part_of_weight)
            relation.part_of = relation.part_of + [duplicates[0]]
            duplicates[0].has_parts = duplicates[0].has_parts + [relation]
            return []
            
    else:  # There is more than 1 duplicate!
        print("PISHTJA: MNOGO DUBLICATES W HANDLE_ANTICIPATIONS RELATIONS....")
        # AKO IMA ANTICIPATION< DA PREHWYRLI WSICHKO KUM NEGO; AKO NJAMA _ KUM PYRWIQ!
        return []
              

def handle_anticipation_for_instance_mapping(mapping, to_be_anticipated, instance):
    # Checks for consistencies and returns requests if the mapped element is an instance.
    duplicates = []
    for rel in instance.argument_of:
        for whole in rel.part_of:
            if (whole in variables.list_of_anticipations) and (whole.instance_of == to_be_anticipated.instance_of):
                duplicates = duplicates + [whole]
    for req in variables.list_of_all_requests:
        if (isinstance(req, InstanceAnticipationRequest)) and (req.instance_of == to_be_anticipated.instance_of):
            duplicates = duplicates + [req]
    if len(duplicates) == 0:
        return make_instance_request(mapping, to_be_anticipated, instance)
    elif len(duplicates) == 1:
        if isinstance(duplicates[0], InstanceAnticipationRequest):
            duplicates[0].has_parts = duplicates[0].has_parts + [instance]
            return []
        else:
            create_link(instance, duplicates[0], default_part_of_weight)
            create_link(duplicates[0], instance, default_part_of_weight)
            instance.part_of = instance.part_of + [duplicates[0]]
            duplicates[0].has_parts = duplicates[0].has_parts + [instance]
            return []
    else:  # There is more than 1 duplicate!
        print("Problem: Too many duplicates in HANDLE_ANTICIPATIONS INSTANCE....")
        # If there is an anticipation, replace everything to it. If not --> to the first one.
        return []


def check_relation_anticipation(relation):
    # If there is a relation without corresponding one, check if its arguments are all mapped to something in the target.
    # For now, we think that the function needs only the relation as an argument.
    pass


def inhibit_competing_anticipations(agent):
    for has_p in agent.has_parts:
        for part_o in has_p.part_of:
            if (isinstance(part_o, UnrealAgent)) and (part_o != agent):
                create_link(agent, part_o, default_inhibitory_weight)
                create_link(part_o, agent, default_inhibitory_weight)
                if part_o not in agent.inhibitions:
                    agent.inhibitions = agent.inhibitions + [part_o]
                if agent not in part_o.inhibitions:
                    part_o.inhibitions = part_o.inhibitions + [agent]

                
def remove_anticipations():
    pass

# OTHERS #
##########


def collect_all_relational_interconnected(agent):
    # Returns a list of all agents that have a path through any relations with AGENT.
    list_1 = [agent]
    list_2 = [agent]
    while list_1:
        new_list = []
        ag = list_1[0]
        if isinstance(ag, RelationInstanceAgent):
            for arg in ag.arguments:
                if arg not in list_2:
                    new_list = new_list + [arg]
            for rel in ag.argument_of:
                if rel not in list_2:
                    new_list = new_list + [rel]
        else:
            for rel in ag.argument_of:
                if rel not in list_2:
                    new_list = new_list + [rel]
        list_1 = list_1 + new_list
        list_2 = list_2 + new_list
        list_1.remove(ag)
    return list_2

# Think whether to go upper in the structure and to consider connections through higher order relations.
# NOW we do look at the higher order relations.


def collect_all_agents_with_a_common_structure(request):
    # Returns a list of all AnticipationAgents that share the same structure as REQUEST.
    existing_anticip = []
    for anticip in variables.list_of_anticipations:
        justifications = anticip.justifications
        parts = []
        for justification in justifications:
            parts = parts + justification.base_instance
            anticip_agents = []
            for part in parts:
                anticip_agents = anticip_agents + collect_all_relational_interconnected(part)
                if part.instance_of:
                    anticip_agents = anticip_agents + collect_all_relational_interconnected(part.instance_of[0])
            agents = []
            for req_just in request.justifications:
                agents = agents + collect_all_relational_interconnected(req_just.base_instance[0])
                if req_just.base_instance[0].argument_of:
                    agents = agents + collect_all_relational_interconnected(req_just.base_instance[0].argument_of[0])
                connection = [val for val in anticip_agents if val in agents]
                if connection:
                    if anticip not in existing_anticip:
                        existing_anticip = existing_anticip + [anticip]
    if len(existing_anticip) > 1:
        print("There is more than 1 anticipations that fulfills the condition: '{}'.".format(existing_anticip))
        for inhibition in existing_anticip[0].inhibitions:
            for jus in request.justifications:
                if jus == inhibition:
                    print("The relation check is not enough!")
    return existing_anticip
            
# END OF FILE REQUESTS.PY #
