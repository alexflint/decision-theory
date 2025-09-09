import inference

def decide(theory, world_model, observations, utility_node, physical_identity, logical_identity, args=None):
    if args and args.initial_verbose:
        world_model.view(filename="Initial")
    if args and args.verbose:
        print(f"INITIAL NODES:")
        for node, values in world_model.nodes.items():
            print(f"  {node:20s} ∊ {values}")
        print(f"INITIAL FACTORS:")
        for factor in world_model.factors:
            print(f"  {factor.consequence:20s} <= {factor.causes}")
    
    # use the decision theory to perform surgery to get a factor graph where our
    # decision can be taken by maximizing expected utility coniditioned on a single
    # "intervention" node. In the below, this intervention node is the name of a node
    # in modified_model
    modified_model, intervention_node, output_formatter = theory(world_model, observations, utility_node, physical_identity, logical_identity)

    if args and args.modified_verbose:
        modified_model.view(filename="Modified")
    if args and args.verbose:
        print(f"MODIFIED NODES:")
        for node, values in modified_model.nodes.items():
            print(f"  {node:20s} ∊ {values}")
        print(f"MODIFIED FACTORS:")
        for factor in modified_model.factors:
            print(f"  {factor.consequence:20s} <= {factor.causes}")

    # go through each possible value of the intervention node and compute an expected utility
    expected_utilities = {}
    for intervention in modified_model.nodes[intervention_node]:
        expectation = inference.expected_utility(modified_model, utility_node, intervention_node, intervention)
        expected_utilities[intervention] = expectation

    # pick the intervention with highest expected utility
    output = max(expected_utilities.keys(), key=lambda node_name: expected_utilities[node_name])
    return output, output_formatter(output)
