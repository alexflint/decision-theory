from factorgraph import Factor, FactorGraph

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
    Set up newcomb's problem as a decision problem.

    Here we use a 5-node factor graph to set up the problem. The nodes are:
     - "my inclination"      my background tendency to 1-box or 2-box
     - "which boxes I take"  decision I actually make, represented in the world model as identical to "my inclination"
     - "omega's prediction"  omega's prediction about whether I will 1-box or 2-box, represented in the world model as identical to "my inclination"
     - "contents of first box"    amount of money omega puts in first box: either 0 or 1000000
     - "money I walk away with"   amount of money I walk away with

    This is intentionally not the most minimal possible setup since our goal here is understandability.
    """

    # first set up the names of the nodes and their possible values
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

    # create the factor graph
    world_model = FactorGraph(nodes, factors)

    # in newcomb's problem there are no observations
    observations = {}

    # in this graph, utility always corresponds to "money I walk away with"
    utility_node = "money I walk away with"

    # from a physical standpoint, our action corresponds is the node "which boxes I take"
    physical_identity = "which boxes I take"

    # from a logical standpoint, our action corresponds to both "which boxes I take" and "omega's prediction"
    logical_identity = ["which boxes I take", "omega's prediction"]

    # return the full problem setup
    return world_model, observations, utility_node, physical_identity, logical_identity


def build_transparent_newcomb():
    """
    Set up tranparent Newcomb's problem as a decision problem.

    Here we use a 5-node factor graph to set up the problem. The nodes are:
     - "my inclination"      my background tendency to 1-box or 2-box
     - "which boxes I take"  decision I actually make, represented in the world model as identical to "my inclination"
     - "omega's prediction"  omega's prediction about whether I will 1-box or 2-box, represented in the world model as identical to "my inclination"
     - "contents of first box"    amount of money omega puts in first box: either 0 or 1000000
     - "money I walk away with"   amount of money I walk away with

    The only difference with ordinary Newcomb's problem is that we observe the value of
    "contents of first box" to be 1000000. This observation is provided as an additional
    piece of information beyond the factor graph itself. The factor graph still has a node
    "contents of first box" that can take on two possible values (0 or 1000000), and the
    factors in the factor graph still model the relationship between both of those values
    and all other nodes. The observation that "contents of first box = 1000000" is provided
    as an additional piece of metadata.
    """

    # first set up the names of the nodes and their possible values
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
        Factor.deterministic("contents of first box", ["omega's prediction"],
                             lambda prediction: 1000000 if prediction == "1-box" else 0),
        Factor.deterministic("money I walk away with", ["contents of first box", "which boxes I take"],
                             lambda first_box_contents, decision: first_box_contents if decision == "1-box" else first_box_contents + 1000)
    ]

    # create the factor graph
    world_model = FactorGraph(nodes, factors)

    # in transparent newcomb's problem we observe $1000000 in the first box
    observations = {"contents of first box": 1000000}

    # in this graph, utility always corresponds to "money I walk away with"
    utility_node = "money I walk away with"

    # from a physical standpoint, our action corresponds is the node "which boxes I take"
    physical_identity = "which boxes I take"

    # from a logical standpoint, our action corresponds to both "which boxes I take" and "omega's prediction"
    logical_identity = ["which boxes I take", "omega's prediction"]

    # return the full problem setup
    return world_model, observations, utility_node, physical_identity, logical_identity


def build_red_room_blue_room(observed_color):
    """
    Set up the red room / blue room problem, with an observation that is either
    "red" or "blue".

    Similar to transparent Newcomb's problem, we set up the problem so that the agent
    always observes the actual color of the room they find themselves in, yet we build
    a factor graph that describes both possibilities: the red and the blue observation.
    This is so that we can represent the fact that whatever color is in fact seen,
    the copy of the agent sees the opposite.

    In this problem an agent is placed in either a red room or a blue room. A copy of the
    agent is placed in a room of the opposite color. The agent can output two possible
    messages, and receives a reward if it chooses *differently* from its copy.

    This problem is the canonical counterexample for UDT1.0, and was a major motivation
    for UDT1.1.

    This problem is often described as a "multi-agent scenario", which makes sense, but
    in this framework we model it as a single factor graph.
    """

    # first set up the names of the nodes and their possible values
    nodes = {
        "outer setup":          ["red first", "blue first"],
        "color I see":          ["red", "blue"],
        "action I take":        [1, 2],
        "color my copy sees":   ["red", "blue"],
        "action my copy takes": [1, 2],
        "utility":              [0, 1],
    }

    # now set up the factors defining the relationships between thes nodes
    factors = [
        Factor.uniform("outer setup", 0.5),
        Factor.deterministic("color I see", ["outer setup"],
                             lambda setup: "red" if setup.startswith("red") else "blue"),
        Factor.deterministic("color my copy sees", ["outer setup"],
                             lambda setup: "blue" if setup.startswith("red") else "red"),
        Factor.uniform_function_of("action I take", ["color I see"], 0.5),
        Factor.uniform_function_of("action my copy takes", ["color my copy sees"], 0.5),
        Factor.deterministic("utility", ["action I take", "action my copy takes"],
                             lambda my_action, other_action: 0 if my_action == other_action else 1)
    ]

    # create the factor graph
    world_model = FactorGraph(nodes, factors)

    # in this problem we observe the color of the room we are in
    observations = {"color I see": observed_color}

    # in this graph, utility always corresponds to the node labelled "utility"
    utility_node = "utility"

    # from a physical standpoint, our action corresponds to the node "color I see"
    physical_identity = "action I take"

    # from a logical standpoint, our decision algorithm determines both "color I see" and "color my copy sees"
    logical_identity = ["action I take", "action my copy takes"]

    # return the full problem setup
    return world_model, observations, utility_node, physical_identity, logical_identity
