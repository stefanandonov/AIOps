import pandas as pd
from neomodel import db

from Neo4jManipulation.deeptralog.model import DeepTraLogDto, DeepTraLogTrace
from Neo4jManipulation.model import ProcessedFile

@db.transaction
def file_to_db_deeptralog(folder_name, file_name):
    df = pd.read_csv(folder_name + file_name)

    if len(df.columns) != 11:
        return

    print(len(df))

    root_df_list = df.loc[df['ParentSpan'] == "-1"].values.tolist()
    root_dto_list = [DeepTraLogDto.from_list(el) for el in root_df_list]

    for root_dto in root_dto_list:
        root_span_id = root_dto.span_id

        root_node = DeepTraLogTrace(
            span_id=root_span_id,
            level=0,
            trace_id=root_dto.trace_id,
            name=file_name,
            execution_time=0,
            path=root_dto.url,
            service=root_dto.service,
            peer=root_dto.peer,
            component=root_dto.component,
            span_type=root_dto.span_type,
            is_error=root_dto.is_error
        )

        root_node.save()

        generate_deeptralog_graph(df, parent_node=root_node, parent_level=0, parent_stop_time=0)

        pf = ProcessedFile(name=file_name)
        pf.save()


def generate_deeptralog_graph(df, parent_node, parent_level, parent_stop_time):
    children = df.loc[df['ParentSpan'] == parent_node.span_id].values.tolist()
    children = [DeepTraLogDto.from_list(el) for el in children]

    for childDto in children:

        delta_seconds = (childDto.end_time - childDto.start_time).total_seconds()

        child_entity = DeepTraLogTrace(
            span_id=childDto.span_id,
            level=parent_level + 1,
            trace_id=childDto.trace_id,
            name=childDto.span_id,
            execution_time=delta_seconds,
            path=childDto.url,
            service=childDto.service,
            peer=childDto.peer,
            component=childDto.component,
            span_type=childDto.span_type,
            is_error=childDto.is_error
        )

        child_entity.save()

        if parent_level == 0:
            edge_value = None
        else:
            edge_value = (childDto.start_time - parent_stop_time).total_seconds() * 1000
            edge_value = abs(edge_value)

        child_entity.parent.connect(parent_node)
        generate_deeptralog_graph(df, child_entity, parent_level=parent_level + 1, parent_stop_time=childDto.end_time)
