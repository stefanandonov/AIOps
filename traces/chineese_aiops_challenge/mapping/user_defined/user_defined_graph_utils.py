from collections import deque
import numpy as np
import pandas as pd
import datetime
from preprocessing.trace_utils import find_root_node_from_trace, edge_columns_encoded


def get_nodes_from_trace(traces: pd.DataFrame) -> list[str]:
    return [trace for trace in traces.span_id]


def get_edges_from_trace(traces: pd.DataFrame) -> list[tuple[str, str]]:
    return [tuple(trace) for trace in traces[['parent_span_id', 'span_id']].values if trace[0] is not np.nan]


def check_if_graph_is_anomalous(traces: pd.DataFrame) -> bool:
    root = find_root_node_from_trace(traces)
    print(f"Checking if trace with trace_id {root['trace_id']} is anomalous...")
    is_anomalous = not all(traces['service_is_not_anomalous'].values)
    print(f"Trace with trace_id {root['trace_id']} is anomalous {is_anomalous}")
    return is_anomalous


def calculate_node_depth(traces: pd.DataFrame) -> dict[str, int]:
    root = find_root_node_from_trace(traces)['span_id'].to_list().pop()

    print(
        f"Calculating node depth for trace with root node {root}")

    nodes = get_nodes_from_trace(traces)
    queue = deque([[root, 0]])
    result = {}
    visited = {trace_id: False for trace_id in nodes}

    while queue:
        current, level = queue.popleft()
        if not visited[current]:
            result[current] = level
            visited[current] = True
            neighbors = list(traces[traces.parent_span_id == current].span_id.values)
            for neighbor in neighbors:
                queue.append([neighbor, level + 1])

    print(f"Finished calculating node depth for graph with root node {root}")
    print(result)
    return result


def get_node_attributes(traces: pd.DataFrame, encode: bool = True) -> dict[str, dict]:
    root = find_root_node_from_trace(traces)
    print(f"Calculating node attributes for trace with trace_id {root['trace_id']}")

    node_attributes = {}

    node_depth = calculate_node_depth(traces)
    graph_is_anomalous = check_if_graph_is_anomalous(traces)

    for node in get_nodes_from_trace(traces):
        node_columns_encoded = list(set(traces.columns.values).difference(set(edge_columns_encoded)))
        row = traces.loc[traces.span_id == node, node_columns_encoded]
        attribute_dict: dict = row.to_dict(orient='records').pop()
        attribute_dict['start_time'] = row.index.to_pydatetime().tolist().pop().timestamp()
        attribute_dict['depth'] = node_depth[node]
        attribute_dict['graph_is_anomalous'] = graph_is_anomalous
        attribute_dict['service_is_anomalous'] = not attribute_dict["service_is_not_anomalous"]
        attribute_dict['is_root'] = row['parent_span_id'].to_list().pop() is np.nan
        if encode:
            redundant_columns = ['service_is_not_anomalous', 'parent_span_id', 'trace_id', 'service_name',
                                 'host_name', 'data_source_name']
            for column in redundant_columns:
                attribute_dict.pop(column)
        node_attributes[node] = attribute_dict
    print(f"Finished calculating node attributes for trace with trace_id {root['trace_id']}")
    print(node_attributes)
    return node_attributes


def get_edge_attributes(traces: pd.DataFrame, encode: bool = True) -> dict[tuple[str, str], dict]:
    root = find_root_node_from_trace(traces)
    print(f"Calculating edge attributes for trace with trace_id {root['trace_id']}")

    edge_attributes = {}

    root = find_root_node_from_trace(traces)

    for edge in get_edges_from_trace(traces):
        row = traces.loc[(traces.parent_span_id == edge[0]) & (traces.span_id == edge[1]), edge_columns_encoded]
        attribute_dict: dict = row.to_dict(orient='records').pop()
        attribute_dict['milliseconds_from_root'] = (row.index.values.item() - root.index.values.item()) / 1e6
        if encode:
            attribute_dict.pop('call_type')
        edge_attributes[edge] = attribute_dict

    print(f"Finished calculating edge attributes for trace with trace_id {root['trace_id']}")
    print(edge_attributes)
    return edge_attributes
