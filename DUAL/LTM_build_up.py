
################
# LTM build up #
################


# DEFINES FUNCTIONS FOR BUILDING DUAL's LTM
# BASED ON THE ONTOLOGIES: WordNet and PropBank.
# PROGRAMERS: Yolina Petrova, YEAR 2018
# Last updated: Yolina Petrova, January, 2019

#####################
# External protocol #
#####################

"""
The DUAL's LTM is based on two onthologies: WordNet and PropBank.

load_knowledge() --> loads into DUAL the LTM knowledge following the creation algorithm:
    1. Turns the predicates from PropBank into RelationConceptAgents and their corresponding arguments into ConceptAgents.
    2. Connects the relations with the verbs from WordNet.                                                                 
        (while checking the super and subclasses of the verbs, check if they do not exist as relations already!)
    3. Connect the arguments (all of which are nouns) with WordNet and turn their direct neighbours into ConceptAgents.   
    4. Turn the rest of the WordNet's nouns into ConceptAgents.
    5. Turn the rest of the WordNet's verbs into ConceptAgents.
    6. Tutns the adjectives from WordNet into ConceptAgents.

"""

from main_cycle import *
from nltk.corpus import wordnet as wn
from nltk.corpus import propbank as pb

# import dual_parser
# import nltk - add it when you use Lematize (probably when dual parser is ON
# and the user should point to the right meaning of a word)


"""

### CHECK TO DO:

# use the documented part of connect_pb_args_to_wn()
--> for the cases when the user should point to the right meaning of a word
(for example when the dual_parser part is added)

connect_pb_rels_to_wn()
--> make sure that indeed the right meaning is chosen (if it is not a completely exact match)

# Fix the Adding argument_of/CAUSES relations part.
    #add_causes(synset, relation)

# substance_holonym() fix --> maybe this is something like made of?

check if there is a relation opposite_rel and MADE_of_rel.
If there is, turn it into the superclass of all opposite and made_of relations.
think about causes as well!!!

1 - There is no opposite_rel --> create it manually.
3 - cause?
2 - made_of?

"""

def activation_test():
    # After the ontology knowledge is loaded in DUAL,
    # Boy feeds a cat and Girl feeds a dog are established as two episodic situations.
    # Girl feeds a dog is setas input. Through cycles(n), one can trace how the activation
    # as well as the rest of the model's processes together with the ontology knowledge.
    add_agent("boy_1", agent_type=InstanceAgent, instance_of=[find_agent("boy_n")])
    add_agent("cat_1", agent_type=InstanceAgent, instance_of=[find_agent("cat_n")])
    add_agent("feed_1", agent_type=RelationInstanceAgent, instance_of=[find_agent("feed_rel")],
              arguments=[find_agent("boy_1"), find_agent("cat_1")])
    
    add_agent("girl_2", agent_type=InstanceAgent, instance_of=[find_agent("girl_n")])
    add_agent("dog_2", agent_type=InstanceAgent, instance_of=[find_agent("dog_n")])
    add_agent("feed_2", agent_type=RelationInstanceAgent, instance_of=[find_agent("feed_rel")],
              arguments=[find_agent("girl_2"), find_agent("dog_2")])
    add_to_input(find_agent("feed_2"))

    

def construct_ontology_knowledge():
    # Loads and connects the LTM knowledge from PropBank and WordNet.
    # First, it initializes DUAL so it could be ready.
    initialize_dual()
    load_relations()
    connect_pb_rels_to_wn()
    connect_pb_args_to_wn()
    load_rest_of_the_wn_nouns()
    load_rest_of_the_wn_verbs()
    load_rest_of_the_wn_adjectives()
    save_kb_to_file("LT_knowledge_with_ADJ.csv")

# The knowledge can be loaded thrugh the function from agent_manipulation.py:
# load_kb_from_file("LT_knowledge_with_ADJ.csv")
# This takes around 30 seconds,
# compared to the KB construction every single time, which takes several minutes.


LOADED_RELATIONS = []
LOADED_SYNSETS = []


def load_relations():
    # Loads the predicates knowledge from PropBank.
    # Adds the predicate's exact name as a word, while the agent's name ends with "_rel".
    # Adds the predicate's definition as a comment.
    global LOADED_RELATIONS
    for relation in pb.rolesets():
        # Makes sure there are no two relations with the same meaning.
        if relation.attrib['id'][:-3] not in LOADED_RELATIONS:
            arguments = []
            rel_args = []
            if len(relation.findall("roles/role")) > 3:
                rel_args = relation.findall("roles/role")[:2]
            else:
                rel_args = relation.findall("roles/role")
            for arg in rel_args:
                if arg.attrib['descr'] in variables.all_agents.keys():
                    # In cases the argument has the same name as an existing agent, adds that agent as an argument,
                    if isinstance(find_agent(arg.attrib['descr']), ConceptAgent):
                        arguments = arguments + [find_or_create_concept_from_pb(arg.attrib['descr'], relation.attrib['id'][:-3])]
                    else:
                        print("What else - {} is an argument of the relation: {}.".format(arg.attrib['descr'],
                                                                                          relation.attrib['id']))
                else:
                    arguments = arguments + [find_or_create_concept_from_pb(arg.attrib['descr'], relation.attrib['id'][:-3])]
            new_agent = add_agent(name="{}_rel".format(relation.attrib['id'][:-3]),
                                  agent_type=RelationConceptAgent,
                                  word=relation.attrib['id'][:-3],
                                  comment=relation.attrib['name'],
                                  arguments=arguments, arity = len(arguments))
            LOADED_RELATIONS = LOADED_RELATIONS + [relation.attrib['id'][:-3]]


