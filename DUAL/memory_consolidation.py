
########################
# Memory consolidation #
########################

# DEFINES FUNCTIONS FOR CATEGORY LEARNING.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018


#####################
# External protocol #
#####################

"""



.....

# MEMORY CONSOLIDATION #
########################

* decide_to_kill(looser) -->

* split_justifications(agent, list_of_neighbors) --> Returns three lists: Arguments; Argument_of; Part_of.
The last one - Part_of contains everything that is unknown.

* concept_creation(mapping, args) -->

* relational_concept_creation(mapping, args) -->

* update_argument_of(new_agent, args, mapping) -->

* mapping_into_concept(mapping) -->

* search_and_create_new_situations(target_instance, base_instance, concept)
--> Classifies the episode as a situation. If such does not exists, the function creates it.

* anticipation_into_instance(anticipation) -->

* hierarchy_tuning(categorized_instance, anticipation) -->
"""

from activation import *
import variables
from random import randint

########################################################################
# CLASSIFICATION PART used for the inverse base rate effect simulation #
########################################################################


def random_classification():
    rand_int = randint(1, 10)
    if rand_int % 2 == 0:
        resp = str("A")
    else:
        resp = str("B")
    return resp


def give_feedback(instance):
    if "_a_" in instance.name:
        return True
    else:
        return False


def classify_first_example(instance):
    # Classifies the first example into a random category (A or B),
    # because there is nothing into the LTM/WM to which it can compare it.
    random_classification()
    current_feedback = give_feedback(instance)
    if current_feedback:
        update_schema(instance, find_agent("cat_A"))
    else:
        update_schema(instance, find_agent("cat_B"))


# FOR now it is used only for claasification CAT_A/CAT_B simulations???
def update_schema(target_instance, category):
    name_target_schema = gen_name_sit(category.name)
    comment_target = "Created new instance of the schema/category: {} for: {} in time: {}.".format(
        category, target_instance, variables.dual_time)
    target_schema = add_agent(name=name_target_schema, agent_type=InstanceAgent, comment=comment_target,
                              has_parts=[target_instance], instance_of=[category])
    for interconn in collect_all_relational_interconnected(target_instance):
        add_in_slot(interconn, "part_of", target_schema)
    variables.target_agents = variables.target_agents + [target_schema]
    variables.just_created = variables.just_created + [target_schema]


def correct_or_not(anticipation):
    # First, checks if the classification is correct
    if ((("_a" in anticipation.has_parts[0].name) and (
        anticipation.instance_of[0] == find_agent("cat_A"))) or (
            ("_b" in anticipation.has_parts[0].name) and (
                        anticipation.instance_of[0] == find_agent("cat_B")))):
        instance_of = anticipation.instance_of
    else:
        # If the classification is not correct, it will only add the instance accordingly,
        # without receiving the chance to do anything else
        variables.correct_classification = False
        if anticipation.instance_of[0] == find_agent("cat_A"):
            instance_of = [find_agent("cat_B")]
        else:
            instance_of = [find_agent("cat_A")]
    return instance_of

# MEMORY CONSOLIDATION #
########################


def decide_to_kill(looser):
    # LOOSER is a list containing all mappings that contradict the winning one.
    # (which is to become a real concept).
    for inh in looser:
        print("deleting: ", looser)
        remove_agent(inh)  # TO DO: think about whether we delete the loosers completely or
    # to take away all their activation


def split_justifications(agent, list_of_neighbors):
    # Returns three lists: Arguments; Argument_of; Part_of.
    # The last one - Part_of contains everything that is unknown.
    argss = []
    argss_of = []
    parts_of = []
    for n in list_of_neighbors:
        if not isinstance(n, UnrealAgent):
            for n_superc in n.superclasses:
                for ag_superc in agent.superclasses:
                    if isinstance(n_superc, SemanticAgent):
                        if ag_superc in n_superc.argument_of:
                            argss = argss + [n]
                        if isinstance(n_superc, RelationConceptAgent):
                            if ag_superc in n_superc.arguments:
                                argss_of = argss_of + [n]
                    else:
                        parts_of = parts_of + [n]
    return argss, argss_of, parts_of
                    

