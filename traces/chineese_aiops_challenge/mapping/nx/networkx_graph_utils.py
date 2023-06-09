from typing import Hashable
import datetime
import networkx as nx
import pandas as pd

from mapping.user_defined.graph import get_node_attributes, get_edge_attributes
from preprocessing.trace_utils import *

'''
trace (grouped) to nx graph
'''


def build_initial_networkx_graph_from_trace(traces: pd.DataFrame) -> nx.DiGraph:
    print("Building initial nx graph...")

    graph = nx.from_pandas_edgelist(sort_traces_by_timestamp(traces), source='parent_span_id', target='span_id',
                                    create_using=nx.DiGraph(), edge_attr='call_type')
    if graph.has_node('None'):
        graph.remove_node('None')

    print("Successfully built initial nx graph!")

    return graph


def generate_networkx_graph(trace_id: Hashable, traces: pd.DataFrame) -> nx.DiGraph:
    print(f"Mapping trace {trace_id} with {len(traces)} spans to nx graph...")
    graph = build_initial_networkx_graph_from_trace(traces)
    print(graph.nodes())
    print(graph.edges())
    nx.set_node_attributes(graph, get_node_attributes(traces))
    nx.set_edge_attributes(graph, get_edge_attributes(traces))
    print(f"Successfully mapped trace {trace_id} with {len(traces)} spans to nx graph!")
    return graph
