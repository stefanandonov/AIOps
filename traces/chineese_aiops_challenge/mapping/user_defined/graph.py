import datetime
from collections import deque
from typing import List

import pandas as pd

from preprocessing.trace_utils import find_root_node_from_trace, node_columns, edge_columns


def get_nodes_from_trace(traces: pd.DataFrame) -> list[str]:
    return [trace for trace in traces.span_id]


def get_edges_from_trace(traces: pd.DataFrame) -> list[tuple[str, str]]:
    return [tuple(trace) for trace in traces[['parent_span_id', 'span_id']].values if trace[0] != 'None']


def calculate_node_depth(traces: pd.DataFrame) -> dict[str, int]:
    # bfs

    root = list(find_root_node_from_trace(traces)['span_id'].values).pop()
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

    return result


def get_node_attributes(traces: pd.DataFrame) -> dict[str, dict]:
    node_attributes = {}

    node_depth = calculate_node_depth(traces)

    for node in get_nodes_from_trace(traces):
        row = traces.loc[traces.span_id == node, node_columns]
        attribute_dict = row.to_dict(orient='records').pop()
        attribute_dict['depth'] = node_depth[node]
        node_attributes[node] = attribute_dict

    return node_attributes


def get_edge_attributes(traces: pd.DataFrame) -> dict[tuple[str, str], dict]:
    edge_attributes = {}

    root = find_root_node_from_trace(traces)

    for edge in get_edges_from_trace(traces):
        row = traces.loc[(traces.parent_span_id == edge[0]) & (traces.span_id == edge[1]), edge_columns]
        attribute_dict = row.to_dict(orient='records').pop()
        attribute_dict['start_time'] = datetime.datetime.utcfromtimestamp(row.index.values.item() / 1e9).strftime(
            '%Y-%m-%d %H:%M:%S.%f')[:-3]
        attribute_dict['milliseconds_from_root'] = (row.index.values.item() - root.index.values.item()) / 1e6
        edge_attributes[edge] = attribute_dict

    return edge_attributes
