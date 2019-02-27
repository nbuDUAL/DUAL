
#############
# L I N K S #
#############

# DEFINES FUNCTIONS FOR LINKS MANIPULATION (CREATION AND REMOVAL).
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018

# TO DO: To define more update weights methods for the update_weight function?

"""
Each agent is connected to few peers through weighted links. Each agent sends activation to its neighbors,
resulting in constant exchange of activation. (For more information --> activation.py and main_cycle.py.)

Most of the agents in the DUAL architecture receive only excitatory input.
Exception make Mapping and Unreal(anticipation) agents - those are the so-called temporary agents
that the architecture creates by itself. They compete with their rivals by means of
inhibitory links and, therefore, receive both excitatory and inhibitory activation.
Constraint satisfaction is implemented by the connectionist aspect of those agents.
(The links in the constraint-satisfaction network are created by other modules/files
where defined are the marker-passing/semantic similarity pressures, the structure-correspondence, etc.

* create_link (sender, receiver, weight, function)
--> A function which creates a link/connection between SENDER and RECEIVER.
SENDER and RECEIVER are agents (as expected, SENDER activates RECEIVER ).
If there is no link between SENDER and RECEIVER such is created with WEIGHT.
If there is an existing link, the link's weight is updated with WEIGHT.
For the purpose the argument FUNCTION is send to the function update_weight (link, weight, function).
For the moment the default value of FUNCTION is "change".

* create_new_link (sender, receiver, weight) --> Returns link from SENDER to RECEIVER with specific WEIGHT.

* update_weight (link, new_weight, function) --> The weight of an existing LINK is updated with NEW_WEIGHT.

* create_links_of_the_new_agent (new_agent) --> The function is called when NEW_AGENT is added.
The function creates bi-directional links between NEW_AGENT and all of its slots' arguments.

* remove_link (link, receiver)
--> The function deletes the LINK. It removes it from the RECEIVER's "incoming_links" slot.
It also removes the RECEIVER from the the sender's slot "agents_to_activate".

* get_outgoing_link_weight(sender, receiver) --> Given two agents SENDER and RECEIVER,
the function returns the weight of the outgoing link from the SENDER to the RECEIVER.

* add_noise_of_links_of_agent (agent, variance)
--> Adds random noise between 0.00 and VARIANCE to all outgoing links of AGENT.

* add_noise_in_all_links (variance)
--> Adds random noise between 0.00 and VARIANCE to all outgoing links of all Dual agents.

* normalize_instance_links(concept, variance)
--> The function normalizes all links pointing to the CONCEPT's instances.
"""

from classes import *
# The function "gauss" from the module "random" is imported so we can generate random noise to the links's weights.
from random import gauss


def create_new_link(sender, receiver, weight):
    # If the link already exists, a new identical link is also created.
    l = Link(sender, weight)
    sender.agents_to_activate = sender.agents_to_activate + [receiver]
    receiver.incoming_links = receiver.incoming_links + [l]
    return l


def update_weight(link, new_weight, function="change"):
    # Updates weight using function.
    if function == "change":
        link.weight = new_weight
    # TO DO: To define more update weights methods.
    else:
        dual_raise("UPDATE_WEIGHT",
                   "Not defined function '{}'.".format(function))


def remove_link(link, receiver):
    link.sender.agents_to_activate = [x for x in link.sender.agents_to_activate if x != receiver]
    # removes RECEIVER for LINK.SENDER.AGENTS_TO_ACTIVATE.
    receiver.incoming_links.remove(link)
    del link


def create_link(sender, receiver, weight, function="change"):
    # Creates new link OR updates weight if the link exists already.
    sender = sender
    receiver = receiver
    already_exist = False
    for l in receiver.incoming_links:
        if l.sender == sender:
            already_exist = True
            update_weight(l, weight, function)
    if not already_exist:
        create_new_link(sender, receiver, weight)


