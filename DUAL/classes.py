
#################
# C L A S S E S #
#################

# DEFINES THE VARIOUS CLASSES USED BY DUAL (DualError, DUAL agents, LINK, DUAL requests)
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last update: Yolina Petrova, December, 2018

#####################
# External protocol #
#####################

# DUAL agents structure #
#########################

# DUAL's class structure:
#                                      _______________
#                                     |               |
#                                     |   DUAL agent  |
#                                     |_______________|
#                                    /                  \
#                                   /                    \
#                        __________/_____             ____\___________
#                       |                |           |                |
#                       | SEMANTIC agent |           | EPISODIC agent |
#                       |________________|           |________________|\_ _ _ _ _ _ _ _ _
#                     /       |        \                      |       |                   \
#                    /        |         \                     \        \_ _ _ _ _ _        \_ _ _ _ _ _
#  _______________  /  _______|________  \ _______________     \________________   \________________   \ ______________
# |               |   |    RELATION    |  |               |    |                |  |    RELATION    |   |              |
# | CONCEPT agent |   | CONCEPT agent  |  | MAPPING agent |    | INSTANCE agent |  | INSTANCE agent |   | UNREAL agent |
# |_______________|   |________________|  |_______________|    |________________|  |________________|   |______________|
#                                                                                                         /          \
#                                                                                                        /            \
#                                                                                          _____________/___     ________________
#                                                                                         | UNREAL RELATION |   |     UNREAL     |
#                                                                                         | INSTANCE agent  |   | INSTANCE agent |
#                                                                                         |_________________|   |________________|
#
#

