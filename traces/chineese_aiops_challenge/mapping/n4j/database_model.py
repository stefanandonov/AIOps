from neomodel import StructuredRel, UniqueIdProperty, StringProperty, IntegerProperty, StructuredNode, RelationshipTo, \
    BooleanProperty, DateTimeProperty, FloatProperty
from neomodel.contrib import SemiStructuredNode


class ParentSpanRelationship(StructuredRel):
    call_type = StringProperty()
    call_type_CSF = IntegerProperty()
    call_type_FlyRemote = IntegerProperty()
    call_type_JDBC = IntegerProperty()
    call_type_LOCAL = IntegerProperty()
    call_type_OSB = IntegerProperty()
    call_type_RemoteProcess = IntegerProperty()
    elapsed_time = IntegerProperty()
    milliseconds_from_root = IntegerProperty()


class Span(SemiStructuredNode):
    span_id = StringProperty()
    is_root = BooleanProperty()
    service_is_anomalous = BooleanProperty()
    graph_is_anomalous = BooleanProperty()
    depth = IntegerProperty()
    start_time = FloatProperty()
    parent_span = RelationshipTo('Span', 'PARENT_SPAN', model=ParentSpanRelationship)
