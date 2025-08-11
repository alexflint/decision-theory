import itertools

def expected_utility(world_model, utility_node, intervention_node, intervention_value):
    # Make a list of the possible values of each node other than the intervention node
    non_intervention_nodes = [node_name for node_name in world_model.nodes.keys() if node_name != intervention_node]

    # Now go through the cartesian product of the above
    sum_probability = 0.
    sum_weigted_utility = 0.
    for non_intervention_values in itertools.product(*[world_model.nodes[n] for n in non_intervention_nodes]):
        # Make a map from node names to their values
        nodes = non_intervention_nodes + [intervention_node]
        values = list(non_intervention_values) + [intervention_value]
        world = {node: value for node, value in zip(nodes, values)}

        # First compute the probability of this possible world
        probability = world_model.evaluate(world)

        # Next compute the utility of this possible world (look up value of utility node)
        utility = world[utility_node]

        # Add these values to the accumulators
        sum_probability += probability
        sum_weigted_utility += probability * utility

    # The expected utility is the sum of the weighted utilities divided by the probability mass
    # associated with this intervention
    return sum_weigted_utility / sum_probability
