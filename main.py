import argparse

import problems
import theories
import inference

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("decision_theory", choices=["EDT", "CDT", "FDT"])
    parser.add_argument("decision_problem", choices="newcomb")
    parser.add_argument("--verbose", action="store_true", default=False)
    args = parser.parse_args()

    if args.decision_theory.lower() == "edt":
        theory = theories.evidential_decision_theory
    elif args.decision_theory.lower() == "cdt":
        theory = theories.causal_decision_theory
    elif args.decision_theory.lower() == "fdt":
        theory = theories.functional_decision_theory
    else:
        print(f"unknown decision theory: {args.decision_theory}")
        return

    if args.decision_problem == "newcomb":
        world_model, utility_node, physical_identity, logical_identity = problems.build_newcomb()
    else:
        print(f"unknown decision theory: {args.decision_theory}")
        return

    # use the decision theory to perform surgery to get a factor graph where our
    # decision can be taken by maximizing expected utility coniditioned on a single
    # "intervention" node. In the below, this intervention node is a string
    # identifying a node in the decision_model.
    modified_model, intervention_node = theory(world_model, physical_identity, logical_identity)

    # go through each possible value of the intervention node and compute an expected utility
    expected_utilities = {}
    for intervention in modified_model.nodes[intervention_node]:
        expectation = inference.expected_utility(modified_model, utility_node, intervention_node, intervention)
        expected_utilities[intervention] = expectation
        if args.verbose:
            print(f"expected utility of {intervention} = {expectation}")

    # pick the intervention with highest expected utility
    output = max(expected_utilities.keys(), key=lambda node_name: expected_utilities[node_name])
    print(output)


if __name__ == "__main__":
    main()
