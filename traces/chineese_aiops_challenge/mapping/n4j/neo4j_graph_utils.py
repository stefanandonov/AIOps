from abc import ABC

import networkx as nx
from neomodel import *

config.DATABASE_URL = f'neo4j://neo4j:traces_password@localhost:7687/neo4j'

'''
trace (grouped) to n4j graph
'''


class ParentSpanRelationship(StructuredRel):
    uid = UniqueIdProperty()
    call_type = StringProperty()
    call_type_CSF = IntegerProperty()
    call_type_FlyRemote = IntegerProperty()
    call_type_JDBC = IntegerProperty()
    call_type_LOCAL = IntegerProperty()
    call_type_OSB = IntegerProperty()
    call_type_RemoteProcess = IntegerProperty()
    elapsed_time = IntegerProperty()
    success = IntegerProperty()
    start_time = StringProperty()
    milliseconds_from_root = IntegerProperty()


class Span(StructuredNode):
    uid = UniqueIdProperty()
    span_id = StringProperty(unique_index=True)
    cmdb_id = StringProperty()
    service_name = StringProperty()
    data_source_name = StringProperty()
    depth = IntegerProperty()
    parent_span = RelationshipTo('Span', 'PARENT_SPAN', model=ParentSpanRelationship)


@db.transaction
def generate_neo4j_graph(node_attributes: dict[str, dict], edge_attributes: dict[tuple[str, str], dict]) -> None:
    for span, attributes in node_attributes.items():
        node = Span(**attributes)
        node.save()

    for (parent_span, child_span), attributes in edge_attributes.items():
        child_node = Span.nodes.get(span_id=child_span)
        parent_node = Span.nodes.get(span_id=parent_span)
        parent_node.parent_span.connect(child_node, attributes)
