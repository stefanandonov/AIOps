import os

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.colors as mcolors
from pyvis.network import Network

from mapping.nx.networkx_graph_utils import build_initial_networkx_graph_from_trace
from mapping.user_defined.user_defined_graph_utils import get_node_attributes, get_edge_attributes
from preprocessing.trace_utils import find_root_node_from_trace
from settings import environment_variables_dict

VISUALIZATION_OUTPUT_DIRECTORY_PATH: str = environment_variables_dict["VISUALIZATION_OUTPUT_DIRECTORY_PATH"]


def get_node_labels(traces: pd.DataFrame) -> dict[str, int]:
    node_attributes = get_node_attributes(traces=traces, encode=False)
    return {
        key: (f"{value['host_name']} {value['service_name']} {value['data_source_name']} {value['depth']} "
              f"{value['service_is_anomalous']}")
        for key, value in
        node_attributes.items()
    }


def get_edge_labels(traces: pd.DataFrame) -> dict[tuple[str, str], dict]:
    edge_attributes = get_edge_attributes(traces=traces, encode=False)
    return {
        key: f"{value['call_type']} {value['milliseconds_from_root']} "
             f"{value['elapsed_time']}" for key, value in edge_attributes.items()
    }


def get_node_label_colors(traces: pd.DataFrame, cmap: plt.cm = plt.get_cmap('Set1')) -> dict[str, str]:
    return {label: cmap(i) for i, label in enumerate(sorted(traces.host_name.unique()))}


def get_edge_label_colors(traces: pd.DataFrame, cmap: plt.cm = plt.get_cmap('Set1')) -> dict[str, str]:
    return {label: cmap(i) for i, label in enumerate(sorted(traces.call_type.astype('str').unique()))}


def nx_set_graph_attributes_and_labels(traces: pd.DataFrame) -> dict[str, nx.DiGraph | list[dict[str, str]]]:
    graph = build_initial_networkx_graph_from_trace(traces)

    root, node_attributes, node_labels, edge_attributes, edge_labels = find_root_node_from_trace(
        traces), get_node_attributes(traces=traces, encode=False), get_node_labels(traces=traces), get_edge_attributes(
        traces=traces, encode=False), get_edge_labels(traces=traces)

    print(f'Root: {root}')

    print(f'Trace start time: {root.index.to_list().pop()}')

    cmap = plt.get_cmap('Set1')
    nx.set_node_attributes(graph, node_attributes)
    nx.set_edge_attributes(graph, edge_attributes)

    edge_label_colors = {edge: get_edge_label_colors(traces=traces, cmap=cmap)[edge_attributes[edge]['call_type']] for
                         edge in
                         graph.edges()}
    node_label_colors = {node: get_node_label_colors(traces=traces, cmap=cmap)[node_attributes[node]['host_name']] for
                         node
                         in
                         graph.nodes()}

    return {
        "graph": graph,
        "node_labels": node_labels,
        "edge_labels": edge_labels,
        "node_label_colors": node_label_colors,
        "edge_label_colors": edge_label_colors,
        "trace_id": root["trace_id"].to_list().pop()
    }


def visualize_nx_graph(graph_dict: dict[
    str, nx.DiGraph | dict[tuple, dict] | dict[str, dict] | list[tuple[float, float]]]):
    graph = graph_dict["graph"]
    node_labels = graph_dict["node_labels"]
    edge_labels = graph_dict["edge_labels"]
    node_label_colors = graph_dict["node_label_colors"]
    edge_label_colors = graph_dict["edge_label_colors"]
    trace_id = graph_dict["trace_id"]

    pos = nx.planar_layout(graph)
    plt.figure(figsize=(10, 15), dpi=200)
    nx.draw(graph,
            pos=pos,
            node_color=list(node_label_colors.values()),
            node_size=100,
            linewidths=0.5,
            edge_color=list(edge_label_colors.values()),
            )
    nx.draw_networkx_labels(graph,
                            pos=pos,
                            labels=node_labels,
                            font_size=4)

    nx.draw_networkx_edge_labels(graph,
                                 pos=pos,
                                 edge_labels=edge_labels,
                                 font_size=4,
                                 label_pos=0.7)
    plt.savefig(
        "\\".join([VISUALIZATION_OUTPUT_DIRECTORY_PATH, f'networkx-visualization\\{trace_id}.png']))


def visualize_pyvis_graph_from_nx(graph_dict: dict[
    str, nx.DiGraph | list[str] | dict[tuple, dict] | dict[str, dict] | list[tuple[float, float]]]):
    graph = graph_dict["graph"]
    node_labels = graph_dict["node_labels"]
    edge_labels = graph_dict["edge_labels"]
    node_label_colors = graph_dict["node_label_colors"]
    edge_label_colors = graph_dict["edge_label_colors"]
    trace_id = graph_dict["trace_id"]
    network = Network()
    network.from_nx(graph)
    for node in network.nodes:
        node['label'] = node_labels[node['span_id']]
        node['color'] = mcolors.to_hex(node_label_colors[node['span_id']])

    for edge in network.edges:
        edge['label'] = edge_labels[(edge['from'], edge['to'])]
        edge['color'] = mcolors.to_hex(edge_label_colors[(edge['from'], edge['to'])])

    network.write_html("\\".join([VISUALIZATION_OUTPUT_DIRECTORY_PATH, f'pyvis-visualization\\{trace_id}.html']))
