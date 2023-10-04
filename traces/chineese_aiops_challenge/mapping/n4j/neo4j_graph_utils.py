from neomodel import *
from mapping.n4j.database_model import Span

'''
trace (grouped) to n4j graph
'''


@db.transaction
def generate_neo4j_graph(node_attributes: dict[str, dict], edge_attributes: dict[tuple[str, str], dict]) -> None:
    for span, attributes in node_attributes.items():
        node: Span = Span(**attributes)
        node.save()

    for (parent_span, child_span), attributes in edge_attributes.items():
        child_node: Span = Span.nodes.get(span_id=child_span)
        parent_node: Span = Span.nodes.get(span_id=parent_span)
        parent_node.parent_span.connect(child_node, attributes)
