import os
import re
from enum import Enum

import pandas as pd

DIR_PATH = r'E:\faks\Рударење на масивни податоци\AIOps挑战赛数据'
DATE_PATTERN = r'[0-9]{4}_[0-9]{2}_[0-9]{2}'


class DataSource(Enum):
    ESB = 1
    KPI = 2
    TRACE = 3


CN_TO_EN_MAP = {
    '业务指标': DataSource.ESB,
    '平台指标': DataSource.KPI,
    '调用链指标': DataSource.TRACE
}

EN_TO_CN_MAP = dict((v, k) for k, v in CN_TO_EN_MAP.items())


def list_date_folders():
    return [folder for folder in os.listdir(DIR_PATH) if re.match(DATE_PATTERN, folder)]


def list_folder_paths_by_data_source(src: DataSource) -> list[str]:
    return ["\\".join([DIR_PATH, folder, EN_TO_CN_MAP[src]]) for folder in list_date_folders()]


def list_file_paths_by_data_source(src: DataSource) -> list[list[str]]:
    return [["\\".join([folder, file]) for file in os.listdir(folder)] for folder in
            list_folder_paths_by_data_source(src)]


def list_folder_paths_by_date(date: str) -> list[str]:
    return ["\\".join([DIR_PATH, date, EN_TO_CN_MAP[src]]) for src in DataSource]


def list_file_paths_by_date(date: str) -> list[list[str]]:
    return [["\\".join([folder, file]) for file in os.listdir(folder)] for folder in list_folder_paths_by_date(date)]


def list_folder_paths_by_data_source_and_date(src: DataSource, date: str) -> list[str]:
    return ["\\".join([DIR_PATH, date, EN_TO_CN_MAP[src]])]


def list_file_paths_by_data_source_and_date(src: DataSource, date: str) -> list[str]:
    return [["\\".join([folder, file]) for file in os.listdir(folder)] for folder in
            list_folder_paths_by_data_source_and_date(src, date)].pop()


def extract_file_name(path: str) -> str:
    return path.split("\\")[-1].split(".")[0]


def extract_file_names(src: DataSource) -> set:
    if src != DataSource.ESB:
        return set([extract_file_name(path) for path in sum(list_file_paths_by_data_source(src), [])])


def rename_columns(df: pd.DataFrame, src: DataSource) -> pd.DataFrame:
    if src == DataSource.ESB:
        return df.rename(columns={'serviceName': 'service_name',
                                  'startTime': 'start_time',
                                  'avg_time': 'average_call_time',
                                  'num': 'total_number_of_calls',
                                  'succee_num': 'number_of_successful_calls',
                                  'succee_rate': 'successful_call_rate'})

    elif src == DataSource.KPI:
        return df.rename(columns={'itemid': 'item_id',
                                  'cmdb_id': 'host_id',
                                  'name': 'kpi_metric_name',
                                  'value': 'kpi_metric_value'})
    else:
        return df.rename(columns={'callType': 'call_type',
                                  'startTime': 'start_time',
                                  'elapsedTime': 'elapsed_time',
                                  'traceId': 'trace_id',
                                  'serviceName': 'service_name',
                                  'dsName': 'data_source_name',
                                  'id' : 'span_id',
                                  'pid': 'parent_span_id'})


def set_index(df: pd.DataFrame, src: DataSource) -> pd.DataFrame:
    if src != DataSource.KPI:
        df.set_index('start_time', inplace=True)

    else:
        df.set_index('timestamp', inplace=True)

    df.index = pd.to_datetime(df.index, unit='ms')

    return df


def preprocess_dataset(df: pd.DataFrame, src: DataSource) -> pd.DataFrame:
    return set_index(rename_columns(df, src), src)


def load_data(src_list: list[DataSource], date_list: list[str]) -> dict[str, dict[str, dict[str, pd.DataFrame]]]:
    data = {
        date: {
            data_source: {
                name: preprocess_dataset(pd.read_csv(path), data_source) for name, path in
                zip(extract_file_names(data_source), list_file_paths_by_data_source_and_date(data_source, date))
            }
            for data_source in src_list
        }
        for date in date_list
    }
    return data