def create_links_of_the_new_agent(new_agent):
    # Goes through the slots of the NEW_AGENT and creates the respective bi-directional links.

    try:
        for act in new_agent.agents_to_activate:
            create_link(new_agent, act, weight=default_associative_weight)
            create_link(act, new_agent, weight=default_associative_weight)
    except AttributeError:
        pass
    
    try:
        for link in new_agent.incoming_links:
            create_link(new_agent, link, weight=default_associative_weight)
            create_link(link, new_agent, weight=default_associative_weight)
    except AttributeError:
        pass

    try:
        for sup in new_agent.superclasses:
            create_link(new_agent, sup, weight=default_is_a_weight)
            create_link(sup, new_agent, weight=default_class_subclass_weight)
            if not (new_agent in sup.subclasses):
                sup.subclasses = sup.subclasses + [new_agent]
    except AttributeError:
        pass
            
    try:
        for sub in new_agent.subclasses:
            create_link(new_agent, sub, weight=default_class_subclass_weight)
            create_link(sub, new_agent, weight=default_is_a_weight)
            if not (new_agent in sub.superclasses):
                sub.superclasses = sub.superclasses + [new_agent]
    except AttributeError:
        pass

    try:
        for inst in new_agent.instances:
            create_link(new_agent, inst, weight=default_class_instance_weight)
            create_link(inst, new_agent, weight=default_is_a_weight)
            if not (new_agent in inst.instance_of):
                inst.instance_of = inst.instance_of + [new_agent]
    except AttributeError:
        pass

    try:
        for inst_of in new_agent.instance_of:
            create_link(new_agent, inst_of, weight=default_instance_of_weight)
            create_link(inst_of, new_agent, weight=default_class_instance_weight)
            if not (new_agent in inst_of.instances):
                inst_of.instances = inst_of.instances + [new_agent]
    except AttributeError:
        pass

    try:
        for h_parts in new_agent.has_parts:
            create_link(new_agent, h_parts, weight=default_has_part_weight)
            create_link(h_parts, new_agent, weight=default_part_of_weight)
            if not (new_agent in h_parts.part_of):
                h_parts.part_of = h_parts.part_of + [new_agent]
    except AttributeError:
        pass

    try:
        for part_o in new_agent.part_of:
            create_link(new_agent, part_o, weight=default_part_of_weight)
            create_link(part_o, new_agent, weight=default_has_part_weight)
            if not (new_agent in part_o.has_parts):
                part_o.has_parts = part_o.has_parts + [new_agent]
    except AttributeError:
        pass

    try:
        for sit in new_agent.situations:
            create_link(new_agent, sit, weight=default_part_of_weight)
            create_link(sit, new_agent, weight=default_is_part_weight)
    except AttributeError:
        pass

    try:
        for arg in new_agent.arguments:
            create_link(new_agent, arg, weight=default_predicate_argument_weight)
            create_link(arg, new_agent, weight=default_argument_predicate_weight)
            if not (new_agent in arg.argument_of):
                arg.argument_of = arg.argument_of + [new_agent]     
    except AttributeError:
        pass

    try:
        for arg_of in new_agent.argument_of:
            create_link(new_agent, arg_of, weight=default_argument_predicate_weight)
            create_link(arg_of, new_agent, weight=default_predicate_argument_weight)
            if not (new_agent in arg_of.arguments):
                arg_of.arguments = arg_of.arguments + [new_agent]
    except AttributeError:
        pass

    try:
        for target in new_agent.target_instance:
            create_link(new_agent, target, weight=default_instance_of_weight)
            create_link(target, new_agent, weight=default_instance_of_weight)
            if not (new_agent in target.mappings):
                target.mappings = target.mappings + [new_agent]
    except AttributeError:
        pass

    try:
        for base in new_agent.base_instance:
            create_link(new_agent, base, weight=default_instance_of_weight)
            create_link(base, new_agent, weight=default_instance_of_weight)
            if not (new_agent in base.mappings):
                base.mappings = base.mappings + [new_agent]
    except AttributeError:
        pass

    try:
        for base in new_agent.justifications:
            create_link(new_agent, base, weight=default_justification_weight)
            create_link(base, new_agent, weight=default_justification_weight)
            if not (new_agent in base.justifications):
                if not isinstance(new_agent, UnrealInstanceAgent):
                    base.justifications = base.justifications + [new_agent]
    except AttributeError:
        pass

    try:
        for inh in new_agent.inhibitions:
            create_link(new_agent, inh, weight=default_inhibitory_weight)
            create_link(inh, new_agent, weight=default_inhibitory_weight)
            if not (new_agent in inh.inhibitions):
                inh.inhibitions = inh.inhibitions + [new_agent]
    except AttributeError:
        pass


def get_outgoing_link_weight(sender, receiver):
    for l in receiver.incoming_links:
        if l.sender == sender:
            return l.weight
        

def add_noise_of_links_of_agent(agent, variance):
    for link in agent.incoming_links:
        link.weight = link.weight + gauss(0.00, variance)
        if link.weight < 0.00:
            link.weight = 0.01


def add_noise_in_all_links(variance):
    for agent in variables.all_agents.values():
        add_noise_of_links_of_agent(agent, variance)


def normalize_instance_links(concept, variance):
    length = len(concept.instances)
    for inst in concept.instances:
        for l in inst.incoming_links:
            if l.sender == concept:
                l.weight = (l.weight + gauss(0.00, length*variance))/length
                if l.weight < 0.00:
                    l.weight = 0.01

# END OF FILE LINKS.PY #
