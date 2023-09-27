import pandas as pd

from pandas.core.groupby import DataFrameGroupBy

from preprocessing.preprocessing_utils import *

edge_columns_encoded = ['call_type', 'call_type_CSF', 'call_type_FlyRemote', 'call_type_JDBC',
                        'call_type_LOCAL', 'call_type_OSB', 'call_type_RemoteProcess', 'elapsed_time'
                        ]
categorical_columns_to_encode = ['call_type', 'host_name', 'data_source_name', 'service_name']

def load_trace_data_from_date(date: str) -> dict[str, pd.DataFrame]:
    # date: {trace_type: trace_df}
    print(f"Loading traces from date: {date}...")

    data = {
        extract_file_name(path): preprocess_dataset(pd.read_csv(path), DataSource.TRACE) for path in
        list_file_paths_by_data_source_and_date(DataSource.TRACE, date)
    }

    print(f"Successfully loaded traces from date: {date}!")

    return data


def extract_all_traces_from_date(date: str) -> list[str]:
    return list(set([trace_id for df in load_trace_data_from_date(date).values() for trace_id in df.trace_id.values]))


def concat_traces_from_date(date: str) -> pd.DataFrame:
    print(f"Concatenating trace dataframes from date: {date}...")

    result = pd.concat([df for df in load_trace_data_from_date(date).values()])

    print(f"Successfully concatenated datasets from date: {date}!")

    return result


def one_hot_encode_traces(df: pd.DataFrame) -> pd.DataFrame:
    print(f"Encoding concatenated trace dataframes...")

    result = df.copy(deep=True)

    for column in categorical_columns_to_encode:
        result = pd.concat([result, pd.get_dummies(df[[column]])], axis=1)

    print(f"Successfully encoded concatenated trace dataframes...")

    return result


def group_traces_by_trace_id_from_date(date: str) -> DataFrameGroupBy:
    print(f"Grouping traces by trace_id from date: {date}...")

    result = one_hot_encode_traces(concat_traces_from_date(date)).groupby('trace_id')

    print(f"Successfully grouped traces by trace_id from date: {date}!")

    return result


def sort_traces_by_timestamp(traces: pd.DataFrame) -> pd.DataFrame:
    return traces.sort_index(ascending=True)


def find_root_node_from_trace(traces: pd.DataFrame) -> pd.DataFrame:
    return traces[traces['parent_span_id'].isna()]
