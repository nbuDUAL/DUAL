
########################
#  P A R A M E T E R S #
########################

# DEFINES THE MAIN DUAL PARAMETERS. 
# PROGRAMERS: Yolina Petrova and Georgi Petkov, YEAR 2017
# Last updated: Yolina Petrova, October, 2018


# When a new agent is instantiated it is with the following level of activation.
initial_agent_activation = 0.0
# Each agent on the input receives the following level of activation.
input_node_activation = 1.0
# Each agent on the goal receives the following level of activation.
goal_node_activation = 1.0
# When a mapping is created it receives the following activation.
default_initial_mapping_activation = 0.4  # CHECK
# When an anticipation is created it receives the following activation.
default_initial_anticipation_activation = 0.4  # CHECK

# The default value of all links that are being created.
initial_weight_for_links = 0.1
default_associative_weight = 0.5  # CHECK WHICH SHOULD BE THE USED ONE.
# Default weight for super-sub classes links.
default_is_a_weight = 0.5
default_class_subclass_weight = 0.3
default_class_instance_weight = 0.3
default_instance_of_weight = 0.2
default_class_anticipation_weight = 0.01
default_anticipation_mapping_just_weight = 0.00
default_mapping_class_weight = 0.00
default_part_of_weight = 0.3
default_is_part_weight = 0.3  # CHECK WHICH ONE IS THE USED ONE.
default_has_part_weight = 0.2
# The default predicate-arguments links are with the following value.
default_predicate_argument_weight = 2.0  # The old one was 0.5
# The default arguments-predicate links are with the following value.
default_argument_predicate_weight = 2.0  # The old one was 0.5
# Default weight of the links between the mappings between relations and their arguments.
default_str_corr_weight = 1.00
# Default weight of the links for the additional mappings supporting the already existing one.
default_justification_weight = 1.00
# Default weight of the supporting links between two mappings.
default_mapping_to_mapping_support_weight = 0.5
# Default weight of the links between contradicting mappings.
default_inhibitory_weight = - 1.50  # The old value was -1.00
# The weight of the link between the group/situation and the creator of the new situation.
group_creator_weight = 1.00
# The weight of the link between the group/situation and the rest of the members of the new group/situation.
group_argument_weight = 0.10
# The weight of the link between the creator of the new situation and the new situation.
creator_group_weight = 0.70
# The weight of the link between the rest of the members of the new situation and the new situation.
part_of_group_weight = 0.30
# The weight between the new focus and the group of the old focus.
new_focus_old_focus_weight = part_of_group_weight

# The agent's level of activation should be higher than the following threshold to enter the working memory.
threshold_agent_activation = 0.2  # currently IN use
# This is the initial threshold value for each newly created agent. It is similar to the frequency, the expectancy is to be changed.
default_mapping_threshold = 0.4
# (The threshold is higher than the usual one, because the newly created agents are to be activated harder than the permanent ones.)
default_instance_anticipation_threshold = 0.6
# For a mapping to be transformed into concept, its activation level should be higher that this threshold.
mapping_into_concept_threshold = 10.0  # currently IN use
# For an anticipation to be transformed into instance agent, its activation level should be higher that this threshold.
anticipation_into_instance_threshold = 10.0  # currently IN use
# Default weight for all links. - CHECK WHICH IS THE CORRECT ONE

# Calculates the differences in the activation level after each cycle.
# It could be used for surprise calculation; which has importance for the change focus.
default_speed_of_change = 0.0  # currently not IN use but it is part of the parameters

# Parameters for the activation functions
old_activation_rate = 0.75  # currently IN use
new_activation_rate = 1.0 - old_activation_rate
strength_of_increase = 0.0  # CHECK WHAT THIS IS FOR
# The activation level of each agent tends to decrease with the following value.
decay_rate = 0.90


# Categorization parameters #
#############################

# A parameter pointing to whether the program should receive feedback or not.
feedback = False
# A special link weight for some of the instance_of links.
special = 1.35

# Focus of attention functions #
################################

# Coefficient for the importance of the change of activation for updating the focus.
importance_coefficient = 0.5
# Coefficient for importance of the activation for updating the focus
new_activation_coefficient = 0.5
resistance_of_old_focus = 0.0
# A coefficient determining the activation level of the new group.
bootstrapping_activation_of_focus = 1.00
update_focus_threshold = 0.15

# END OF FILE PARAMETERS.PY #