def connect_pb_rels_to_wn():
    relations = [x for x in variables.all_agents.values() if isinstance(x, RelationConceptAgent)]
    for relation in relations:
        # First, check the exact lemma of the argument.
        pos_exact_match = wn.synsets(relation.name[:-4], 'v')
        if pos_exact_match:
            if pos_exact_match[0].name()[:-5] == relation.name[:-4]:
                # Adjust with WordNet's relations.
                adjust_rels_with_wn_info(pos_exact_match[0], relation)
            else:
                #print("WN thinks there is an EXACT match between WN: {} and PB: {}".format(pos_exact_match[0].name(), relation))
                #print("{} means: {}".format(pos_exact_match[0], pos_exact_match[0].definition()))
                #answer = input("If that applies, please write down: yes ")
                #if answer == "yes":
                # Adjust with WordNet's relations.
                adjust_rels_with_wn_info(pos_exact_match[0], relation)


def adjust_rels_with_wn_info(synset, relation):
    global LOADED_SYNSETS
    # Adding the IS_A/SUPERCLASSES relations.
    for hypernym in synset.hypernyms():
        if ".01" in hypernym.name() and hypernym.name()[:-5] != relation.name[:-4]:
            hypernym_rel_name = "{}_rel".format(hypernym.name()[:-5])
            hypernym_verb_name = "{}_v".format(hypernym.name()[:-5])
            if get_agent(hypernym_rel_name) == False and get_agent(hypernym_verb_name) == False:
                add_agent(hypernym_verb_name, agent_type=ConceptAgent, word=hypernym.name()[:-5],
                          comment=synset.definition(), subclasses = [relation])
            elif get_agent(hypernym_rel_name) != False:
                add_in_slot(relation, "superclasses", find_agent(hypernym_rel_name))
            else:
                add_in_slot(relation, "superclasses", find_agent(hypernym_verb_name))
    # Adding the SUBCLASSES relations.
    for hyponym in synset.hyponyms():
        if ".01" in hyponym.name() and hyponym.name()[:-5] != relation.name[:-4]:
            hyponym_rel_name = "{}_rel".format(hyponym.name()[:-5])
            hyponym_verb_name = "{}_v".format(hyponym.name()[:-5])
            if get_agent(hyponym_rel_name) == False and get_agent(hyponym_verb_name) == False:
                add_agent(hyponym_verb_name, agent_type=ConceptAgent, word=hyponym.name()[:-5],
                          comment=synset.definition(), superclasses = [relation])
            elif get_agent(hyponym_rel_name) != False:
                add_in_slot(relation, "subclasses", find_agent(hyponym_rel_name))
            else:
                add_in_slot(relation, "subclasses", find_agent(hyponym_verb_name))
    # Adding the HAS_PARTS relations.
    for ent in synset.entailments():
        ent_name_rel_name = "{}_rel".format(ent.name()[:-5])
        ent_name_verb_name = "{}_v".format(ent.name()[:-5])
        if get_agent(ent_name_rel_name) == False and get_agent(ent_name_verb_name) == False:
            add_agent(ent_name_verb_name, agent_type=ConceptAgent,
                      word=ent.name()[:-5], comment=synset.definition(), part_of=[relation])
        elif get_agent(ent_name_rel_name) != False:
            if relation != find_agent(ent_name_rel_name):
                if find_agent(ent_name_rel_name) not in relation.superclasses:
                    if find_agent(ent_name_rel_name) not in relation.part_of:
                        if find_agent(ent_name_rel_name) not in relation.subclasses:
                            add_in_slot(relation, "has_parts", find_agent(ent_name_rel_name))
        else:
            if find_agent(ent_name_verb_name) not in relation.subclasses:
                add_in_slot(relation, "has_parts", find_agent(ent_name_verb_name))
    # Adding argument_of/CAUSES relations.
    #add_causes(synset, relation)
    LOADED_SYNSETS = LOADED_SYNSETS + [synset.name()[:-5]]
    

def find_or_create_concept_from_pb(roleset, relation):
    # If ROLESET does not exist as an agent, create and return it,
    # otherwhise, find the agent and return it.
    # Take into account some human-made patterns.
    argument_name = ""
    if str(roleset) == "agent, causer" or str(roleset) == "causer, agent" or\
    str(roleset) == "agent" or str(roleset) == "causal agent" or "causer" in str(roleset) or "agent" in str(roleset):
        if relation[-1] == "e":
            argument_name = "{}r_n".format(relation)
        else:
            argument_name = "{}er_n".format(relation)
    if "(s)" in roleset:
        argument_name = "{}_n".format(roleset.replace("(s)", ""))
    if not argument_name:
        argument_name = "{}_n".format(roleset)
    if get_agent(argument_name) == False:
        new_agent = add_agent(argument_name, agent_type=ConceptAgent, word=argument_name[:-2])
    else:
        new_agent = find_agent(argument_name)
    return new_agent


