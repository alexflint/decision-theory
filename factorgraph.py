from typing import Callable, Any

class Factor(object):
    """
    A factor is a conditional probability that may appear in a factor graph. It has
    a set of causally upstream nodes (the "causes") identified by the names of those
    nodes, and one causally downstream node (the "consequence"), also identified by the
    name of that node. Additionally, there is a coniditional probability function that
    outputs a float given values of all the nodes involved.

    In the examples in this library, we only ever have factors with zero or one causally
    upsream nodes. A factor with zero causally upstream nodes is a prior on the consequence
    node. A factor with one causally upstream node is a conditional probability
    P(consequence | cause).

    In this library, all nodes have a finite set of possible values. Those possible values
    are defined in the factor graph, and can have any type that is convenient for a certain
    problem setup.

    It is assumed that the conditional probability produces outputs between 0 and 1, and
    that those outputs sum to 1 over the possible values of the consequence node.
    """
    def __init__(self, consequence: str, causes: list[str], conditional: Callable[..., float]):
        if not isinstance(causes, list):
            raise Exception(f"Factor constructed with causes={causes}, expected list of strings")
        if not all(isinstance(cause, str) for cause in causes):
            raise Exception(f"Factor constructed with causes={causes}, expected list of strings")
        self.consequence = consequence
        self.causes = causes
        self.conditional = conditional

    def __call__(self, *values):
        return self.conditional(*values)

    @classmethod
    def uniform(cls, node_name, probability):
        """
        Create a factor that assigns a uniform probability to a certain node
        """
        return Factor(node_name, [], lambda _: probability)

    @classmethod
    def uniform_function_of(cls, consequence, causes, probability):
        """
        Create a factor that assigns a uniform probability to a certain node,
        and indicates that a certain other node is an input
        """
        return Factor(consequence, causes, lambda *args: probability)

    @classmethod
    def identical(cls, consequence, cause):
        """
        Create a factor that assigns probability 1 in all cases where a certain consequence node
        equals a certain cause node, and probability 0 in all other cases.
        """
        return Factor(
            consequence,
            [cause],
            lambda consequence, cause: float(consequence == cause))

    @classmethod
    def deterministic(cls, consequence, causes, f):
        """
        Create a factor that assigns probability 1 in all cases where a certain consequence node
        has a value that equals f(causes), and 0 in all other cases.
        """
        return Factor(
            consequence,
            causes,
            lambda consequence, *causes: float(consequence == f(*causes))
        )

    @classmethod
    def curry(cls, factor, **values):
        """
        Create a factor that wraps another factor and always sets the nodes named in the
        keys of VALUES to their repsective values.
        """
        raise Exception("TODO")


class FactorGraph(object):
    """
    A factor graph is a list of node names, together with the possible values for each
    of those nodes, and a list of factors defined over those nodes.

    It is assumed that every node appears as a consequence in exactly one factor, so
    the number of factors will always equal the number of nodes.
    """
    def __init__(self, nodes: dict[str, list[str]], factors: list[Factor]):
        self.nodes = nodes
        self.factors = factors

    def evaluate(self, world: dict[str, Any]):
        """
        Evaluate the probability of a possible world. A posssible world is a map from
        node names to the value of that node in this world. We evaluate each factor and
        multiply the results together to get a probability.
        """
        probability = 1.
        for factor in self.factors:
            node_names = [factor.consequence] + factor.causes
            node_values = [world[n] for n in node_names]
            probability *= factor(*node_values)
        return probability
    
    def view(self, *args, **kwargs):
        """
        Render and open a .pdf of self in out/ using graphviz.
        """
        import graphviz
        dot = graphviz.Digraph()
        for node, values in self.nodes.items():
            dot.node(node,f"<<b>{node}</b><font point-size=\"10\">{''.join(f'<br/>{v}' for v in values)}</font>>")
        for factor in self.factors:
            for cause in factor.causes:
                dot.edge(cause, factor.consequence)
        kwargs.setdefault("directory", "out")
        dot.view(*args, **kwargs)

def conditionalize(world_model, **values):
    """
    Given a factor graph, create a new factor graph representing a conditional distribution.
    Values is a map from nodes to values. These are the nodes that the new factor graph is
    conditioned on, and their respective values. Note that we eliminate the conditioned
    nodes entirely from the new factor graph. When the evaluate() member is called on the
    new factor graph, the probabilities returned are always conditioned on the respective
    values.
    """
    # TODO: curry each factor in world_model on VALUES; remove the nodes in VALUES from the
    # list of nodes
