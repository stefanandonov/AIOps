import datetime

from neomodel import StructuredNode, UniqueIdProperty, StringProperty, \
    FloatProperty, \
    RelationshipTo, IntegerProperty

from Neo4jManipulation.model import ParentTraceRelationship


class DeepTraLogTrace(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty()
    level = IntegerProperty()
    execution_time = FloatProperty()
    path = StringProperty()
    span_type = StringProperty()
    service = StringProperty()
    span_id = StringProperty()
    trace_id = StringProperty()
    peer = StringProperty()
    parent_span = StringProperty()
    component = StringProperty()
    is_error = StringProperty()
    parent = RelationshipTo('DeepTraLogTrace', 'PARENT_TRACE', model=ParentTraceRelationship)

class DeepTraLogDto:
    def __init__(self, start_time, end_time, url, span_type, service, span_id, trace_id, peer, parent_span, component, is_error):
        self.start_time = datetime.datetime.fromtimestamp(start_time / 1000)
        self.end_time = datetime.datetime.fromtimestamp(end_time / 1000)
        self.url = url
        self.span_type = span_type
        self.service = service
        self.span_id = span_id
        self.trace_id = trace_id
        self.peer = peer
        self.parent_span = parent_span
        self.component = component
        self.is_error = is_error

    @staticmethod
    def from_list(lst):
        return DeepTraLogDto(*lst)