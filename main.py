import argparse

import problems
import theories
import decide

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("decision_theory", choices=["EDT", "CDT", "TDT", "UDT1.1", "RDT"])
    parser.add_argument("decision_problem", choices=["newcomb", "redroom", "blueroom"])
    parser.add_argument("--verbose", action="store_true", default=False)
    parser.add_argument("--initial_verbose", action="store_true", default=False)
    parser.add_argument("--modified_verbose", action="store_true", default=False)
    args = parser.parse_args()

    if args.decision_theory.upper() == "EDT":
        theory = theories.evidential_decision_theory
    elif args.decision_theory.upper() == "CDT":
        theory = theories.causal_decision_theory
    elif args.decision_theory.upper() == "TDT":
        theory = theories.timeless_decision_theory
    elif args.decision_theory.upper() == "UDT1.1":
        theory = theories.updateless_decision_theory_11
    elif args.decision_theory.upper() == "RDT":
        theory = theories.recursive_decision_theory
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

    output, formatted_output = decide.decide(theory, world_model, observations, utility_node, physical_identity, logical_identity, args)
    if args.verbose:
        print(output)
    print(formatted_output)


if __name__ == "__main__":
    main()