"""
# Dual Error #
##############

class DualError signals for various custom defined errors. It has a single slot.
<DualError>.function --> FUNCTION refers to the function, where the error has occurred
(that is the the function where the specific error has been called).

dual_raise (function, message)--> This function takes care of the error messages.
Prompts an error of type DualError with information about which FUNCTION calls the specific MESSAGE.
The Error is not reported if the global variable variables.flag_error equals False.

# Dual Agents #
###############
The DUAL agents are hybrid entities that have many aspects, for example:
    -- symbolic vs. connectionist aspect of a DUAL agent   and
    -- declarative vs. procedural aspect of a DUAL agent.

        +---------------+-------------------------------+
        |               | Representation   Processing   |
        +---------------+-------------------------------+
        | Connectionist |  activation      spreading    |
        | aspect        |  level           activation   |
        +- - - - - - - -+- - - - - - - - - - - - - - - -+
        | Symbolic      |  symbolic        symbol       |
        | aspect        |  structures      manipulation |
        +---------------+-------------------------------+

The diagram above illustrates the main classes of agents and the taxonomic relations between them.
At the top of the hierarchy is DUAL agent.
class DualAgent is the main superclass of all Dual agents.
It is designed as a foundation for the other classes of agents (usually, it is not used by itself).

The classes Semantic and Episodic Agents which inherit the upper class Dual agent
stand for the differentiation between the human's episodic and semantic memory. However, as DualAgent,
they are just 'holders' for the actual agents defined in and from the architecture.
Those are the 7 types of agents - shown on the graph above and bellow (marked with * in front of them).
(Some of those agents are predefined by the user - such is the case mainly with ConceptAgent, RelationConceptAgent,
InstanceAgent and RelationInstanceAgent;
and some are created by the architecture - such as MappingAgent and all UnrealAgents).

    class SemanticAgent - the main holder for the semantic memory.
        * class ConceptAgent
        * class RelationConceptAgent
        * class MappingAgent

    class EpisodicAgent - the main holder for the episodic memory.
        * class InstanceAgent
        * class RelationInstanceAgent
          class UnrealAgent
            * class UnrealRelationInstanceAgent
            * class UnrealInstanceAgent

Each agent is actually a collection of slots. Those slots are not intended to stand alone,
rather several slots form a micro-frame which holds the information specific for the given agent.

CONCEPT AGENT has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.word --> string               # The default value is ""                                        
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.part_of --> list              # The default value is []
    <agent>.has_parts --> list            # The default value is []
    <agent>.superclasses --> list         # The default value is []
    <agent>.subclasses --> list           # The default value is []
    <agent>.instances --> list            # The default value is []
    
RELATION CONCEPT AGENT has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.word --> string               # The default value is ""
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.part_of --> list              # The default value is []
    <agent>.has_parts --> list            # The default value is []
    <agent>.superclasses --> list         # The default value is []
    <agent>.subclasses --> list           # The default value is []
    <agent>.instances --> list            # The default value is []
    <agent>.arity --> integer             # The default value is 0
    <agent>.arguments --> list            # The default value is [], but if the number of arguments is different
                                            from the arity, an error is raised.

MAPPING AGENT has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.word --> string               # The default value is ""
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.part_of --> list              # The default value is []
    <agent>.has_parts --> list            # The default value is []
    <agent>.superclasses --> list         # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.justifications --> list       # The default value is []
    <agent>.inhibitions --> list          # The default value is []
    <agent>.target_instance --> list      # The default value is [], but if the number of entered elements is more
                                            or less than 1, an error is raised.
    <agent>.base_instance --> list        # The default value is [], but if the number of entered elements is more
                                            or less than 1, an error is raised.
                 
INSTANCE AGENT has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.word --> string               # The default value is ""
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.part_of --> list              # The default value is []
    <agent>.has_parts --> list            # The default value is []
    <agent>.instance_of --> list          # The default value is []
    <agent>.situations --> list           # The default value is []
    <agent>.mappings --> list             # The default value is []

RELATION INSTANCE AGENT has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.word --> string               # The default value is ""
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.part_of --> list              # The default value is []
    <agent>.has_parts --> list            # The default value is []
    <agent>.instance_of --> list          # The default value is []
    <agent>.situations --> list           # The default value is []
    <agent>.mappings --> list             # The default value is []
    <agent>.arity --> integer             # The default value is 0
    <agent>.arguments --> list            # The default value is [], but if the number of arguments is different
                                            from the arity, an error is raised.

UNREAL RELATION INSTANCE AGENT has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.word --> string               # The default value is ""
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.part_of --> list              # The default value is []
    <agent>.has_parts --> list            # The default value is []
    <agent>.situations --> list           # The default value is []
    <agent>.instance_of --> list          # The default value is []
    <agent>.mappings --> list             # The default value is []
    <agent>.arity --> integer             # The default value is 0
    <agent>.arguments --> list            # The default value is []
    <agent>.justifications --> list       # The default value is []

UNREAL INSTANCE AGENT has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.word --> string               # The default value is ""
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.part_of --> list              # The default value is []
    <agent>.has_parts --> list            # The default value is []
    <agent>.instance_of --> list          # The default value is []
    <agent>.situations --> list           # The default value is []
    <agent>.mappings --> list             # The default value is []
    <agent>.justifications --> list       # The default value is []


* describe_itself(agent)
--> The function describes AGENT. It gives all the available information that characterizes the agent.

# LINKS #
#########
The architecture's knowledge base is in the form of a network, where the networks' nodes are the agents and the
networks' arcs (connections) are the links between the agents. Each link has a pre-defined weight.
For more information --> links.py.
(!!! Soon, the architecture should be able to learn those weights by itself).
The main Link class contains all links between the different agents.

Class Link has two slots:
<Link>.sender --> DualAgent       # The value should be explicitly specified - this is another agent.
<Link>.weight --> float           # The default value is in parameters.py

# REQUESTS #
############
Before creating a temporary agent (MappingAgent or UnrealAgent) the architecture sends a request for its creation.
The idea behind those requests is somewhat binary - from one side it reflects the way the architecture works
(it works in cycles) and from another - they control for the lack of duplicate agents.
class Request is the main superclass of all Dual requests.
The user/program can create 3 types of requests:
    Mapping Request, Instance Anticipation Request and Relation Instance Anticipation Request.
    The requests' classes structure mirrors the structure of the Mapping Agent,
    Instance Agent and Relation Instance agent respectively.


MAPPING REQUEST has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.superclasses --> list         # The default value is []
    <agent>.justifications --> list       # The default value is []
    <agent>.target_instance --> list      # The default value is []
    <agent>.base_instance --> list        # The default value is []

INSTANCE ANTICIPATION REQUEST has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.instance_of --> list          # The default value is []
    <agent>.situations --> list           # The default value is []
    <agent>.part_of --> list              # The default value is []
    <agent>.has_parts --> list            # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.mappings --> list             # The default value is []
    <agent>.justifications --> list       # The default value is []


RELATION INSTANCE ANTICIPATION REQUEST has the following slots:
    <agent>.name --> string               # Should be explicitly specified. If the name duplicates an already
                                            existing one, an error is raised.
    <agent>.comment --> string            # The default value is ""
    <agent>.threshold --> float           # The default value is in parameters.py
    <agent>.level_of_activation --> float # The default value is in parameters.py
    <agent>.speed_of_change --> float     # The default value is in parameters.py
    <agent>.agents_to_activate --> list   # The default value is []
    <agent>.incoming_links --> list       # The default value is []
    <agent>.instance_of --> list          # The default value is []
    <agent>.situations --> list           # The default value is []
    <agent>.part_of --> list              # The default value is []
    <agent>.has_parts --> list            # The default value is []
    <agent>.argument_of --> list          # The default value is []
    <agent>.arity --> integer            # The default value is 0
    <agent>.arguments --> list            # The default value is []
    <agent>.mappings --> list             # The default value is []
    <agent>.justifications --> list       # The default value is []
    
"""

