import pandas as pd
from neomodel import db
from sklearn.preprocessing import OneHotEncoder

from Neo4jManipulation.deeptralog.model import DeepTraLogDto, DeepTraLogTrace
from Neo4jManipulation.model import ProcessedFile


@db.transaction
def file_to_db_deeptralog(folder_name, file_name):
    df = pd.read_csv(folder_name + file_name)

    if len(df.columns) != 11:
        return

    print(len(df))

    df = encode(df, True)

    root_df_list = df.loc[df['isParent'] == 1].values.tolist()
    root_dto_list = [DeepTraLogDto.from_list(el) for el in root_df_list]

    for root_dto in root_dto_list:
        root_span_id = root_dto.span_id

        root_node = DeepTraLogTrace(
            uuid=root_span_id,
            level=0,
            trace_id=root_dto.trace_id,
            execution_time=0,
            is_root=root_dto.is_root,
            service_content_travel=root_dto.service_content_travel,
            span_type_entry=root_dto.span_type_entry,
            span_type_exit=root_dto.span_type_exit,
            component_spring_mvc=root_dto.component_spring_mvc,
            component_spring_rest_template=root_dto.component_spring_rest_template,
            peer_content_ticket_info=root_dto.peer_content_ticket_info,
            peer_content_travel=root_dto.peer_content_travel,
            is_error=root_dto.is_error,
        )

        root_node.save()

        generate_deeptralog_graph(df, parent_node=root_node, parent_level=0, parent_stop_time=0)

        pf = ProcessedFile(name=file_name)
        pf.save()


def generate_deeptralog_graph(df, parent_node, parent_level, parent_stop_time):
    children = df.loc[df['ParentSpan'] == parent_node.uuid].values.tolist()
    children = [DeepTraLogDto.from_list(el) for el in children]

    for childDto in children:

        delta_seconds = (childDto.end_time - childDto.start_time).total_seconds()

        child_entity = DeepTraLogTrace(
            uuid=childDto.span_id,
            level=parent_level + 1,
            trace_id=childDto.trace_id,
            execution_time=delta_seconds,
            is_root=childDto.is_root,
            service_content_travel=childDto.service_content_travel,
            span_type_entry=childDto.span_type_entry,
            span_type_exit=childDto.span_type_exit,
            component_spring_mvc=childDto.component_spring_mvc,
            component_spring_rest_template=childDto.component_spring_rest_template,
            peer_content_ticket_info=childDto.peer_content_ticket_info,
            peer_content_travel=childDto.peer_content_travel,
            is_error=childDto.is_error,
        )

        child_entity.save()

        if parent_level == 0:
            edge_value = None
        else:
            edge_value = (childDto.start_time - parent_stop_time).total_seconds() * 1000
            edge_value = abs(edge_value)

        child_entity.parent.connect(parent_node, edge_value)
        generate_deeptralog_graph(df, child_entity, parent_level=parent_level + 1, parent_stop_time=childDto.end_time)


def encode(df, include_peer_and_service_content=False):
    df['isParent'] = df['ParentSpan'].apply(lambda x: 1 if x == "-1" else 0)
    columns_to_encode = ['SpanType', 'Component']

    if include_peer_and_service_content:
        columns_to_encode.extend(['Peer_Content', 'Service_Content'])

        df['Peer_Content'] = df['Peer'].apply(lambda x: '-'.join(x.split('-')[1:-1]) if '-' in x else 'unknown')
        df['Service_Content'] = df['Service'].apply(lambda x: '-'.join(x.split('-')[1:-1]) if '-' in x else 'unknown')

    encoder = OneHotEncoder(sparse=False)
    encoded_data = encoder.fit_transform(df[columns_to_encode])
    encoded_df = pd.DataFrame(encoded_data, columns=encoder.get_feature_names_out(columns_to_encode))
    result_df = pd.concat([df.reset_index(drop=True), encoded_df.reset_index(drop=True)], axis=1)
    result_df.drop(columns=['URL', 'SpanType', 'Service', 'Peer', 'Component'], inplace=True)

    if include_peer_and_service_content:
        result_df.drop(columns=['Peer_Content', 'Service_Content'], inplace=True)

    result_df['IsError'] = result_df['IsError'].astype(int)
    return result_df