def find_or_create_concept_from_wn(synset):
    # If ROLESET does not exist as an agent, create and return it,
    # otherwhise, find the agent and return it.
    # Take into account some human-made patterns.
    argument_name = "{}_n".format(synset.name()[:-5])
    if get_agent(argument_name) == False:
        new_agent = add_agent(argument_name, agent_type=ConceptAgent,
                              word=argument_name[:-2], comment=synset.definition())
    else:
        new_agent = find_agent(argument_name)
    return new_agent


def find_or_create_verb_from_wn(synset):
    # If SYNSET does not exist as an agent, create and return it,
    # otherwhise, find the agent and return it.
    rel_name = "{}_rel".format(synset.name()[:-5])
    verb_name = "{}_v".format(synset.name()[:-5])
    if get_agent(rel_name) == False:
        if get_agent(verb_name) == False:
            new_agent = add_agent(rel_name, agent_type=ConceptAgent,
                                  word=verb_name[:-2], comment=synset.definition())
        else:
            new_agent = find_agent(verb_name)
    else:
        new_agent = find_agent(rel_name)
    return new_agent


def connect_pb_args_to_wn():
    # Connects the relation arguments existing as dual agents and adjust them to WordNet information.
    relations = [x for x in variables.all_agents.values() if isinstance(x, RelationConceptAgent)]
    for relation in relations:
        for argument in relation.arguments:
            # First, check the exact lemma of the argument.
            pos_exact_match = wn.synsets(argument.name[:-2], 'n')
            if pos_exact_match:
                if pos_exact_match[0].name()[:-5] == argument.name[:-2]:
                    # Adjust with WordNet's relations.
                    adjust_args_with_wn_info(pos_exact_match[0], argument)
                else:
                    #print("WN thinks there is an EXACT match between WN: {} and PB: {}".format(pos_exact_match[0].name(), argument))
                    #print("{} means: {}".format(pos_exact_match[0], pos_exact_match[0].definition()))
                    #answer = input("If that applies, please write down: yes ")
                    #if answer == "yes":
                    if True:
                        # Adjust with WordNet's relations.
                        adjust_args_with_wn_info(pos_exact_match[0], argument)


def adjust_args_with_wn_info(synset, argument):
    # Adjust ARGUMENT which is a Dual agent with the WordNet knowledge of SYNSET.
    # Adds the definition of the SYNSET as the argument's comment. 
    global LOADED_SYNSETS
    add_hypernyms(synset, argument)
    add_hyponyms(synset, argument)
    add_part_ofs(synset, argument)
    add_has_parts(synset, argument)
    add_made_ofs(synset, argument)
    argument.comment = synset.definition()
    LOADED_SYNSETS = LOADED_SYNSETS + [synset.name()[:-5]]


def load_rest_of_the_wn_nouns():
    # Loads the concept knowledge of nouns.
    # Adds the concept's definition as a comment.
    global LOADED_SYNSETS
    for synset in list(wn.all_synsets('n')):
        # Each lemma is processed only as the most probable synset.
        if synset.name()[:-5] not in LOADED_SYNSETS and ".01" in synset.name():
            new_agent = find_or_create_concept_from_wn(synset)
            # Adding the IS_A/SUPERCLASSES relations.
            add_hypernyms(synset, new_agent)
            # Adding the SUBCLASSES relations.
            add_hyponyms(synset, new_agent)
            # Adding the PART_OF relations.
            add_part_ofs(synset, new_agent)
            # Adding the HAS_PARTS relations.
            add_has_parts(synset, new_agent)
            # Adding the MADE_OF relations.
            add_made_ofs(synset, new_agent)
            LOADED_SYNSETS = LOADED_SYNSETS + [synset.name()[:-5]]


def load_rest_of_the_wn_verbs():
    # Loads the rest of the concept's knowledge of verbs.
    # Adds the concept's definition as a comment.
    global LOADED_SYNSETS
    for synset in list(wn.all_synsets('v')):
        # Each lemma is processed only as the most probable synset.
        if synset.name()[:-5] not in LOADED_SYNSETS and ".01" in synset.name():
            new_agent = find_or_create_verb_from_wn(synset)
            # Adding the IS_A/SUPERCLASSES relations.
            add_hypernyms(synset, new_agent)
            # Adding the SUBCLASSES relations.
            add_hyponyms(synset, new_agent)
            # Adding the HAS_PARTS relations.
            add_verb_has_parts(synset, new_agent)
            # Adding argument_of/CAUSES relations.
            #add_causes(synset, new_agent)
            LOADED_SYNSETS = LOADED_SYNSETS + [synset.name()[:-5]]