from parameters import *
import variables

# Dual Error #
##############


class DualError (Exception):
    # The class signaling for various custom defined errors.

    def __init__(self, function):
        self.function = function
        
    def __str__(self):
        return repr(self.function)


def dual_raise(function, message):
    if variables.flag_error:
        raise DualError("Function: {} says: {}".format(function, message))
    else:
        print("Function: {} says: {}".format(function, message))
    
# Dual Agents #
###############


class DualAgent(object):
    # The main class of all DUAL agents.

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation, level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change, argument_of=[],
                 part_of=[], has_parts=[]):
        
        self.name = name
        self.word = word
        self.comment = comment
        self.agents_to_activate = agents_to_activate
        self.incoming_links = incoming_links
        self.threshold = threshold
        self.level_of_activation = level_of_activation
        self.speed_of_change = speed_of_change
        self.input_activation = 0.0
        self.part_of = part_of
        self.has_parts = has_parts
        self.argument_of = argument_of

    def __repr__(self):
        return self.name    

    def describe_itself(self):
        print("The name of the agent is '{}' and its type is {}.".format(self.name, self.__class__.__name__))
        print("The word label of the agent is: {}".format(self.word))
        print("Comment: {}".format(self.comment))
        print("Threshold: {}".format(self.threshold))
        print("Activation level: {}".format(self.level_of_activation))
        print("Speed of change: {}".format(self.speed_of_change))
        incoming_links = ""
        for link in self.incoming_links:
            incoming_links = incoming_links + "(" + link.sender.name + " weight " + str(link.weight) + ") "
        print("Incoming links: ", incoming_links)
        outgoing_links = ""
        from links import get_outgoing_link_weight
        for agent in self.agents_to_activate:
            weight = get_outgoing_link_weight(self, agent)
            outgoing_links = outgoing_links + "(" + agent.name + " weight " + str(weight) + ") "
        print("Outgoing links: ", outgoing_links)
        print("Part of: ", ', '.join(str(x) for x in self.part_of))
        print("Has_parts: ", ', '.join(str(x) for x in self.has_parts))
        print("Argument_of: ", ', '.join(str(x) for x in self.argument_of))


# S E M A N T I C agent #
#########################


class SemanticAgent(DualAgent):
    # The main holder for the semantic memory.

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 superclasses=[], subclasses=[], instances=[]):
        
        DualAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links, threshold,
                           level_of_activation, speed_of_change, argument_of, part_of, has_parts)
        
        self.superclasses = superclasses
        self.subclasses = subclasses
        self.instances = instances
        
    def describe_itself(self):
        DualAgent.describe_itself(self)
        print("Superclasses: ", ", ".join(str(x) for x in self.superclasses))
        print("Subclasses: ", ", ".join(str(x) for x in self.subclasses))
        print("Instances: ", ", ".join(str(x) for x in self.instances))


class ConceptAgent(SemanticAgent):

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 superclasses=[], subclasses=[], instances=[]):
        
        SemanticAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links,
                               threshold, level_of_activation, speed_of_change, argument_of, part_of, has_parts,
                               superclasses, subclasses, instances)

    def describe_itself(self):
        SemanticAgent.describe_itself(self)


class RelationConceptAgent(SemanticAgent):

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 superclasses=[], subclasses=[], instances=[],
                 arity=0, arguments=[]):
        
        SemanticAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links,
                               threshold, level_of_activation, speed_of_change, argument_of, part_of, has_parts,
                               superclasses, subclasses, instances)
        
        self.arity = arity
        self.predicate = self
        self.arguments = arguments

    def describe_itself(self):
        SemanticAgent.describe_itself(self)
        print("The arity of the relation is: {}".format(self.arity))
        print("The predicate of the relation is: {}".format(self.predicate))
        print("The arguments of the relation are: ", ", ".join(str(x) for x in self.arguments))


