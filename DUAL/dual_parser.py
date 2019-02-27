## -*- coding: utf-8 -*-
#"""
#Created on Wed Nov 21 12:42:16 2018
#
#@author: Slavi Slavov
#"""

import nltk

# Test sentences:
sent_1 = "The cat is chasing the mouse."
sent_2 = "The square is inside the circle."
sent_3 = "John is drinking orange juice."
sent_4 = "The white bear ate the scared fish."
sent_5 = "The little Johnny is playing with the cool toy."
sent_6 = "The little Johnny is playing with the scary cats."

# The following sentences do not work with our parser, but they work with SPACY.
# By 'work' we mean that it extracts the main relation with its arguments.
compl_1 = "John, although aggressive, loves Mary"
compl_2 = "John, being angry and aggressive, loves Mary."
compl_3 = "John likes orange juice."
compl_4 = "John, who is tall, likes the beautiful Mary."
# The Spacy parser works with compound sentences such as:
compl_7 = "John loves Mary and he is tall."

# Yet, SPACY does not work with:
#    "The square is inside the circle."
# --> we work with our parser and use the SPACY one only for complex sentences,
# so we could use at least the main relation with the appropriate arguments.

# The following do not work with any of the parsers:
compl_5 = "There are three people jogging in the park."
compl_6 = "New York is eight times more populated than Sofia."


# Parser creating predicate structures:
PREDICATES_LIST = []


class Predicate(object):
    # The PREDICATE class creates structures with arguments:
    # RELATION, ARGUMENTS, ARITY and PROPERTIES.
    # The argument RELATION is a list with the relation as first element and its POS type as second.
    # The argument ARGUMENTS is a list of lists.
    # Each such list contains an argument of the relation together with its POS type.
    # The argument PROPERTIES refers to any property that an argument can have.
    # It is a dict, containing an argument as a key and its property and POS type as value.
    # If none of the argumnts has a property, PROPERTIES is an empty string.
    def __init__(self, relation=[], arguments=[], arity=0, properties = ""):
        
        self.relation = relation
        self.arguments = arguments
        self.arity = arity
        self.properties = properties


    def __repr__(self):
        # Each predicate structure is represented in an analogous form:
        # [loves[John, Mary], {'Mary': 'beatiful'}]
        arguments_list = [x[0] for x in self.arguments]
        if self.properties:
            properties_list = {}
            for key, value in self.properties.items():
                properties_list[key] = value[0][0]
        else:
            properties_list = ""
        return "{} {}; {}".format(self.relation[0][0], arguments_list, properties_list)

    
    def describe_itself(self):
        # When the predicate structure is described,
        # printed are: the whole structure as represented by __repr__
        # and all of the arguments of the Predicate class.
        print("Whole structure: {}".format(self))
        print("Relation: {}".format(self.relation[0][0]))
        print("Arguments: {}".format([x[0] for x in self.arguments]))
        print("Arity: {}".format(self.arity))
        if self.properties:
            properties_list = {}
            for key, value in self.properties.items():
                properties_list[key] = value[0][0]
        else:
            properties_list = ""
        print("Properties: {}".format(properties_list))
    
                