def load_rest_of_the_wn_adjectives():
    # Loads the concept knowledge of adjectives.
    # Adds the concept's definition as a comment.
    # If the synset is an adjective.
    for synset in list(wn.all_synsets('a')):
        agent_synset_name = "{}_a".format(synset.lemma_names()[0])
        if get_agent(agent_synset_name) == False:
            new_agent = add_agent(agent_synset_name, agent_type=ConceptAgent,
                                  word=synset.lemma_names()[0],
                                  comment=synset.definition())
            if synset.lemmas()[0].antonyms(): # If the adj has any antonyms.
                antonym_name = "{}_a".format(synset.lemmas()[0].antonyms()[0].name())
                if get_agent(antonym_name) == False:
                    antonym = add_agent(antonym_name, agent_type=ConceptAgent,
                                        word=synset.lemmas()[0].antonyms()[0].name(),
                                        comment=synset.definition())
                else:
                    antonym = find_agent(antonym_name)
                rel_name = "{}_opposite".format(agent_synset_name)
                add_agent(rel_name, agent_type=RelationConceptAgent,
                          word=rel_name, comment=synset.definition(),
                          arguments=[new_agent, antonym])
    # If the synset is a satelite adjective.
    for synset in list(wn.all_synsets('s')):
        agent_synset_name = "{}_a".format(synset.lemma_names()[0])
        if get_agent(agent_synset_name) == False:
            new_agent = add_agent(agent_synset_name, agent_type=ConceptAgent,
                                  word=synset.lemma_names()[0],
                                  comment=synset.definition())
            if synset.lemmas()[0].antonyms(): # If the adj has any antonyms.
                antonym_name = "{}_a".format(synset.lemmas()[0].antonyms()[0].name())
                if get_agent(antonym_name) == False:
                    antonym = add_agent(antonym_name, agent_type=ConceptAgent,
                                        word=synset.lemmas()[0].antonyms()[0].name(),
                                        comment=synset.definition())
                else:
                    antonym = find_agent(antonym_name)
                rel_name = "{}_opposite".format(agent_synset_name)
                add_agent(rel_name, agent_type=RelationConceptAgent,
                          word=rel_name, comment=synset.definition(),
                          arguments=[new_agent, antonym])


def add_hypernyms(synset, new_agent):
    # Adds all hypernyms of SYNSET as superclasses of NEW_AGENT.
    # If some of the hypernyms does not exist as an agent, create it.
    for hypernym in synset.hypernyms():
        hypernym_name = "{}_n".format(hypernym.name()[:-5])
        if get_agent(hypernym_name) == False:
            add_agent(hypernym_name, agent_type=ConceptAgent, word=hypernym.name()[:-5],
                      comment=synset.definition(), subclasses = [new_agent])
        elif new_agent.name != hypernym_name:
            add_in_slot(new_agent, "superclasses", find_agent(hypernym_name))
        else:
            pass
    if synset._pos == 'n':
        for ins_hypernym in synset.instance_hypernyms():
            ins_hypernym_name = "{}_n".format(ins_hypernym.name()[:-5])
            if get_agent(ins_hypernym_name) == False:
                add_agent(ins_hypernym_name, agent_type=ConceptAgent, word=ins_hypernym.name()[:-5],
                          comment=synset.definition(), subclasses = [new_agent])
            else:
                add_in_slot(new_agent, "superclasses", find_agent(ins_hypernym_name))
    
    
def add_hyponyms(synset, new_agent):
    # Adds all hyponyms of SYNSET as subclasses of NEW_AGENT.
    # If some of the hyponyms does not exist as an agent, create it.
    for hyponym in synset.hyponyms():
        hyponym_name = "{}_n".format(hyponym.name()[:-5])
        if get_agent(hyponym_name) == False:
            add_agent(hyponym_name, agent_type=ConceptAgent, word=hyponym.name()[:-5],
                      comment=synset.definition(), superclasses = [new_agent])
        elif new_agent.name != hyponym_name:
            add_in_slot(new_agent, "subclasses", find_agent(hyponym_name))
        else:
            pass
    if synset._pos == 'n':
        for ins_hyponym in synset.instance_hyponyms():
            ins_hyponym_name = "{}_n".format(ins_hyponym.name()[:-5])
            if get_agent(ins_hyponym_name) == False:
                add_agent(ins_hyponym_name, agent_type=ConceptAgent, word=ins_hyponym.name()[:-5],
                          comment=synset.definition(), superclasses = [new_agent])
            else:
                add_in_slot(new_agent, "subclasses", find_agent(ins_hyponym_name))


def add_part_ofs(synset, new_agent):
    # Adds all "part of" links of SYNSET as part of of NEW_AGENT.
    # If a part of does not exist as an agent, create it.
    for part_holonym in synset.part_holonyms():
        part_holonym_name = "{}_n".format(part_holonym.name()[:-5])
        if get_agent(part_holonym_name) == False:
            #print("1 - Adding: {} as part_of: {}.".format(new_agent, part_holonym_name))
            add_agent(part_holonym_name, agent_type=ConceptAgent, word=part_holonym.name()[:-5],
                      comment=synset.definition(), has_parts=[new_agent])
        elif new_agent.name != part_holonym_name:
            #print("2 - Adding: {} as part_of: {}.".format(new_agent, part_holonym_name))
            add_in_slot(new_agent, "part_of", find_agent(part_holonym_name))
        else:
            pass
    for member_holonym in synset.member_holonyms():
        member_holonym_name = "{}_n".format(member_holonym.name()[:-5])
        if get_agent(member_holonym_name) == False:
            #print("3 - Adding: {} as part_of: {}.".format(new_agent, member_holonym_name))
            add_agent(member_holonym_name, agent_type=ConceptAgent, word=member_holonym.name()[:-5],
                      comment=synset.definition(), has_parts=[new_agent])
        elif new_agent.name != member_holonym_name:
            #print("4 - Adding: {} as part_of: {}.".format(new_agent, member_holonym_name))
            add_in_slot(new_agent, "part_of", find_agent(member_holonym_name))
        else:
            pass
    """
    for substance_holonym in synset.substance_holonyms():
        #print("S synset: ", synset, "substance_holonym: ", substance_holonym)
        substance_holonym_name = substance_holonym.name()[:-5]
        if get_agent(substance_holonym_name) == False:
            add_agent(substance_holonym_name, agent_type=ConceptAgent,
                      comment=synset.definition(), part_of=[new_agent])
        else:
            add_in_slot(new_agent, "part_of", find_agent(substance_holonym_name))
    """


