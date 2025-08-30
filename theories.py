import itertools
import collections
from copy import deepcopy

from factorgraph import Factor, FactorGraph


def evidential_decision_theory(world_model, observations, physical_identity, logical_identity):
    """
    In evidential decision theory we make no changes to the world model, and directly
    conidition on the physical_identity node. This makes EDT incredibly trivial to
    implement in this framework.
    """
    return world_model, physical_identity, lambda output: output


def causal_decision_theory(world_model, observations, physical_identity, logical_identity):
    """
    In causal decision theory we do a surgery in which we drop all factors with the physical_identity
    as a consequence, and then condition on the physical_identity node.
    """
    modified_factors = [factor for factor in world_model.factors if factor.consequence != physical_identity]
    return FactorGraph(world_model.nodes, modified_factors), physical_identity, lambda output: output



def timeless_decision_theory(world_model, observations, physical_identity, logical_identity):
    """
    In timeless decision theory we do a surgery in which we drop all factors with any logical_identity
    node as a consequence, then add a new node with each logical_identity node as a deterministic consequence
    of it.
    """

    # add a new node with possible values equal to those of the logical identity nodes
    possible_values = world_model.nodes[logical_identity[0]]
    modified_nodes = deepcopy(world_model.nodes)
    modified_nodes["output of my decision algorithm"] = possible_values

    # remove factors that have any logical_identity node as a consequence
    modified_factors = [factor for factor in world_model.factors if factor.consequence not in logical_identity]

    # add a factor that makes each logical_identity node a deterministic function of "output of my decision algorithm"
    for n in logical_identity:
        modified_factors.append(Factor.identical(n, "output of my decision algorithm"))

    # return the modified factor graph, using the new logical node as the intervention node
    return FactorGraph(modified_nodes, modified_factors), "output of my decision algorithm", lambda output: output


def updateless_decision_theory_11(world_model, observations, physical_identity, logical_identity):
    """
    In updateless decision theory 1.1 we add a policy node representing our action as a function of
    each possible input. The space of possible inputs is determined by the set of nodes that
    are direct causes of the nodes in logical_identity. These must all have the same set of
    possible values in order that the function we are intervening on have a consistent type
    signature.

    We drop factors that are causes of any of our logical identity nodes.
    """

    # work out our own type signature by making a list of nodes that are used as inputs
    inputs_by_logical_identity = collections.defaultdict(list)
    for factor in world_model.factors:
        if factor.consequence in logical_identity:
            inputs_by_logical_identity[factor.consequence].extend(factor.causes)

    # our output space is represented directly in the world model
    output_space = world_model.nodes[logical_identity[0]]

    # now construct the cartesian product over the possible values of all the input nodes to get the space of inputs
    input_nodes = inputs_by_logical_identity[logical_identity[0]]
    input_values = [world_model.nodes[node] for node in input_nodes]
    input_space = list(itertools.product(*input_values))

    # check that our type signature is the same for each of our logical identities
    for identity in logical_identity:
        alt_output_space = world_model.nodes[identity]
        alt_input_nodes = inputs_by_logical_identity[identity]
        alt_input_values = [world_model.nodes[node] for node in alt_input_nodes]
        alt_input_space = list(itertools.product(*alt_input_values))
        if set(alt_input_space) != set(input_space):
            raise Exception(f"inconsistent logical inputs: {alt_input_space} vs {input_nodes} (for {identity})")
        if set(alt_output_space) != set(output_space):
            raise Exception(f"inconsistent logical outputs: {alt_output_space} vs {output_space} (for {identity})")

    # now do a second cartesian product to make a list of all possible policies
    policy_space = list(itertools.product(output_space, repeat=len(input_space)))

    # add a new node with possible values equal to the policy space
    modified_nodes = deepcopy(world_model.nodes)
    modified_nodes["my policy"] = policy_space

    # remove factors that have any logical_identity node as a consequence
    modified_factors = [factor for factor in world_model.factors if factor.consequence not in logical_identity]

    # add a factor that makes each logical_identity node a function of its original inputs plus "my policy"
    for n in logical_identity:
        original_causes = inputs_by_logical_identity[n]
        modified_causes = ["my policy"] + original_causes
        modified_factors.append(Factor.deterministic(n, modified_causes,
                                                     lambda policy, *inputs: policy[input_space.index(inputs)]))

    # turn the observations dictionary into a tuple of inputs
    output_formatter = lambda output: output
    if all(node in observations for node in input_nodes):
        observed_inputs = tuple(observations[node] for node in input_nodes)
        output_formatter = lambda policy: policy[input_space.index(observed_inputs)]

    # return the modified factor graph, using the new policy node as the intervention node
    return FactorGraph(modified_nodes, modified_factors), "my policy", output_formatter
