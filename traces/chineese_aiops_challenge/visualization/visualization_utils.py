# import pandas as pd
# import matplotlib.pyplot as plt
# import networkx as nx
# import matplotlib.colors as mcolors
# from pyvis.network import Network
# import datetime
#
# from preprocessing.trace_utils import get_graph_from_trace, find_root_node_from_trace
#
#
# def get_edge_label_colors(traces: pd.DataFrame, cmap: plt.cm = plt.get_cmap('Set1')):
#     return {label: cmap(i) for i, label in enumerate(sorted(traces.call_type.astype('str').unique()))}
#
#
# def get_node_label_colors(traces: pd.DataFrame, cmap: plt.cm = plt.get_cmap('Set1')):
#     return {label: cmap(i) for i, label in enumerate(sorted(traces.cmdb_id.unique()))}
#
#
# def set_graph_attributes___(df: pd.DataFrame, limit=10):
#     for trace_id, traces in df[:limit]:
#
#         graph = get_graph_from_trace(traces)
#
#         pos = nx.planar_layout(graph)
#
#         root, node_attributes, node_labels, edge_attributes, edge_labels = find_root_node_from_trace(
#             traces), {}, {}, {}, {}
#
#         print(f'Root: {root}')
#
#         print(f'Trace start time: {list(root.index.values).pop()}')
#
#         cmap = plt.get_cmap('Set1')
#
#         edge_label_colors = get_edge_label_colors(traces, cmap)
#         node_label_colors = get_node_label_colors(traces, cmap)
#
#         node_columns = ['cmdb_id', 'service_name', 'elapsed_time']
#
#         for node in graph.nodes():
#             row = traces.loc[traces.id == node, node_columns]
#
#             attribute_dict = row.to_dict(orient='records').pop()
#
#             node_attributes[node] = attribute_dict
#
#             node_labels[node] = f"{attribute_dict['cmdb_id']}"
#
#         edge_columns = ['service_name', 'call_type', 'data_source_name']
#
#         for edge in graph.edges():
#             row = traces.loc[(traces.pid == edge[0]) & (traces.id == edge[1]), edge_columns]
#
#             attribute_dict = row.to_dict(orient='records').pop()
#
#             attribute_dict['start_time'] = datetime.datetime.utcfromtimestamp(row.index.values.item() / 1e9).strftime(
#                 '%Y-%m-%d %H:%M:%S.%f')[:-3]
#
#             attribute_dict['milliseconds_from_root'] = (row.index.values.item() - root.index.values.item()) / 1e6
#
#             edge_attributes[edge] = attribute_dict
#
#             edge_labels[edge] = f"{attribute_dict['call_type']} {attribute_dict['milliseconds_from_root']} ms"
#
#         nx.set_node_attributes(graph, node_attributes)
#         nx.set_edge_attributes(graph, edge_attributes)
#
#         edge_colors = [edge_label_colors[edge_attributes[edge]['call_type']] for edge in graph.edges()]
#         node_colors = [node_label_colors[node_attributes[node]['cmdb_id']] for node in graph.nodes()]
#
#         plt.figure(figsize=(10, 15), dpi=200)
#
#         nx.draw(graph,
#                 pos=pos,
#                 node_color=node_colors,
#                 node_size=100,
#                 linewidths=0.5,
#                 edge_color=edge_colors,
#                 )
#
#         nx.draw_networkx_labels(graph,
#                                 pos=pos,
#                                 labels=node_labels,
#                                 font_size=5)
#
#         nx.draw_networkx_edge_labels(graph,
#                                      pos,
#                                      edge_labels=edge_labels,
#                                      font_size=5,
#                                      label_pos=0.7)
#
#         plt.savefig(rf"./networkx-visualization/{trace_id}.png")
#
#         network = Network()
#         network.from_nx(graph)
#
#         for node in network.nodes:
#             node['label'] = node['cmdb_id']
#             node['color'] = mcolors.to_hex(node_label_colors[node['cmdb_id']][:-1])
#             print(node)
#
#         for edge in network.edges:
#             edge['label'] = f"{edge['call_type']} {edge['milliseconds_from_root']} ms"
#             edge['color'] = mcolors.to_hex(edge_label_colors[edge['call_type']][:-1])
#         network.write_html(rf"./pyvis-visualization/{trace_id}.html")
#
#
# def get_node_colors(graph: nx.DiGraph, node_attributes: dict):
#     return [node_attributes[node]['cmdb_id'] for node in graph.nodes()]
#
#
# def visualize_nx_graph(graph: nx.DiGraph, pos):
#     plt.figure(figsize=(10, 15), dpi=200)
#     nx.draw(graph,
#             pos=pos,
#             node_color=node_colors,
#             node_size=100,
#             linewidths=0.5,
#             edge_color=edge_colors,
#             )
#
#     nx.draw_networkx_labels(graph,
#                             pos=pos,
#                             labels=node_labels,
#                             font_size=5)
#
#     nx.draw_networkx_edge_labels(graph,
#                                  pos=pos,
#                                  edge_labels=edge_labels,
#                                  font_size=5,
#                                  label_pos=0.7)
#
#     plt.savefig(rf"./networkx-visualization/{trace_id}.png")
#
#
# def visualize_pyvis_graph(network: Network, node_label_colors, edge_label_colors, trace_id):
#     for node in network.nodes:
#         node['label'] = node['cmdb_id']
#         node['color'] = mcolors.to_hex(node_label_colors[node['cmdb_id']][:-1])
#         print(node)
#
#     for edge in network.edges:
#         edge['label'] = f"{edge['call_type']} {edge['milliseconds_from_root']} ms"
#         edge['color'] = mcolors.to_hex(edge_label_colors[edge['call_type']][:-1])
#         network.write_html(rf"./pyvis-visualization/{trace_id}.html")
