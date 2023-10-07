from neomodel import StructuredNode, FloatProperty, \
    RelationshipTo, IntegerProperty

from Neo4jManipulation.model import ParentTraceRelationship


class DeepTraLogTrace(StructuredNode):
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
    def __init__(self, start_time, end_time, span_id, trace_id, parent_span, is_error, is_root,
                 span_type_entry, span_type_exit, component_spring_mvc, component_spring_rest_template,
                 component_mongodb_driver, component_rabbitmq_producer, component_rabbitmq_consumer,
                 component_spring_async, component_tomcat, peer_content_order,
                 peer_content_ticket_info, peer_content_travel, service_content_travel,
                 service_content_order, service_content_station):

        self.start_time = start_time
        self.end_time = end_time
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
        self.component_spring_mongodb_driver = component_mongodb_driver
        self.component_rabbitmq_producer = component_rabbitmq_producer
        self.component_rabbitmq_consumer = component_rabbitmq_consumer
        self.component_spring_async = component_spring_async
        self.component_tomcat = component_tomcat
        self.peer_content_order = peer_content_order
        self.peer_content_ticket_info = peer_content_ticket_info
        self.peer_content_travel = peer_content_travel
        self.service_content_order = service_content_order
        self.service_content_station = service_content_station

    @staticmethod
    def from_list(lst):
        return DeepTraLogDto(*lst)

    @staticmethod
    def from_dic(dic):
        values = ['StartTime', 'EndTime', 'SpanId', 'TraceId', 'ParentSpan',
                  'IsError', 'isParent', 'SpanType_Entry', 'SpanType_Exit',
                  'Component_SpringMVC', 'Component_SpringRestTemplate',
                  'Component_mongodb-driver', 'Component_rabbitmq_producer', 'Component_rabbitmq_consumer', 'Component_Tomcat', 'Component_SpringAsync',
                  'Peer_Content_ticketinfo', 'Peer_Content_travel', 'Peer_Content_order',
                  'Service_Content_travel', 'Service_Content_order', 'Service_Content_station']

        for key in values:
            if key not in dic:
                dic[key] = None

        start_time = dic['StartTime']
        end_time = dic['EndTime']
        span_id = dic['SpanId']
        trace_id = dic['TraceId']
        parent_span = dic['ParentSpan']
        is_error = dic['IsError']
        is_root = dic['isParent']
        span_type_entry = dic['SpanType_Entry']
        span_type_exit = dic['SpanType_Exit']
        component_spring_mvc = dic['Component_SpringMVC']
        component_spring_rest_template = dic['Component_SpringRestTemplate']
        component_mongodb_driver = dic['Component_mongodb-driver']
        component_rabbitmq_producer = dic['Component_rabbitmq_producer']
        component_rabbitmq_consumer = dic['Component_rabbitmq_consumer']
        component_spring_async = dic['Component_SpringAsync']
        component_tomcat = dic['Component_Tomcat']
        peer_content_order = dic['Peer_Content_order']
        peer_content_ticket_info = dic['Peer_Content_ticketinfo']
        peer_content_travel = dic['Peer_Content_travel']
        service_content_travel = dic['Service_Content_travel']
        service_content_order = dic['Service_Content_order']
        service_content_station = dic['Service_Content_station']

        return DeepTraLogDto(start_time, end_time, span_id, trace_id, parent_span, is_error, is_root,
                             span_type_entry, span_type_exit, component_spring_mvc, component_spring_rest_template,
                             component_mongodb_driver, component_rabbitmq_producer, component_rabbitmq_consumer,
                             component_spring_async, component_tomcat, peer_content_order,
                             peer_content_ticket_info, peer_content_travel, service_content_travel,
                             service_content_order, service_content_station)