class MappingAgent(SemanticAgent):

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 superclasses=[], justifications=[], inhibitions=[],
                 target_instance=[], base_instance=[]):
        
        DualAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links,
                           threshold, level_of_activation, speed_of_change, argument_of, part_of, has_parts)
        
        self.superclasses = superclasses
        self.justifications = justifications
        self.inhibitions = inhibitions
        self.target_instance = target_instance
        self.base_instance = base_instance
        variables.list_of_mappings = variables.list_of_mappings + [self]

    def describe_itself(self):
        DualAgent.describe_itself(self)
        print("Justifications: ", ", ".join(str(x) for x in self.justifications))
        print("Inhibits: ", ", ".join(str(x) for x in self.inhibitions))
        print("Superclasses: ", ", ".join(str(x) for x in self.superclasses))
        print("Target_instance: ", ", ".join(str(x) for x in self.target_instance))
        print("Base_instance: ", ", ".join(str(x) for x in self.base_instance))

###################
# E P I S O D I C #
###################


class EpisodicAgent(DualAgent):
    # The main holder for the episodic memory.

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 situations=[], instance_of=[], mappings=[]):

        DualAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links,
                           threshold, level_of_activation, speed_of_change, argument_of, part_of, has_parts)
        
        self.situations = situations
        self.instance_of = instance_of
        self.mappings = mappings
        
    def describe_itself(self):
        DualAgent.describe_itself(self)
        print("Situations: ", ", ".join(str(x) for x in self.situations))
        print("Instance_of: ", ", ".join(str(x) for x in self.instance_of))
        print("Mappings: ", ", ".join(str(x) for x in self.mappings))
            

class InstanceAgent(EpisodicAgent):

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 situations=[], instance_of=[], mappings=[]):
        
        EpisodicAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links,
                               threshold, level_of_activation, speed_of_change, argument_of, part_of, has_parts,
                               situations, instance_of, mappings)

    def describe_itself(self):
        EpisodicAgent.describe_itself(self)


class RelationInstanceAgent(EpisodicAgent):

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 situations=[], instance_of=[], mappings=[],
                 arity=0, arguments=[]):

        EpisodicAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links,
                               threshold, level_of_activation, speed_of_change, argument_of, part_of, has_parts,
                               situations, instance_of, mappings)
        
        self.arity = arity
        self.predicate = self
        self.arguments = arguments

    def describe_itself(self):
        EpisodicAgent.describe_itself(self)
        print("The arity of the relation is: {}".format(self.arity))
        print("The predicate of the relation is: {}".format(self.predicate))
        print("The arguments of the relation are: ", ", ".join(str(x) for x in self.arguments))


class UnrealAgent(EpisodicAgent):

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 situations=[], instance_of=[],  mappings=[],  justifications=[], inhibitions=[]):

        EpisodicAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links,
                               threshold, level_of_activation, speed_of_change, argument_of, part_of, has_parts,
                               situations, instance_of, mappings)
        
        self.justifications = justifications
        self.inhibitions = inhibitions
        variables.list_of_anticipations = variables.list_of_anticipations + [self]

    def describe_itself(self):
        EpisodicAgent.describe_itself(self)
        print("Justifications: ", ", ".join(str(x) for x in self.justifications))
        print("Inhibits: ", ", ".join(str(x) for x in self.inhibitions))


class UnrealRelationInstanceAgent(UnrealAgent):

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 situations=[], instance_of=[], mappings=[],
                 arity=0, arguments=[], justifications=[], inhibitions=[]):
        
        UnrealAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links,
                             threshold, level_of_activation, speed_of_change, argument_of, part_of, has_parts,
                             situations, instance_of, mappings, justifications, inhibitions)
        self.arity = arity
        self.predicate = self
        self.arguments = arguments

    def describe_itself(self):
        UnrealAgent.describe_itself(self)
        print("The arity of the relation is: {}".format(self.arity))
        print("The predicate of the relation is: {}".format(self.predicate))
        print("The arguments of the relation are: ", ", ".join(str(x) for x in self.arguments))


class UnrealInstanceAgent(UnrealAgent):

    def __init__(self, name, word="", comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 situations=[], instance_of=[],  mappings=[],  justifications=[],
                 inhibitions=[]):
        
        UnrealAgent.__init__(self, name, word, comment, agents_to_activate, incoming_links,
                             threshold, level_of_activation, speed_of_change, argument_of, part_of, has_parts,
                             situations, instance_of, mappings, justifications, inhibitions)

    def describe_itself(self):
        UnrealAgent.describe_itself(self)


# LINKS #
#########

class Link(object):
    # The superior class for all links.

    def __init__(self, sender, weight=initial_weight_for_links):

        self.sender = sender
        self.weight = weight


