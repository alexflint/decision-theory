from factor import Factor, FactorGraph

# This file sets up a number of common decision problems as factor graphs.

class DecisionProblem(object):
    """
    A decision problem is a tuple (world model, physical identity, logical identity)
    """
    def __init__(self, world_model, physical_identity, logical_identity):
        self.world_model = world_model
        self.physical_identity = physical_identity
        self.logical_identity = logical_identity


def build_newcomb():
    """
    Set up newcomb's problem as a decision problem in our framework.

    Here we use 5 nodes to set up the problem in a rather verbose way. It could be represented
    in a much more austere way, but here we err on the side of making things very explicit.

    The nodes are:
     - "my inclination"      my background tendency to 1-box or 2-box
     - "which boxes I take"  decision I actually make, represented in the world model as identical to "my inclination"
     - "omega's prediction"  omega's prediction about whether I will 1-box or 2-box, represented in the world model as identical to "my inclination"
     - "contents of first box"    amount of money omega puts in first box: either 0 or 1000000
     - "money I walk away with"   amount of money I walk away with
    """

    # first set up the names of the nodes an their possible values
    nodes = {
        "my inclination":           ["1-box", "2-box"],
        "which boxes I take":       ["1-box", "2-box"],
        "omega's prediction":       ["1-box", "2-box"],
        "contents of first box":    [1000000, 0],
        "money I walk away with":   [0, 1000, 1000000, 1001000],
    }

    # now set up the factors defining the relationship between the different nodes
    factors = [
        Factor.uniform("my inclination", 0.5),
        Factor.identical("which boxes I take", "my inclination"),
        Factor.identical("omega's prediction", "my inclination"),
        Factor.deterministic("contents of first box", ["omega's prediction"], lambda prediction: 1000000 if prediction == "1-box" else 0),
        Factor.deterministic("money I walk away with", ["contents of first box", "which boxes I take"],
                             lambda first_box_contents, decision: first_box_contents if decision == "1-box" else first_box_contents + 1000)
    ]

    # in this graph, utility always corresponds to "money I walk away with"
    utility_node = "money I walk away with"

    # from a physical standpoint, our action corresponds is the node "which boxes I take"
    physical_identity = "which boxes I take"

    # from a logical standpoint, our action corresponds to both "which boxes I take" and "omega's prediction"
    logical_identity = ["which boxes I take", "omega's prediction"]

    # create the factor graph and return the full problem setup
    return FactorGraph(nodes, factors), utility_node, physical_identity, logical_identity
