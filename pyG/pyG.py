from neo4j import GraphDatabase
import pandas as pd
import torch
from torch_geometric.data import Data
from encoders import SequenceEncoder, CategoricalEncoder, IdentityEncoder
import neomodel

# database connection
url = 'bolt://localhost:7687'
user = 'neo4j'
password = '12345'

driver = GraphDatabase.driver(url, auth=(user, password))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print("Torch device:", device)


def fetch_data(query, trace_uid):
    with driver.session() as session:
        result = session.run(query, parameters={"trace_uid": trace_uid})
        return pd.DataFrame([r.values() for r in result], columns=result.keys())


def load_node(cypher, index_col, trace_uid, encoders=None, **kwargs):
    # Execute the cypher query and retrieve data from Neo4j
    df = fetch_data(cypher, trace_uid)
    df.set_index(index_col, inplace=True)
    # Define node mapping
    mapping = {index: i for i, index in enumerate(df.index.unique())}
    # Define node features
    x = None
    if encoders is not None:
        xs = [encoder(df[col]) for col, encoder in encoders.items()]
        x = torch.cat(xs, dim=-1)

    return x, mapping


def load_edge(cypher, trace_uid, src_index_col, src_mapping, dst_index_col, dst_mapping,
              encoders=None, **kwargs):
    # Execute the cypher query and retrieve data from Neo4j
    df = fetch_data(cypher, trace_uid)
    # Define edge index
    src = [src_mapping[index] for index in df[src_index_col]]
    dst = [dst_mapping[index] for index in df[dst_index_col]]
    edge_index = torch.tensor([src, dst])
    # Define edge features
    edge_attr = None
    if encoders is not None:
        edge_attrs = [encoder(df[col]) for col, encoder in encoders.items()]
        edge_attr = torch.cat(edge_attrs, dim=-1)

    return edge_index, edge_attr


def create_data_object_for_trace(trace_uid: str):
    print(f"Processing trace {trace_uid}-----------------------------------")
    trace_query = """
            MATCH (n:Trace{uid:$trace_uid})-[*]-(children:Trace)
            WITH  n + COLLECT(DISTINCT children) AS all_traces
            UNWIND all_traces as trace
            RETURN trace.method as method, //categorical data
                      trace.physical_host as physical_host, //categorical data
                      trace.scheme as scheme, //categorical data
                      trace.execution_time as execution_time, //only normalization?
                      trace.level as level, //as it is, numerical value
                      trace.path as path, //SequenceEncoder
                      trace.span_id as span_id, //not useful
                      trace.uid as uid //not useful
            ORDER by trace.uid
            """
    edge_query = """
            MATCH  (n:Trace{uid:$trace_uid})-[rel:PARENT_TRACE*]-(children:Trace)
            WITH collect(rel) as rels
            WITH REDUCE(output = [], r in rels | output + r) as flattened_rels
            UNWIND flattened_rels as rel
            RETURN startNode(rel).uid AS source_uid, endNode(rel).uid as dest_uid, rel.ms_parent_to_child as miliseconds
              """

    print("Loading node-----------------------------------")
    # Load data from queries
    trace_x, trace_mapping = load_node(trace_query, index_col='uid', trace_uid=trace_uid, encoders={
        'path': SequenceEncoder(),
        'method': CategoricalEncoder(),
        'scheme': CategoricalEncoder(),
        'physical_host': CategoricalEncoder(),
        'execution_time': IdentityEncoder(dtype=torch.double)
    })

    print("Loading edge-----------------------------------")
    edge_index, edge_label = load_edge(
        edge_query, trace_uid=trace_uid,
        src_index_col='source_uid',
        src_mapping=trace_mapping,
        dst_index_col='dest_uid',
        dst_mapping=trace_mapping,  # src and dst mapping are same cause our graph is Homo
        encoders={'miliseconds': IdentityEncoder(dtype=torch.double)},
    )

    # build homogenous Graph
    data = Data()
    print("Creating data object-----------------------------------")
    # Add trace node features for message passing:
    data_object = Data(x=torch.eye(len(trace_mapping), device=device), edge_index=edge_index)
    # data.to(device, non_blocking=True)
    return data_object


def get_all_root_traces_uid():
    query = """
            MATCH (t:Trace{level:0})
            RETURN t.uid
    """
    matches, _ = neomodel.db.cypher_query(query)
    print(matches)
    return matches[0][0]


def create_all_data_objects():
    root_traces_uids = get_all_root_traces_uid()
    data_object_list = []
    for rtu in root_traces_uids:
        data_object = create_data_object_for_trace(rtu)
        data_object_list.append(data_object)

    return data_object_list


def test_functionality():
    r = create_data_object_for_trace("416dda5752cd4d56a33d21581be1930f")
    print(r)


if __name__ == "__main__":
    # TODO: First, we need to project the GDS in-memory graph. (Using neo4j GraphDataScience Library)
    test_functionality()