# REQUESTS #
############

class Request(object):
    # The main class/holder of all DUAL requests.

    def __init__(self, name, comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[], justifications=[], inhibitions=[]):
        
        self.name = name
        self.comment = comment
        self.agents_to_activate = agents_to_activate
        self.incoming_links = incoming_links
        self.threshold = threshold
        self.level_of_activation = level_of_activation
        self.speed_of_change = speed_of_change
        self.argument_of = argument_of
        self.part_of = part_of
        self.has_parts = has_parts
        self.justifications = justifications
        self.inhibitions = inhibitions
        # When a request is created, it is automatically added to the global variable list_of_all_requests.
        variables.list_of_all_requests = variables.list_of_all_requests + [self]

    def __repr__(self):
        return self.name

    def describe_itself(self):
        print("The name of the request is '{}' and its type is {}.".format(self.name, self.__class__.__name__))
        print("Comment: {}".format(self.comment))
        print("Threshold: {}".format(self.threshold))
        print("Activation level: {}".format(self.level_of_activation))
        print("Speed of change: {}".format(self.speed_of_change))
        incoming_links = ""
        for link in self.incoming_links:
            incoming_links = incoming_links + "(" + link.sender.name + " weight " + str(link.weight) + ") "
        print("Incoming links: ", incoming_links)
        print("Outgoing links: ", ', '.join(str(x) for x in self.agents_to_activate))
        print("Part of: ", ', '.join(str(x) for x in self.part_of))
        print("Has_parts: ", ', '.join(str(x) for x in self.has_parts))
        print("Argument_of: ", ', '.join(str(x) for x in self.argument_of))
        print("Justifications: ", ", ".join(str(x) for x in self.justifications))
        print("Inhibits: ", ", ".join(str(x) for x in self.inhibitions))


class MappingRequest (Request):
    
    def __init__(self, name, comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 superclasses=[], justifications=[], inhibitions=[],
                 target_instance=[], base_instance=[]):
        
        Request.__init__(self, name, comment, agents_to_activate, incoming_links,
                         threshold, level_of_activation, speed_of_change,
                         argument_of, part_of, has_parts, justifications, inhibitions)
        
        self.superclasses = superclasses
        self.target_instance = target_instance
        self.base_instance = base_instance

    def describe_itself(self):
        Request.describe_itself(self)
        print("Superclasses: ", ", ".join(str(x) for x in self.superclasses))
        print("Target_instance: ", ", ".join(str(x) for x in self.target_instance))
        print("Base_instance: ", ", ".join(str(x) for x in self.base_instance))


class InstanceAnticipationRequest (Request):
    
    def __init__(self, name, comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 situations=[], instance_of=[],  mappings=[], justifications=[], inhibitions=[]):
        
        Request.__init__(self, name, comment, agents_to_activate, incoming_links,
                         threshold, level_of_activation, speed_of_change,
                         argument_of, part_of, has_parts, justifications, inhibitions)

        self.situations = situations
        self.instance_of = instance_of
        self.mappings = mappings

    def describe_itself(self):
        Request.describe_itself(self)
        print("Situations: ", ", ".join(str(x) for x in self.situations))
        print("Instance_of: ", ", ".join(str(x) for x in self.instance_of))
        print("Mappings: ", ", ".join(str(x) for x in self.mappings))


class RelationInstanceAnticipationRequest (Request):
    
    def __init__(self, name, comment="", agents_to_activate=[], incoming_links=[],
                 threshold=threshold_agent_activation,
                 level_of_activation=initial_agent_activation,
                 speed_of_change=default_speed_of_change,
                 argument_of=[], part_of=[], has_parts=[],
                 situations=[], instance_of=[], mappings=[], justifications=[],
                 inhibitions=[], arity=0, arguments=[]):
        
        Request.__init__(self, name, comment, agents_to_activate, incoming_links,
                         threshold, level_of_activation, speed_of_change,
                         argument_of, part_of, has_parts, justifications, inhibitions)

        self.situations = situations
        self.instance_of = instance_of
        self.mappings = mappings
        self.arity = arity
        self.arguments = arguments

    def describe_itself(self):
        Request.describe_itself(self)
        print("Situations: ", ", ".join(str(x) for x in self.situations))
        print("Instance_of: ", ", ".join(str(x) for x in self.instance_of))
        print("Mappings: ", ", ".join(str(x) for x in self.mappings))
        print("The arity of the relation is: {}".format(self.arity))
        print("The arguments of the relation are: ", ", ".join(str(x) for x in self.arguments))
        
# END OF FILE: classes.py #