def concept_creation(mapping, args):
    if variables.user_interaction:
        name = ask_for_a_name(mapping)
    else:
        name = mapping.name.strip("abstr_")
    comment = ("Created by: {} in dual time: {} (which was {}).".format(mapping,
                                                                        variables.dual_time, mapping.comment))
    threshold = threshold_agent_activation
    level_of_activation = mapping.level_of_activation
    speed_of_change = mapping.speed_of_change
    superclasses = mapping.superclasses
    instances = [mapping.target_instance[0], mapping.base_instance[0]]
    # Fix the instances - now it takes care only of the direct ones.
    # Make it check in the upper part of the hierarchy as well!
    # collect_all_active... OR - leave like this for now
    for superc in mapping.superclasses:
        for inst in instances:
            remove_from_slot(superc, "instances", inst)
    argument_of = args[1]
    part_of = args[2]
    if isinstance(mapping.target_instance[0], RelationInstanceAgent):
            dual_raise("concept_creation",
                       "The mapping: {} is trying to become a ConceptAgent, but it is supposed to be a RelationInstanceAgent.".format(
                           mapping))
    else:
        new_agent = add_agent(name=name, agent_type=ConceptAgent, comment=comment,
                              threshold=threshold, level_of_activation=level_of_activation,
                              speed_of_change=speed_of_change, superclasses=superclasses,
                              instances=instances, part_of=part_of, argument_of=argument_of)
    return new_agent


def relational_concept_creation(mapping, args):
    if variables.user_interaction:
        name = ask_for_a_name(mapping)
    else:
        name = mapping.name.strip("abstr_")
    comment = ("Created by: {} in dual time: {} (which was {}).".format(mapping,
                                                                        variables.dual_time, mapping.comment))
    threshold = threshold_agent_activation
    level_of_activation = mapping.level_of_activation
    speed_of_change = mapping.speed_of_change
    superclasses = mapping.superclasses
    instances = [mapping.target_instance[0], mapping.base_instance[0]]
    # Fix the instances - now it takes care only of the direct ones.
    # Make it check in the upper part of the hierarchy as well!
    # collect_all_active... OR - leave like this for now
    for superc in mapping.superclasses:
        for inst in instances:
            remove_from_slot(superc, "instances", inst)
    argument_of = args[1]
    part_of = args[2]
    arity = len(args[0])
    arguments = args[0]
    if isinstance(mapping.target_instance[0], InstanceAgent):
            dual_raise("relational_concept_creation",
                       "The mapping: {} is trying to become a RelationConceptAgent, but it is supposed to be a ConceptAgent.".format(
                           mapping))
    else:
        # TO DO: LOOK IF IT WORKS WITH MORE THAN TWO ARGUMENTS!
        new_agent = add_agent(name=name, agent_type=RelationConceptAgent, comment=comment,
                              threshold=threshold, level_of_activation=level_of_activation,
                              speed_of_change=speed_of_change, arity=arity,
                              arguments=arguments, instances=instances, argument_of=argument_of,
                              superclasses=superclasses, part_of=part_of)
        for arg in arguments:
            if isinstance(arg, MappingAgent):
                arg.justifications = arg.justifications + [new_agent]
                create_link(new_agent, arg, default_justification_weight)
            else:
                # It keeps the arguments in order.
                new_agent.arguments = [x for x in new_agent.arguments if x != arg]
                for inst in new_agent.instances:
                    if inst in variables.target_agents:
                        for i in range(len(inst.arguments)):
                            for inst_of in inst.arguments[i].instance_of:
                                if inst_of == arg:
                                    new_agent.arguments.insert(i, arg)
    return new_agent


def update_argument_of(new_agent, args, mapping):
    for argument in args[1]:
        if argument not in new_agent.argument_of:
            new_agent.argument_of = new_agent.argument_of + argument
    for arg in args[1]:
        placed = True
        # In case arg is still a Mapping agent.
        if isinstance(arg, MappingAgent):
            if isinstance(arg.target_instance[0], RelationInstanceAgent):
                for i in range(len(arg.target_instance[0].arguments)):
                    if mapping.target_instance[0] == arg.target_instance[0].arguments[i]:
                        argument_place = int(i)
                arg.justifications.insert(argument_place, new_agent)
        else:
            # In case new_agent is argument of more than one relation.
            for i in range(len(arg.arguments)):
                if placed:
                    # Keeps track of the arguments order.
                    if isinstance(arg.arguments[i], MappingAgent):
                        if mapping.target_instance[0] == arg.arguments[i].target_instance[0]:
                            arg.arguments = [x for x in arg.arguments if x != new_agent]
                            arg.arguments.insert(i, new_agent)
                            placed = False
                        elif mapping.target_instance[0] == arg.arguments[i]:
                            arg.arguments = [x for x in arg.arguments if x != new_agent]
                            arg.arguments.insert(i, new_agent)
                            placed = False
                        else:
                            print("In mapping_into_concept with: new agent {}, args: {} and mapping {} why are we passing 1?".format(new_agent, args, mapping))
                            pass
            create_link(arg, new_agent, default_predicate_argument_weight)
            create_link(new_agent, arg, default_argument_predicate_weight)


