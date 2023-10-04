from mapping.n4j.neo4j_graph_utils import *
from mapping.user_defined.user_defined_graph_utils import get_node_attributes, get_edge_attributes, \
    check_if_graph_is_anomalous
from preprocessing.preprocessing_utils import list_date_folders
from preprocessing.trace_utils import group_traces_by_trace_id_from_date
from settings import *
from visualization.visualization_utils import nx_set_graph_attributes_and_labels, visualize_nx_graph, \
    visualize_pyvis_graph_from_nx


def run(dates: list[str] = list_date_folders()) -> None:
    '''
    :param dates:
    :return: None
    Processes the traces from specified dates, if none specified, processes the whole dataset
    '''
    if not connect_to_neo4j():
        raise Exception("Unable to connect to neo4j database!")

    for date in dates:
        df = group_traces_by_trace_id_from_date(date)
        for trace_id, trace_df in df:
            node_attributes = get_node_attributes(trace_df)
            edge_attributes = get_edge_attributes(trace_df)
            generate_neo4j_graph(node_attributes, edge_attributes)
            visualize_nx_graph(graph_dict=nx_set_graph_attributes_and_labels(traces=trace_df))
            visualize_pyvis_graph_from_nx(graph_dict=nx_set_graph_attributes_and_labels(traces=trace_df))


if __name__ == '__main__':
    run(['2020_04_11'])
