import datetime

from neomodel import StructuredNode, UniqueIdProperty, StringProperty, \
    FloatProperty, \
    RelationshipTo, IntegerProperty

from Neo4jManipulation.model import ParentTraceRelationship


class DeepTraLogTrace(StructuredNode):
    uuid = UniqueIdProperty()
    level = IntegerProperty()
    execution_time = FloatProperty()
    is_root = IntegerProperty()
    service_content_travel = IntegerProperty()
    span_type_entry = IntegerProperty()
    span_type_exit = IntegerProperty()
    component_spring_mvc = IntegerProperty()
    component_spring_rest_template = IntegerProperty()
    peer_content_ticket_info = IntegerProperty()
    peer_content_travel = IntegerProperty()
    is_error = IntegerProperty()
    parent = RelationshipTo('DeepTraLogTrace', 'PARENT_TRACE', model=ParentTraceRelationship)


class DeepTraLogDto:
    def __init__(self, start_time, end_time, span_id, trace_id, parent_span, is_error, is_root, service_content_travel,
                 span_type_entry, span_type_exit, component_spring_mvc, component_spring_rest_template,
                 peer_content_ticket_info, peer_content_travel):
        self.start_time = datetime.datetime.fromtimestamp(start_time / 1000)
        self.end_time = datetime.datetime.fromtimestamp(end_time / 1000)
        self.span_id = span_id
        self.trace_id = trace_id
        self.parent_span = parent_span
        self.is_error = is_error
        self.is_root = is_root
        self.service_content_travel = service_content_travel
        self.span_type_entry = span_type_entry
        self.span_type_exit = span_type_exit
        self.component_spring_mvc = component_spring_mvc
        self.component_spring_rest_template = component_spring_rest_template
        self.peer_content_ticket_info = peer_content_ticket_info
        self.peer_content_travel = peer_content_travel

    @staticmethod
    def from_list(lst):
        return DeepTraLogDto(*lst)
