from mapping.n4j.neo4j_graph_utils import *
from mapping.nx.networkx_graph_utils import get_node_attributes, get_edge_attributes
from preprocessing.trace_utils import group_traces_by_trace_id_from_date

# def main() -> None:
#     for date in list_date_folders():
#         df = group_traces_by_trace_id_from_date(date)
#
#         for trace_id, trace_df in df:
#             node_attributes = get_node_attributes(trace_df)
#             edge_attributes = get_edge_attributes(trace_df)
#             generate_neo4j_graph(node_attributes, edge_attributes)


if __name__ == '__main__':
    df = group_traces_by_trace_id_from_date('2020_05_29')
    for trace_id, trace_df in df:
        node_attributes = get_node_attributes(trace_df)
        edge_attributes = get_edge_attributes(trace_df)
        generate_neo4j_graph(node_attributes, edge_attributes)