def mapping_into_concept(mapping):
    # The function transforms MAPPING into a real concept.
    # Removes/deletes the inhibiting mapping agents that compete with the mapping which is to be transformed into a concept.
    decide_to_kill(mapping.inhibitions)
    args = split_justifications(mapping, mapping.justifications)
    print("{}, IN Mapping_into_concept, just split arguments: {}, argument_of: {}, part_of: {}".format(mapping, args[0],
                                                                                                       args[1], args[2]))
    if not args[0]:
        # The concept created would be e ConceptAgent.
        new_agent = concept_creation(mapping, args)
    else:
        # The concept created would be e RelationConceptAgent.
        new_agent = relational_concept_creation(mapping, args)
    # In case the newly created agent is an argument of a relation.
    if args[1]:
        update_argument_of(new_agent, args, mapping)
    variables.just_created = variables.just_created + [new_agent]
    # Look whether there are situations in the target or in the base; if not, create them!
    search_and_create_new_situations(mapping.target_instance[0], mapping.base_instance[0], new_agent)
    # Removes/deletes the mapping agent that was transformed into a concept.
    remove_agent(mapping)

    
def search_and_create_new_situations(target_instance, base_instance, concept):
    # Classifies the episode as a situation. If such does not exist, the function creates it.
    if ((target_instance.part_of and (target_instance.part_of[0] not in variables.just_created)) or (
                base_instance.part_of and (base_instance.part_of[0] not in variables.just_created))):
        return []
    else:
        flag = True
        for interconn in collect_all_relational_interconnected(target_instance):
            if interconn.part_of:
                flag = False
                situation = interconn.part_of[0].instance_of[0]
                add_in_slot(concept, "part_of", situation)
        if flag:
            if variables.user_interaction:
                name_concept = ask_for_a_name(concept)
            else:
                name_concept = gen_name_sit_from_zero(concept.name)
            comment_concept = "The situation was created by: '{}' in time {}".format(
                concept, variables.dual_time)
            concept_sit = add_agent(name=name_concept, agent_type=ConceptAgent,
                                    comment=comment_concept, has_parts=[concept])

            name_base_sit = gen_name_sit(concept.name)
            comment_base = "The base instance situation was created by: '{}' for: '{}' in time {}".format(
                concept, base_instance, variables.dual_time)
            base_sit = add_agent(name=name_base_sit, agent_type=InstanceAgent,
                                 comment=comment_base, has_parts=[base_instance],
                                 instance_of=[concept_sit])
            for interconn in collect_all_relational_interconnected(base_instance):
                add_in_slot(interconn, "part_of", base_sit)
            
            name_target_sit = gen_name_sit(concept.name)
            comment_target = "The target instance situation was created by: '{}' for: '{}' in time {}".format(
                concept, target_instance, variables.dual_time)
            target_sit = add_agent(name=name_target_sit, agent_type=InstanceAgent,
                                   comment=comment_target, has_parts=[target_instance],
                                   instance_of=[concept_sit])
            for interconn in collect_all_relational_interconnected(target_instance):
                add_in_slot(interconn, "part_of", target_sit)

            variables.target_agents = variables.target_agents + [target_sit]
            variables.just_created = variables.just_created + [concept_sit,
                                                               target_sit,
                                                               base_sit]

# ANTICIPATION INTO INSTANCE


