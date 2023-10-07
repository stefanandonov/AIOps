import torch as torch

from Neo4jManipulation.deeptralog.model import DeepTraLogTrace
from torch_geometric.data import Data


def get_features(node):
    # map index to uuid
    return [node.level, node.component_spring_mvc, node.component_spring_rest_template, node.peer_content_ticket_info,
            node.peer_content_travel, node.service_content_travel, node.span_type_entry, node.span_type_exit]


def convert_to_data():
    edge_indexes = []

    nodes = DeepTraLogTrace.nodes.all()
    nodes_list = [node for node in nodes]
    features = [get_features(node) for node in nodes]

    for idx, node in enumerate(nodes):
        if len(node.parent) > 0:
            parent = node.parent[0]

            current_node_index = idx
            parent_node_index = nodes_list.index(parent)
            edge_indexes.append([parent_node_index, current_node_index])

    edge_index = torch.tensor(edge_indexes, dtype=torch.long)
    x = torch.tensor(features, dtype=torch.float)

    return Data(x=x, edge_index=edge_index.t().contiguous())
