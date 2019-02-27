
####################
# GLOBAL VARIABLES #
####################

# DEFINES ALL GLOBAL VARIABLES USED IN DUAL.
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018


# The reports that the architecture gives are usually visible (that is when the value equals True.
# When equals False, it gets the pass function.
verbose = True
# The following value is used in the dual_raise function.
# If flag_error equals True, the architecture raises an error and stops its work;
# If flag_error equals False, the program prints an error and continues its work.
flag_error = True
# The architecture can interact with the user
# - i.e. it can ask for names of the agents that it creates.
# If the value equals True, it interacts; If it equals False it does not interact.
user_interaction = False

# A global variable that stores the time since the beginning of the simulation (in units of simulated time). It gets
# annulled with DUAL's initialization and/or a new simulation begins. Importantly, DUAL agents do not have access
# to this global and absolute time scale (it is only for the user - i.e. the verbose messages, etc.).
dual_time = 0

# Dictionary that contains all agents being created.
# The :Keys are the names of the agents; the :Values are the agents themselves.
all_agents = {}
# Dictionaries containing all the agents in the input_list and the goal_list. Their default state is empty dicts.
# The :Keys are the agents themselves;
# the :Values are the activation of the nodes.
input_list = {}
goal_list = {}
# A list of all the agents which are targets at the moment. The default value is an empty list.
target_agents = []
# A list of all the agents that create the current target situation. The default value is an empty list.
target_situation = []
# A list of all agents which are currently in the short_term_memory. The default value is an empty list.
short_term_memory = []
# A list containing all the agent which are not in the short_term_memory.
# The default value is a list of the values of all the agents in the LTM.
agents_not_in_STM = list(all_agents.values())
# A list containing all the agent which are anticipated. The default value is an empty list.
list_of_anticipations = []
# A list containing all the mappings. The default value is an empty list.
list_of_mappings = []
# The working memory of the architecture contains the STM, everything on the input and all goals.
working_memory = short_term_memory + list(input_list.keys()) + list(goal_list.keys())
# A list containing the agent which is currently the focus_of_attention. The default value is an empty list.
# A list with all the request for the creation of new agents. The default state of the list is empty list.
list_of_all_requests = []
# Each step is filled with the just created non unreal agents.
just_created = []
# All agents that are supposed to be deleted (the list contains them so they cannot be created again).
deactivated_agents = []

# GLOBAL LEARNING/CLASSIFICATION VARIABLES #
# If enable_classification equals False, the architecture is not allowed to classify new episodes.
# The default value is True.
enable_classification = True
# If enable_concept_learning equals False, the architecture is not allowed to learn new concepts.
# The default value is True.
enable_concept_learning = True

###
# On each run it checks if the classification is correct or not.
correct_classification = True
# It calculates how many correct classifications in a row there are.
n_correct = int(0)
# Is the new instance currently classified?
not_classified = True
# Ask for a feedback or not.
feedback = False

# A global variable related to the focus of the working memory and maintained by the function update_focus(),
# which is currently not in use.
focus_of_attention = []
# A list containing the agent which is currently the abstract_focus_of_attention/the second focus of attention.
# The default value is an empty list.
abstract_focus_of_attention = []

# END OF FILE VARIABLES.PY #
