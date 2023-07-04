from neomodel import config, StructuredNode, StructuredRel, UniqueIdProperty, IntegerProperty, StringProperty, \
    FloatProperty, \
    RelationshipTo

#config.DATABASE_URL = f'neo4j://databaseNAME:PASSWORD@localhost'
config.DATABASE_URL = f'neo4j://neo4j:12345@localhost'


class ParentTraceRelationship(StructuredRel):
    ms_parent_to_child = FloatProperty()


# has to be hashable
class Trace(StructuredNode):
    uid = UniqueIdProperty()
    span_id = StringProperty()
    physical_host = StringProperty()
    execution_time = FloatProperty()
    path = StringProperty()
    scheme = StringProperty()
    method = StringProperty()
    level = IntegerProperty()
    parent = RelationshipTo('Trace', 'PARENT_TRACE', model=ParentTraceRelationship)


class ProcessedFile(StructuredNode):
    """Save processed files in database as back-up and easier recovery."""
    uid = UniqueIdProperty()
    name = StringProperty()
