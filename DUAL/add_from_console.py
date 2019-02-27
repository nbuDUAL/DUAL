
from agents_manipulation import *

# TO DO: FIX the add_agent_from_console() functions.



def add_agent_from_console():
    name = input("The name of the agent is: ")
    while not (check_for_free_name(name)):
        name = input("There is already an agent with such a name. The name of the agent is: ")
    agent_type = input("The type of the agent is: ")
    while not (agent_type in ["ConceptAgent", "RelationConceptAgent", "Instancegent", "RelationInstanceAgent"]):
        agent_type = input(
            """
INVALID TYPE! The agent's type should be one of the following - 
ConceptAgent, RelationConceptAgent, InstanceAgent, RelationInstanceAgent. The type of the agent is:
            """
            )
    if agent_type == "ConceptAgent":
        new_agent = add_agent(name=name, agent_type=ConceptAgent, word=name)
    elif agent_type == "RelationConceptAgent":
        new_agent = add_agent(name=name, agent_type=RelationConceptAgent, word=name)
    elif agent_type == "InstanceAgent":
        new_agent = add_agent(name=name, agent_type=InstanceAgent, word=name)
    else:
        new_agent = add_agent(name=name, agent_type=RelationInstanceAgent, word=name)
    new_agent.comment = input("The comment is: ")
    threshold = input("The threshold is: ")
    if threshold:
        new_agent.threshold = threshold
    level_of_activation = input("Level of activation is: ")
    if level_of_activation:
        new_agent.level_of_activation = level_of_activation
    if (agent_type == "ConceptAgent") or (agent_type == "RelationConceptAgent"):
        superclass = input("The superclass is: ")
        if superclasses:
            new_agent.superclasses = [find_agent(superclass)]
        subclass = input("The subclasses are: ")
        if subclass:
            new_agent.subclasses = [find_agent(subclasses)]
    if (agent_type == "RelationConceptAgent") or (agent_type == "RelationInstanceAgent"):
        arity = input("The arity is: ")
        if arity:
            new_agent.arity = arity
        else:
            arity = input("Arity is needed: ")
            new_agent.arity = arity
        for i in range(int(arity)):
            argument = input("Argument {} is: ".format(i+1))
            new_agent.arguments = new_agent.arguments + [argument]
    return new_agent