def add_has_parts(synset, new_agent):
    for part_meronym in synset.part_meronyms():
        part_meronym_name = "{}_n".format(part_meronym.name()[:-5])
        if get_agent(part_meronym_name) == False:
            add_agent(part_meronym_name, agent_type=ConceptAgent, word=part_meronym.name()[:-5],
                      comment=synset.definition(), part_of=[new_agent])
        elif new_agent.name != part_meronym_name:
            add_in_slot(new_agent, "has_parts", find_agent(part_meronym_name))
        else:
            pass


def add_made_ofs(synset, new_agent):
    for substance_meronym in synset.substance_meronyms():
        substance_meronym_name = "{}_n".format(substance_meronym.name()[:-5])
        if get_agent(substance_meronym_name) == False:
            made_of = add_agent(substance_meronym_name, agent_type=ConceptAgent,
                                word=substance_meronym.name()[:-5],
                                comment=synset.definition())
            rel_name = "{}_made_of_rel".format(substance_meronym_name)
            add_agent(rel_name, agent_type=RelationConceptAgent,
                  comment=synset.definition(), arguments=[new_agent, made_of])
        else:
            pass


def add_causes(synset, new_agent):
    for cause in synset.causes():
        cause_name = cause.name()[:-5]
        if get_agent(cause_name) == False:
            caused = add_agent(cause_name, agent_type=ConceptAgent,
                               word=cause.name()[:-5],
                               comment=synset.definition())
            rel_name = "{}_causes_rel".format(cause_name)
            add_agent(rel_name, agent_type=RelationConceptAgent,
                      comment=synset.definition(), arguments=[new_agent, caused])
        else:
            pass
            

def add_verb_has_parts(synset, new_agent):
    for ent in synset.entailments():
        ent_name = ent.name()[:-5]
        if get_agent(ent_name) == False:
            add_agent(ent_name, agent_type=ConceptAgent,
                      word=ent.name()[:-5],
                      comment=synset.definition(), part_of = [new_agent])
        else:
            add_in_slot(new_agent, "has_parts", find_agent(ent_name))
            

