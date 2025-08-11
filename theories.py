from copy import deepcopy

from factor import Factor, FactorGraph


def evidential_decision_theory(world_model, physical_identity, logical_identity):
    """
    In evidential decision theory we make no changes to the world model, and directly
    conidition on the physical_identity node. This makes EDT incredibly trivial to
    implement in this framework.
    """
    return world_model, physical_identity


def causal_decision_theory(world_model, physical_identity, logical_identity):
    """
    In causal decision theory we do a surgery in which we drop all factors with the physical_identity
    as a consequence, and then condition on the physical_identity node.
    """
    modified_factors = [factor for factor in world_model.factors if factor.consequence != physical_identity]
    return FactorGraph(world_model.nodes, modified_factors), physical_identity



def functional_decision_theory(world_model, physical_identity, logical_identity):
    """
    In functional decision theory we do a surgery in which we drop all factors with any logical_identity
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
    return FactorGraph(modified_nodes, modified_factors), "output of my decision algorithm"