def anticipation_into_instance(anticipation):
    print("Anticipaton_into_instance: ", anticipation)
    describe_agent(anticipation)
    if variables.feedback:
        instance_of = correct_or_not(anticipation)
    else:
        instance_of = anticipation.instance_of
    if variables.user_interaction:
        name = ask_for_a_name(anticipation)
    else:
        name = gen_name_sit(instance_of[0].name)
    comment = "Created by: '{}' in dual time: {} (which was: {}).".format(
        anticipation.name, variables.dual_time, anticipation.comment)
    level_of_activation = anticipation.level_of_activation
    # It adds only the Instance agents.... but there are relation instances as well...
    # has_parts = [x for x in anticipation.has_parts if isinstance(x, InstanceAgent)]
    has_parts = anticipation.has_parts
    part_of = anticipation.part_of
    argument_of = anticipation.argument_of
    decide_to_kill(anticipation.inhibitions)
    if isinstance(anticipation, UnrealRelationInstanceAgent):
        arity = anticipation.arity
        arguments = anticipation.arguments
        new_agent = add_agent(name=name, agent_type=RelationInstanceAgent, comment=comment,
                              level_of_activation=level_of_activation, arity=arity,
                              arguments=arguments, argument_of=argument_of, instance_of=instance_of,
                              part_of=part_of, has_parts=has_parts)
    elif isinstance(anticipation, UnrealInstanceAgent):
        new_agent = add_agent(name=name, agent_type=InstanceAgent, comment=comment,
                              level_of_activation=level_of_activation, argument_of=argument_of,
                              instance_of=instance_of, part_of=part_of, has_parts=has_parts)
    else:
        dual_raise("anticipation_into_instance",
                   "We are trying to turn: '{}' into instance agent.".format(anticipation))

    """ # !!! Check the rest of the simulations - specifically the inverse base rate;
    if it turns out that it is not needed, remove it.
    Probably it will not be needed, because the instances are encoded by hand, not learned.
    if variables.feedback:
        r = randint(1, 2)
        if r == 1:
            for t in variables.target_agents:
                if isinstance(t, InstanceAgent):
                    if t not in new_agent.has_parts:
                        add_in_slot(new_agent, "has_parts", t)
                    if t.instance_of[0] == find_agent("B"):
                        create_link(t, t.instance_of[0], special)
                        create_link(t.instance_of[0], t, special)
                    if t.instance_of[0] == find_agent("C"):
                        create_link(t, t.instance_of[0], special)
                        create_link(t.instance_of[0], t, special)
    """
    variables.just_created = variables.just_created + [new_agent]
    variables.target_agents = variables.target_agents + [new_agent]
    # Categorizes the situation elements.
    hierarchy_tuning(new_agent, anticipation)
    # Removes the old agent and the mapping that created it?
    for j in anticipation.justifications:
        if j not in variables.deactivated_agents:
            # Instead of removing the agent its activation level is decreased.
            variables.deactivated_agents = variables.deactivated_agents + [j]
        j.level_of_activation = 0.0
        # remove_agent(j)
    anticipation.level_of_activation = 0.0
    if anticipation not in variables.deactivated_agents:
        variables.deactivated_agents = variables.deactivated_agents + [anticipation]
    variables.target_agents = [x for x in variables.target_agents if x != anticipation]
    # remove_agent(anticipation)
    # DELETE AFTER THAT, NOW IT IS ADDED JUST FOR TESTING
    
    """ # !!! Check the rest of the simulations; if it turns out that it is not needed, remove it.
    # Added on 19.02 for th infant simulation
    decide_to_kill(variables.list_of_mappings)
    for m in variables.list_of_mappings:
        remove_agent(m)
    if variables.list_of_mappings:
        variables.list_of_mappings = []
    for m in variables.list_of_anticipations:
        remove_agent(m)
    if variables.list_of_anticipations:
        variables.list_of_anticipations = []
    """
        

def hierarchy_tuning(categorized_instance, anticipation):
    # The function checks whether some of the elements of the already classified target situation
    # can also be classified in accordance to the global pattern.
    anticipation.justifications = sorted(anticipation.justifications,
                                         key=lambda x: x.level_of_activation)
    anticipation.justifications.reverse()
    parts_for_classificaton = anticipation.has_parts
    parts_to_classsify_at = categorized_instance.instance_of[0].has_parts
    classified = []
    for just in anticipation.justifications:
        for part in parts_to_classsify_at:
            for instance in part.instances:
                if just.target_instance[0] in parts_for_classificaton:
                    if just.base_instance[0] == instance:
                        if just.target_instance[0].instance_of[0] in collect_all_active_superclasses(part):
                            remove_from_slot(just.target_instance[0].instance_of[0], "instances", just.target_instance[0])
                        add_in_slot(part, "instances", just.target_instance[0])
                        parts_for_classificaton = [x for x in parts_for_classificaton if x != just.target_instance[0]]
                        parts_to_classsify_at = [x for x in parts_to_classsify_at if x != part]
                        classified = classified + [just]
    # Deletion of the classified agents.
    for m in classified:
        for other_m in m.target_instance[0].mappings:
            # Instead of removing the agent its activation level is decreased.
            # In addition, the agent is listed as unactive agents to it cannot influence the model's behaviour.
            if other_m not in variables.deactivated_agents:
                variables.deactivated_agents = variables.deactivated_agents + [other_m]
            other_m.level_of_activation = 0.0
            # remove_agent(other_m)
        if m not in variables.deactivated_agents:
            variables.deactivated_agents = variables.deactivated_agents + [m]
        m.level_of_activation = 0.0
        # remove_agent(m)
    for part in categorized_instance.has_parts:
        # TEST IF THIS WORKS AS EXPECTED!
        remove_from_slot(part, "part_of", anticipation)


# End of file memory_consolidation.py #
