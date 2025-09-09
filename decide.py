import pandas as pd
import itertools

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

    worlds = pd.DataFrame(itertools.product(*modified_model.nodes.values()), columns=modified_model.nodes)
    worlds['prob'] = worlds.apply(modified_model.evaluate, axis=1)
    worlds = worlds[worlds['prob'] != 0]
    if args and args.verbose:
        print(worlds.sort_values(intervention_node))
    expected_utilities = worlds.groupby(intervention_node).apply(
        lambda group: (group[utility_node] * group.prob).sum() / group.prob.sum(),
        include_groups=False)
    if args and args.verbose:
        for intervention, expectation in expected_utilities.items():
            print(f"expected utility of {intervention} = {expectation}")
    
    # pick the intervention with highest expected utility
    output = expected_utilities.idxmax()
    return output, output_formatter(output)
