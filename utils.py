"""
Copyright (c) 2024 Marcel Coetzee

MIT License
"""
from typing import Union

import pydot
from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import from_pydot


def dot_to_digraph(dot_string: str) -> MultiDiGraph:
    """
    Convert a DOT string to a NetworkX MultiDiGraph.

    Args:
        dot_string: The DOT string representation of the graph.

    Returns:
        A NetworkX MultiDiGraph object.
    """
    pgraph: Union[pydot.Dot, pydot.Graph, pydot.Cluster] = pydot.graph_from_dot_data(dot_string)[0]
    return from_pydot(pgraph)