def find_verb_in_sentence (sentence):
    # Right now pos_tag interprets 'left of' as the past form of the verb 'left'.
    special = ['right', 'top' 'to', 'next']
    tagged_result=[]
    flag = True
    flag_IN = True
    flag_IS_ARE = False
    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(sentence)) 
    for token in tagged_sentence:
        # IN includes 'below', 'above', 'of', 'in' and 'behind'.    
        if token[1] in ['VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'VB', 'IN', 'RB', 'RBR', 'JJ', 'JJR']:
            if token[1] in ['IN']:
                for res in tagged_result:
                    if res[1] in ['VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'VB', 'IN'] and res[0] != "is":
                        flag_IN = False
                if flag_IN:
                    tagged_result = tagged_result + [[token[0], token[1]]]
            else:
                tagged_result = tagged_result + [[token[0], token[1]]]
                    
        if token[0] in special:
            tagged_result = tagged_result + [token]
            
        if flag:
            if token[1] in ['JJ', 'RB']:
                tagged_result = [x for x in tagged_result if x[0] != token[0]]
        flag = True
        if token[0] == 'more':
            flag = False
    for res in tagged_result:
        if res[0] in ["is", "are"]:
            flag_IS_ARE = True
    if flag_IS_ARE:
        for res in tagged_result:
            if res[1] in ['VBZ', 'VBP', 'VBN', 'VBG', 'VBD', 'VB', 'IN', 'RB', 'RBR', 'JJ', 'JJR']:
                tagged_result = [x for x in tagged_result if x[0] != "is" and x != "are"]
                break
    return tagged_result
            
            
            
# Adding a list of 'part_of' properties.
def jjr_check(words):
    flag = False
    for w in words:
        if words[1] == 'JJR':
            flag = True
    return flag


def find_properties_in_sentence(sentence):
    
    all_properties = {}
    words = []
    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(sentence))
    for token in tagged_sentence:
        words = words + [token]
    try:
        i = -1
        for properties in words:
            property_list = []
            property_of_list = []
            i += 1
            if properties[1] == 'JJ' and words[i-1][0] != 'more' and (properties[1] != 'RBR' or jjr_check(words)):
                property_list = property_list + [properties]
                property_of_list = property_of_list + [words[i+1][0]]
                print("The argument '{}' has property '{}'.".format(property_of_list[0], [x[0] for x in property_list][0]))
                all_properties[property_of_list[0]] = property_list
    except:
        pass
    return all_properties
        
    
def find_nouns_in_sentence(sentence):
    special = ['right', 'top' 'to', 'next']
    tagged_result = []
    tagged_sentence = nltk.pos_tag(nltk.word_tokenize(sentence))
    for token in tagged_sentence:
        if token[1] in ['NNP', 'NN', 'NNS', 'NNPS', 'PRP', 'PRP$'] and token[0] not in special:
            tagged_result = tagged_result + [token]
    return tagged_result

    
def form_predicate(sentence):
    return [find_verb_in_sentence(sentence), find_nouns_in_sentence(sentence), find_properties_in_sentence(sentence)]
    

def predicate(sentences):
    # Forms predicates for multiple sentences using tokenization.
    global PREDICATES_LIST
    result = []
    multi_sent = nltk.sent_tokenize(sentences)
    for sentence in multi_sent:
        result = form_predicate(sentence)
        properties = ""
        if result[2]:
            properties = result[2] 
        # Following the structure of the output result of predicate function.
        predicate_arguments = [x for x in result[1]]
        new_predicate = Predicate(relation=result[0], arguments=predicate_arguments,
                                  arity=len(predicate_arguments), properties=properties)
        PREDICATES_LIST = PREDICATES_LIST + [new_predicate]
    return PREDICATES_LIST


def describe_predicate(predicate):
    Predicate.describe_itself(predicate)

    
def describe_predicates():
    for i in PREDICATES_LIST:
        Predicate.describe_itself(i)
        

def test():
    global PREDICATES_LIST
    PREDICATES_LIST = []
    a = [sent_1, sent_2, sent_3, sent_4, sent_5, sent_6]
    #a = [sent_1, sent_2, sent_3, sent_4, sent_5, sent_6, compl_6, compl_5, compl_4]
    for test in a:
        predicate(test)
    
    return PREDICATES_LIST


# Lematizing the formed predicates as they are in WordNet.
# nltk.stem.WordNetLemmatizer().lemmatize('word', pos='n') turns WORD into its basic form.
# The default pos tag is NOUN, meaning that it does not output the correct lemma of verbs,
# unless the pos tag is explicitly specified as VERB.

Lemmatized_PREDICATES_LIST = []

class Lemm_Predicate(object):
    # The PREDICATE class creates whole structures with argument RELATION, ARGUMENT_1 and ARGUMENT_2.
    def __init__(self, relation=[], arguments=[], arity=0, properties = ""):
        
        self.relation = relation
        self.arguments = arguments
        self.arity = arity
        self.properties = properties


    def __repr__(self):
        if self.properties:
            properties_list = {}
            for key, value in self.properties.items():
                properties_list[key] = value[0][0]
        else:
            properties_list = ""
        return "{} {}; {}".format(self.relation, self.arguments, properties_list)


def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return 'a'
    elif tag.startswith('V') or tag.startswith('IN'):
        return 'v'
    elif tag.startswith('N'):
        return 'n'
    elif tag.startswith('R'):
        return 'r'
    else:
        # The default pos in lemmatization is Noun
        return 'n'


def lemmatize_predicates():
    global PREDICATES_LIST
    global Lemmatized_PREDICATES_LIST
    lemmatizer = nltk.stem.WordNetLemmatizer()
    for predicate in PREDICATES_LIST:
        lemm_relation = lemmatizer.lemmatize(predicate.relation[0][0], pos=get_wordnet_pos(predicate.relation[0][1]))
        lemm_arguments = []
        lemm_properties = {}
        for arg in predicate.arguments:
            lemm_arg = lemmatizer.lemmatize(arg[0], pos=get_wordnet_pos(arg[1]))
            lemm_arguments = lemm_arguments + [lemm_arg.lower()]
            if predicate.properties:
                for key, value in predicate.properties.items():
                    if key == arg[0]:
                        lemm_prop = lemmatizer.lemmatize(value[0][0], pos=get_wordnet_pos(value[0][1]))
                        lemm_properties[lemm_arg.lower()] = [lemm_prop.lower(), value[0][1]]
        if not lemm_properties:
            lemm_properties = ''
        new_predicate = Lemm_Predicate(relation=lemm_relation.lower(), arguments=lemm_arguments,
                                       arity=predicate.arity, properties=lemm_properties)
        Lemmatized_PREDICATES_LIST = Lemmatized_PREDICATES_LIST + [new_predicate]
    return Lemmatized_PREDICATES_LIST


# Turn the lematized predicates in dual agents.


from main_cycle import *
# load_kb_from_file("LT_knowledge_with_ADJ.csv")
from add_from_console import *

def predicates_into_agents():
    global Lemmatized_PREDICATES_LIST
    for predicate in Lemmatized_PREDICATES_LIST:
        if get_agent("{}_rel".format(predicate.relation)):
            rel_name = "{}_{}_rel".format(predicate.relation,
                                          len(find_agent("{}_rel".format(predicate.relation)).instances)+int(1))
            add_agent(rel_name, agent_type=RelationInstanceAgent, arity=predicate.arity,
                      instance_of=[find_agent("{}_rel".format(predicate.relation))])
        else:
            print("There is no appropriate dual agent for the relation: ",
                  "{}_rel".format(predicate.relation))
            if variables.user_interaction:
                ask = input("Would you like to create an agent yourself? (yes or no) ")
                if ask == 'yes':
                    add_agent_from_console()
        for arg in predicate.arguments:
            if get_agent("{}_n".format(arg)):
                arg_name = "{}_{}_n".format(arg, len(find_agent("{}_n".format(arg)).instances)+int(1))
                arg_agent = add_agent(arg_name, agent_type=InstanceAgent,
                          instance_of=[find_agent(find_agent("{}_n".format(arg)))])
                if predicate.properties:
                    for prop, value in predicate.properties.items():
                        if prop == arg:
                            if get_agent("{}_{}".format(value[0], get_wordnet_pos(value[1]))):
                                prop_name = "{}_{}_{}".format(value[0],
                                                              len(find_agent("{}_{}".format(value[0],
                                                                                            get_wordnet_pos(value[1]))).instances)+int(1),
                                                                  get_wordnet_pos(value[1]))
                                add_agent(prop_name, agent_type=InstanceAgent,
                                          instance_of=[find_agent("{}_{}".format(value[0],
                                                                                 get_wordnet_pos(value[1])))],
                                          part_of=[arg_agent])
                            else:
                                print("There is no appropriate dual agent for the property : ",
                                      "{}_{}".format(value[0], get_wordnet_pos(value[1])))
                                if variables.user_interaction:
                                    ask = input("Would you like to create an agent yourself? (yes or no) ")
                                    if ask == 'yes':
                                        add_agent_from_console()
                                                              
            else:
                print("There is no appropriate dual agent for the argument : ",
                      "{}_n".format(arg))
                if variables.user_interaction:
                    ask = input("Would you like to create an agent yourself? (yes or no) ")
                    if ask == 'yes':
                        add_agent_from_console()
            
            

def test_integration():
    load_kb_from_file("LT_knowledge_with_ADJ.csv")
    test()
    lemmatize_predicates()
    predicates_into_agents()
    
        

###################################################
#  Parser for complex sentences

#  Spacy   https://explosion.ai/demos/displacy?text=John%2C%20who%20is%20tall%2C%20likes%20the%20beautiful%20Mary.&model=en_core_web_sm&cpu=1&cph=1

# Below are listed some basic functions Spacy can do and the information it provides:

#  Creates a tree and parses it according to dependencies:
import spacy
nlp = spacy.load('en_core_web_sm')
doc = nlp(u'John, who is tall, likes the beautiful Mary')


#   Checking the structure of the sentence, including: text, the lemma, the tag, and the dependecy:
for token in doc:
    print(token.text, token.lemma_, token.tag_, token.dep_)


#  Checking the structure of the sentence (like our parser):
for token in doc:
    print( token.text, token.tag_)
    
    
    # Chunking for dependencies, i.e. what words connect the nouns and objects within the clauses
    # https://spacy.io/usage/linguistic-features#section-dependency-parse
    
    #  NOT used further in building the parser, just for information
for chunk in doc.noun_chunks:
    print(chunk.text, chunk.root.text, chunk.root.dep_,
          chunk.root.head.text)
    
     
# More complete information, including heads and their children (words, directly connected in the tree)
# serves as the basis of the complex_sent_parser, based on token.dep_  relations
for token in doc:
    print(token.text, token.dep_, token.head.text, token.head.pos_,
          [child for child in token.children])  
    
for token in doc:
    print(token.text, token.head.pos_, [child for child in token.children])
    
structure = []
for token in doc:
    structure.append([token.text, token.dep_, [child for child in token.children]])
    print([token.text, token.dep_, [child for child in token.children]])
###############################################################################


import itertools

#   Complex Parser:

#      works by extracting the Universal Dependencies "nsubj", "dobj, pobj" and "ROOT" and forming 
#      the predicate in the form  [ROOT, [nsubj, dobj]]


#     The function takes into account only 1 nsubj in a sentence:
def form_nsubj(doc, sentence):
    structure = []
    sent = []
    nsubj_sent = []
    for token in doc:
        structure.append([token.text, token.dep_])
    for line in structure:
        if line[1] in ['nsubj']:
            nsubj_sent = nsubj_sent + [[line]]
            if len(nsubj_sent) == 1:
                sent = sent + [line[0]]
    return sent

def form_dobj(doc, sentence):
    structure = []
    sent = []
    for token in doc:
        structure.append([token.text, token.dep_])
    for line in structure:
        if line[1] in ['dobj', 'pobj']:
            sent = sent + [line[0]]
    return sent   


def form_root(doc, sentence):
    structure = []
    sent = []
    for token in doc:
        structure.append([token.text, token.dep_])
    for line in structure:
        if line[1] not in 'ROOT':
            pass
        else:
            sent.append(line)
    sent[0].remove('ROOT')
    return list(itertools.chain.from_iterable(sent))[0]   


def form_complex_predicate(sentence):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    return [form_root(doc, sentence), form_nsubj(doc, sentence) + form_dobj(doc, sentence)]

        
###########################

def complex_sent_parser(sentence):
    # It extracts the main relation.
    # i.e. John, who is tall, likes Mary. --> extracts likes[John, Mary].
    # However, that is the only working example.
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(sentence)
    structure = []
    sent = []
    for token in doc:
        structure.append([token.text, token.dep_, [child for child in token.children]])
        #print([token.text, token.dep_, [child for child in token.children]])
    for line in structure:
        if line[1] not in "ROOT":
                pass
        else:
            #print(line)
            sent.append(line)

    sent[0].remove('ROOT')
    return sent
######################################################


# END of file: dual_parser.py #

