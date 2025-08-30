import argparse

import problems
import theories
import inference

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("decision_theory", choices=["EDT", "CDT", "TDT", "UDT1.1"])
    parser.add_argument("decision_problem", choices=["newcomb", "redroom", "blueroom"])
    parser.add_argument("--verbose", action="store_true", default=False)
    args = parser.parse_args()

    if args.decision_theory.upper() == "EDT":
        theory = theories.evidential_decision_theory
    elif args.decision_theory.upper() == "CDT":
        theory = theories.causal_decision_theory
    elif args.decision_theory.upper() == "TDT":
        theory = theories.timeless_decision_theory
    elif args.decision_theory.upper() == "UDT1.1":
        theory = theories.updateless_decision_theory_11
    else:
        print(f"unknown decision theory: {args.decision_theory}")
        return

    if args.decision_problem == "newcomb":
        world_model, observations, utility_node, physical_identity, logical_identity = problems.build_newcomb()
    elif args.decision_problem == "redroom":
        world_model, observations, utility_node, physical_identity, logical_identity = problems.build_red_room_blue_room("red")
    elif args.decision_problem == "blueroom":
        world_model, observations, utility_node, physical_identity, logical_identity = problems.build_red_room_blue_room("blue")
    else:
        print(f"unknown decision theory: {args.decision_theory}")
        return

    if args.verbose:
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
    modified_model, intervention_node, output_formatter = theory(world_model, observations, physical_identity, logical_identity)

    if args.verbose:
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
        if args.verbose:
            print(f"expected utility of {intervention} = {expectation}")

    # pick the intervention with highest expected utility
    output = max(expected_utilities.keys(), key=lambda node_name: expected_utilities[node_name])
    if args.verbose:
        print(output)
    print(output_formatter(output))


if __name__ == "__main__":
    main()
