import inference

def decide(theory, world_model, observations, utility_node, physical_identity, logical_identity):
    # perform surgery on the factor graph
    modified_model, intervention_node, _ = theory(world_model, observations, utility_node, physical_identity, logical_identity)

    # go through each possible value of the intervention node and compute an expected utility
    expected_utilities = {}
    for intervention in modified_model.nodes[intervention_node]:
        expectation = inference.expected_utility(modified_model, utility_node, intervention_node, intervention)
        expected_utilities[intervention] = expectation

    # pick the intervention with highest expected utility
    return max(expected_utilities.keys(), key=lambda node_name: expected_utilities[node_name])