"""
### FOR DUAL_PARSER!
def pb_check(input):
    # The function checks if the INPUT relation exist in the PropBank ontology.
    pb_results = []
    try:
        pb_results = pb.rolesets(input)
    except ValueError:
        print("'{}' is not in PropBank --> it is a new agent.".format(input))
    if pb_results:
        # Extracts only the first result as it is the most probable one.
        print("PropBank result: ", pb_results[0].attrib['id'])
        for role in pb_results[0].findall("roles/role"):
            print(role.attrib['descr'])
            wn_argument_check(role.attrib['descr'],
                              nltk.stem.WordNetLemmatizer().lemmatize(role.attrib['descr'], 'n'))


def descr_pr_from_pb(input):
    p = pb.rolesets(input)
    for pr in p:
        arguments = []
        for arg in pr.findall("roles/role"):
            arguments = arguments + [arg.attrib['descr']]
        print("PREDICATE: ", pr.attrib['id'],
              "DEFINITION: ", pr.attrib['name'], "ARGs: ", arguments)

        
def wn_argument_check(argument, lematized_arg):
    possible_synsets_1 = wn.synsets(argument, 'n')
    syn_1 = []
    for pos_1 in possible_synsets_1:
        if pos_1.name()[:-5] == lematized_arg:
            syn_1 = pos_1
            break
    if syn_1:
        print("         WordNet Argument: ", syn_1, " - definition: ", syn_1.definition())
    else:
        print("'{}' is not in WordNet.".format(argument))


def check_predicate(sentence="John loves Marry."):
    dual_parser.predicate(sentence)
    # For every predicate strucutre extracted through the predicate(sentence) function
    # and stored in the global PREDICATES_LIST, check if the relations and their corresponding arguments
    # cn be found in the PropBank and WordNet.
    for p in dual_parser.PREDICATES_LIST:
        print("Predicate structure: ", p)
        # nltk.stem.WordNetLemmatizer() turns RELATION into its basic form.
        relation = nltk.stem.WordNetLemmatizer().lemmatize(p.relation, 'v')
        print("Relation: ", p.relation, "; Lemmatized: ", relation)
        pb_check(relation)
        # nltk.stem.WordNetLemmatizer() turns ARGUMENT_1 into its basic form.
        arg_1 = nltk.stem.WordNetLemmatizer().lemmatize(p.argument_1.lower(), 'n')
        print("Argument 1: ", p.argument_1, "; Lemmatized: ", arg_1)
        wn_argument_check(p.argument_1, arg_1)
        # nltk.stem.WordNetLemmatizer() turns ARGUMENT_2 into its basic form.
        arg_2 = nltk.stem.WordNetLemmatizer().lemmatize(p.argument_2.lower(), 'n')
        print("Argument 2: ", p.argument_2, "; Lemmatized: ", arg_2)
        wn_argument_check(p.argument_2, arg_2)
        print()


def find_or_create_from_wn(synset):
    # If SYNSET does not exist as an agent, create and return it,
    # otherwhise, find the agent and return it.
    agent_synset_name = "{}_n".format(synset.name()[:-5])
    if get_agent(agent_synset_name) == False:
        new_agent = add_agent(agent_synset_name, agent_type=ConceptAgent,
                              word=agent_synset_name,
                              comment=synset.definition())
    else:
        new_agent = find_agent(agent_synset_name)
    return new_agent

       
def verb_into_noun(verb):
    # Transforms VERB to the closest noun, which has the synset 'person.n.01' upper in its hiearchy.
    # Verb should be a string.
    
    #verb_into_noun("love")
    #--> {Synset('beloved.n.01'), Synset('fan.n.03'), Synset('lover.n.01'), Synset('lover.n.03')}
    
    set_of_related_nouns = set()
    for lemma in wn.lemmas(wn.morphy(verb, wn.VERB), pos="v"):
        for related_form in lemma.derivationally_related_forms():
            for synset in wn.synsets(related_form.name(), pos=wn.NOUN):
                if wn.synset('person.n.01') in synset.closure(lambda s:s.hypernyms()):
                    set_of_related_nouns.add(synset)

    return set_of_related_nouns


WN_NOUN = 'n'
WN_VERB = 'v'
WN_ADJECTIVE = 'a'
WN_ADJECTIVE_SATELLITE = 's'
WN_ADVERB = 'r'
def convert(word, from_pos, to_pos):    
    # Transforms words from/to the POS tags (i.e., from WN_NOUN to WN_VERB; from 'n' to 'v').
    
    #convert("story", WN_NOUN, WN_VERB)
    #--> [('report', 0.2222222222222222), ('tell', 0.2222222222222222), ('narrate', 0.2222222222222222),...]

    #convert("love", WN_VERB, WN_NOUN)
    #--> [('love', 0.4), ('lover', 0.24), ('enjoyment', 0.08), ('fucking', 0.04), ('bed', 0.04),
    #('screwing', 0.04), ('enjoyer', 0.04), ('fuck', 0.04), ('fucker', 0.04), ('screw', 0.04)]

    synsets = wn.synsets(word, pos=from_pos)
 
    # If there is no such word, returns an empty list.
    if not synsets:
        return []
 
    # Get all lemmas of the word (and consider 'a' and 's' equivalent).
    lemmas = [l for s in synsets
                for l in s.lemmas() 
                if s.name().split('.')[1] == from_pos
                    or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
                        and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]
 
    # Get the related forms of the lemmas.
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]
 
    # Filter only the desired pos (and consider 'a' and 's' equivalent)
    related_noun_lemmas = [l for drf in derivationally_related_forms
                             for l in drf[1] 
                             if l.synset().name().split('.')[1] == to_pos
                                or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
                                    and l.synset.name.split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]
 
    # Extract the words from the lemmas.
    words = [l.name() for l in related_noun_lemmas]
    len_words = len(words)
 
    # Build the result in the form of a list containing tuples (word, probability).
    result = [(w, float(words.count(w))/len_words) for w in set(words)]
    result.sort(key=lambda w: -w[1])
    final_result = []
    for r in result:
        final_result = final_result + [r[0]]
    # Return all possibilities sorted by probability.
    return final_result


def load_relations_old():
    # Loads the predicates knowledge from PropBank.
    # Adds the predicate's exact name as a word, while the agent's name ends with "_rel".
    # Adds the predicate's definition as a comment.
    global LOADED_RELATIONS
    global DOUBLED
    for relation in pb.rolesets():
        if relation.attrib['id'][:-3] not in LOADED_RELATIONS:
            new_agent = add_agent(name="{}_rel".format(relation.attrib['id'][:-3]),
                                  agent_type=RelationConceptAgent,
                                  word=relation.attrib['id'][:-3],
                                  comment=relation.attrib['name'])
            LOADED_RELATIONS = LOADED_RELATIONS + [relation.attrib['id'][:-3]]
        else:
            DOUBLED = DOUBLED + [relation.attrib['id']]
    for relation in pb.rolesets():
        if relation.attrib['id'] not in DOUBLED and relation.attrib['id'][:-3] in LOADED_RELATIONS:
            arguments = []
            for arg in relation.findall("roles/role"):
                if arg.attrib['descr'] in variables.all_agents.keys():
                    # In cases the argument has the same name as an existing relation,
                    # adds the relation, but really, think which is the best thing to do here...
                    if isinstance(find_agent(arg.attrib['descr']), RelationConceptAgent):
                        arguments = arguments + [find_or_create_from_pb(arg.attrib['descr'])]
                    # If the argument is also argument of another relation, just add it to this one as well.
                    elif isinstance(find_agent(arg.attrib['descr']), ConceptAgent):
                        arguments = arguments + [find_or_create_from_pb(arg.attrib['descr'])]
                    else:
                        print("What else - {} is an argument of the relation: {}.".format(arg.attrib['descr'],
                                                                                          relation.attrib['id']))
                else:
                    arguments = arguments + [find_or_create_from_pb(arg.attrib['descr'])]
            for arg in arguments:
                add_in_slot(find_agent(relation.attrib['id'][:-3]), "arguments", arg)
                find_agent(relation.attrib['id'][:-3]).arity = len(arguments)
                

# Test functions:

problems_sup_itself = []
problems_sub_itself = []
problems_same_classes = []
problems_has_parts = []

def test():
    # Tests if there are cases in which the agent is its own superclsses, subclass, etc.
    global problems_sup_itself
    global problems_sub_itself
    global problems_same_classes
    global problems_has_parts
    load_relations()
    connect_pb_rels_to_wn()
    
    for a in variables.all_agents.values():
        if "_rel" in a.name:
            rel_stripped = a.name[:-4]
        else:
            rel_stripped = a.name[:-2]
        for sup in a.superclasses:
            if rel_stripped == sup.name[:-4] or rel_stripped == sup.name[:-2]:
                problems_sup_itself = problems_sup_itself + [a]
        for sub in a.subclasses:
            if rel_stripped == sub.name[:-4] or rel_stripped == sub.name[:-2]:
                problems_sub_itself = problems_sub_itself + [a]
                
        for sup in a.superclasses:
            if "_rel" in sup.name:
                sup_stripped = sup.name[:-4]
            else:
                sup_stripped = sup.name[:-2]
            for sub in a.subclasses:
                if sup_stripped == sub.name[:-4] or sup_stripped == sub.name[:-2]:
                    problems_same_classes = problems_same_classes + [a]
                    
        for part in a.has_parts:
            if "_rel" in part.name:
                part_stripped = part.name[:-4]
            else:
                part_stripped = part.name[:-2]
            if part_stripped == rel_stripped:
                #print("1")
                problems_has_parts = problems_has_parts + [a]
            for has_p in a.part_of:
                if part_stripped == has_p.name[:-4] or part_stripped == has_p.name[:-2]:
                    #print("2")
                    problems_has_parts = problems_has_parts + [a]
            for sup in a.superclasses:
                if part_stripped == sup.name[:-4]  or part_stripped == sup.name[:-2]:
                    #print("3")
                    problems_has_parts = problems_has_parts + [a]
            for sub in a.subclasses:
                if part_stripped == sub.name[:-4]  or part_stripped == sub.name[:-2]:
                    #print("4")
                    problems_has_parts = problems_has_parts + [a]
    print("problems_sup_itself: ", len(problems_sup_itself))
    print("problems_sub_itself: ", len(problems_sub_itself))
    print("problems_same_classes: ", len(problems_same_classes))
    print("problems_has_parts: ", len(problems_has_parts))


def connect_pb_args_to_wn():
    global LOADED_SYNSETS
    matched = []
    duble = []
    global semi_matched
    relations = [x for x in variables.all_agents.values() if isinstance(x, RelationConceptAgent)]
    for relation in relations:
        for argument in relation.arguments:
            # First, check the exact lemma of the argument.
            pos_exact_match = wn.synsets(argument.name[:-2], 'n')
            if pos_exact_match:
                if pos_exact_match[0].name()[:-5] == argument.name[:-2]:
                    # Adjust with WordNet's relations.
                    if argument not in matched:
                        adjust_args_with_wn_info(pos_exact_match[0], argument)
                        matched = matched + [argument]
                else:
                    #print("WN thinks there is an EXACT match between WN: {} and PB: {}".format(pos_exact_match[0].name(), argument))
                    #print("{} means: {}".format(pos_exact_match[0], pos_exact_match[0].definition()))
                    #answer = input("If that applies, please write down: yes ")
                    #if answer == "yes":
                    if True:
                        # Adjust with WordNet's relations.
                        if argument not in semi_matched:
                            adjust_args_with_wn_info(pos_exact_match[0], argument)
                            semi_matched = semi_matched + [argument]
    duble = [x for x in semi_matched if x in matched]
    print("Matched concepts: ", len(matched))
    print("Semi_matched concepts: ", len(semi_matched))
    print("DUBLE concepts: ", len(duble))
          
            # If there are no matches, check the lemmatized version.
            elif True:
                pos_lemmatized_match = nltk.stem.WordNetLemmatizer().lemmatize(argument.name[:-2].lower(), 'n')
                if pos_lemmatized_match != argument.name[:-2]:
                    pos_exact_match = wn.synsets(argument.name[:-2], 'n')
                    if pos_exact_match:
                        print("pos_lemmatized_matchfor arg: '{}' --- {} ".format(argument, pos_lemmatized_match))
                        print("{} means: {}".format(pos_exact_match[0], pos_exact_match[0].definition()))
                        answer = input("If that applies, please write down: yes ")
                        if answer == "yes":
                            # Adjust with WordNet's relations.
                            adjust_args_with_wn_info(pos_exact_match[0], argument)
                # If there are again no matches, propose possibilities based on the relation.
                # For PERSON upper in the hieararchy.
                pos_wn_person_arg = verb_into_noun(relation.name[:-4])
                if pos_wn_person_arg:
                    print("WN possible PERSON arguments: '{}' in DUAL for relation: {} --- {}.".format(argument,
                                                                                                       relation, pos_wn_person_arg))
                    answer = input("Is there a corresponding concept? Write down yes, if there is: ")
                    if answer == "yes":
                        arg = input("Please write down the exact synset: ")
                        re_name = input("How would you name the argument: ")
                        argument.name = re_name
                        # Adjust with WordNet's relations.
                        print("wn.synsets(arg, 'n') is: ", wn.synsets(arg, 'n'))
                        adjust_args_with_wn_info(wn.synset(arg), argument)
                # For other possibilities.
                pos_wn_arg = convert(relation.name, WN_VERB, WN_NOUN)
                if pos_wn_arg:
                    print("WN possiblity for argument: '{}' for relation: {} --- {}.".format(argument,
                                                                                             relation, pos_wn_arg))
                    answer = input("Is there a corresponding concept? Write down yes, if there is: ")
                    if answer == "yes":
                        arg = input("Please write down the exact synset: ")
                        re_name = input("How would you name the argument: ")
                        argument.name = re_name
                        # Adjust with WordNet's relations.
                        adjust_args_with_wn_info(wn.synsets(arg, 'n')[0], argument)
            else:
                print("Hello user! Would you like to add some info about the: {} -- with args: {}".format(relation, relation.arguments))
            print()
            print("---")
            print()


def load_nouns():
    # Loads the concept knowledge of nouns.
    # Adds the concept's definition as a comment.
    global LOADED_SYNSETS
    global LOADED_NOUNS
    for synset in list(wn.all_synsets('n')):
        # Each lemma is processed only as the most probable synset.
        if synset.name()[:-5] not in LOADED_SYNSETS:
            new_agent = find_or_create_from_wn(synset)
            # Adding the IS_A/SUPERCLASSES relations.
            add_hypernyms(synset, new_agent)
            # Adding the SUBCLASSES relations.
            add_hyponyms(synset, new_agent)
            # Adding the PART_OF relations.
            add_part_ofs(synset, new_agent)
            # Adding the HAS_PARTS relations.
            add_has_parts(synset, new_agent)
            # Adding the MADE_OF relations.
            add_made_ofs(synset, new_agent)
            LOADED_SYNSETS = LOADED_SYNSETS + [synset.name()[:-5]]
            LOADED_NOUNS = LOADED_NOUNS + [synset.name()[:-5]]


def load_verbs():
    # Loads the rest of the concept's knowledge of verbs.
    # Adds the concept's definition as a comment.
    global LOADED_SYNSETS
    for synset in list(wn.all_synsets('v')):
        # Each lemma is processed only as the most probable synset.
        if synset.name()[:-5] not in LOADED_SYNSETS:
            new_agent = find_or_create_from_wn(synset)
            # Adding the IS_A/SUPERCLASSES relations.
            add_hypernyms(synset, new_agent)
            # Adding the SUBCLASSES relations.
            add_hyponyms(synset, new_agent)
            # Adding the HAS_PARTS relations.
            add_verb_has_parts(synset, new_agent)
            # Adding argument_of/CAUSES relations.
            #add_causes(synset, new_agent)
            LOADED_SYNSETS = LOADED_SYNSETS + [synset.name()[:-5]]


def load_adjectives():
    # Loads the concept knowledge of adjectives.
    # Adds the concept's definition as a comment.
    # If the synset is an adjective.
    for synset in list(wn.all_synsets('a'))[0:2]:
        agent_synset_name = synset.lemma_names()[0]
        if get_agent(agent_synset_name) == False:
            new_agent = add_agent(agent_synset_name, agent_type=ConceptAgent,
                                  comment=synset.definition())
            if synset.lemmas()[0].antonyms(): # If the adj has any antonyms.
                if get_agent(synset.lemmas()[0].antonyms()[0].name()) == False:
                    antonym = add_agent(synset.lemmas()[0].antonyms()[0].name(), agent_type=ConceptAgent,
                                        comment=synset.definition())
                else:
                    antonym = find_agent(synset.lemmas()[0].antonyms()[0].name())
                rel_name = "{}_opposite".format(agent_synset_name)
                add_agent(rel_name, agent_type=RelationConceptAgent,
                          comment=synset.definition(), arguments = [new_agent, antonym])
    # If the synset is a satelite adjective.
    for synset in list(wn.all_synsets('s'))[0:2]:
        agent_synset_name = synset.lemma_names()[0]
        if get_agent(agent_synset_name) == False:
            new_agent = add_agent(agent_synset_name, agent_type=ConceptAgent,
                                  comment=synset.definition())
            if synset.lemmas()[0].antonyms(): # If the adj has any antonyms.
                if get_agent(synset.lemmas()[0].antonyms()[0].name()) == False:
                    antonym = add_agent(synset.lemmas()[0].antonyms()[0].name(), agent_type=ConceptAgent,
                                        comment=synset.definition())
                else:
                    antonym = find_agent(synset.lemmas()[0].antonyms()[0].name())
                rel_name = "{}_opposite".format(agent_synset_name)
                add_agent(rel_name, agent_type=RelationConceptAgent,
                          comment=synset.definition(), arguments = [new_agent, antonym])
"""

# END OF FILE: LTM_build_up.py #
