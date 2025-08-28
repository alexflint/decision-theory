# Decision Theory in Python

This repository implements causal decision theory, evidential decision theory, and a version of functional decision theory that we are referring to as simply "FDT" for several classic decision theory problems. The goal here is to provide a resource for understanding decision theories by showing implementations of them in code.

So far only Newcomb's problem is implemented. You can run three decision theories on this problem like this:

```
$ python main.py CDT newcomb
2-box
$ python main.py EDT newcomb
1-box
$ python main.py FDT newcomb
1-box
```

The basic organization of this repository is as follows. The decision problems are implemented in problems.py. A decision problem is represented as a factor graph, which is a type of probabilistic graphical model. A decision problem identifies one node in the factor graph as the physical identity, which means that its value is physically controlled by the decision-maker. A decision problem also identifies one or more nodes in the factor graph as logical identities, which means that their values are determined by the output of the decision-maker's algorithm. Although these might sound like the same thing, many classic decision theory problems hinge on scenarios where the physical consequences of your action differ from the logical consequences. Some decision theories in this repository ignore the physical identity and use the logical identity, while others do the opposite. A decision problem also identifies a utility node whose value determines the goodness or badness of the action chosen by the agent.

The decision theories are implemented in theories.py. A decision theory takes a factor graph, a physical identity, and a logical identity, and outputs a new factor graph together with the name of a single node to intervene on. A decision theory is allowed the modify the factor factor graph in any way it wishes. The only rule is that it must identify a single node in that factor graph as the intervention node. An action will then be selected by considering all possible values of that intervention node, and selecting the one that maximizes the expected value of the utility node. That is, the action is selected as the argmax of the expected utility, conditional on the intervention node taking on a certain value.

In order to keep the code focussed, a decision theory does not itself compute any conditional expectations, nor do any optimizations over possible actions. Instead, its job is to set up a factor graph and identify an intervention node. The work to compute joint probabilities and conditional expectations is in inference.py and factorgraph.py.

The file main.py then ties all this together.
