import torch as torch

from Neo4jManipulation.deeptralog.model import DeepTraLogTrace
from torch_geometric.data import Data


def resolve_index(node, uuid_to_index):
    uuid = node.uuid
    if uuid not in uuid_to_index:
        index = len(uuid_to_index)
        uuid_to_index[uuid] = index
    else:
        index = uuid_to_index[uuid]

    return index


def get_features(node, uuid_to_index):
    resolve_index(node, uuid_to_index)  # map index to uuid
    return [node.level, node.component_spring_mvc, node.component_spring_rest_template, node.peer_content_ticket_info,
            node.peer_content_travel, node.service_content_travel, node.span_type_entry, node.span_type_exit]


def convert_to_data():
    edge_indexes = []
    uuid_to_index_dic = {}

    nodes = DeepTraLogTrace.nodes.all()

    features = [get_features(node, uuid_to_index_dic) for node in nodes]

    for node in nodes:
        if len(node.parent) > 0:
            parent = node.parent[0]

            current_node_index = resolve_index(node, uuid_to_index_dic)
            parent_node_index = resolve_index(parent, uuid_to_index_dic)
            edge_indexes.append([parent_node_index, current_node_index])

    edge_index = torch.tensor(edge_indexes, dtype=torch.long)
    x = torch.tensor(features, dtype=torch.float)

    return Data(x=x, edge_index=edge_index.t().contiguous())
