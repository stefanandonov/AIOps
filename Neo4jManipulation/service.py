from datetime import datetime
import re
import json

import neomodel
from neomodel import db
from model import ProcessedFile, Trace, ParentTraceRelationship


def generate_graph(parent_data, parent_node, parent_level, parent_stop_time):
    """Recursive function to traverse the document and save nodes in database.
    Edge value is the difference between parent stop time and child start time."""

    if parent_data['children'] == [] or parent_data['children'] is None:
        return

    # key of node levels is level, value is number of nodes on that level
    for child in parent_data["children"]:
        span_id = child["trace_id"]
        physical_host = child["info"]["host"]

        regex_timestamp_start = r"meta.raw_payload.*-start"
        regex_timestamp_stop = r"meta.raw_payload.*-stop"

        path = ""
        scheme = ""
        method = ""
        for key in child["info"].keys():
            matches_start = re.findall(regex_timestamp_start, str(key))
            matches_stop = re.findall(regex_timestamp_stop, str(key))
            if matches_start:
                timestamp_start = datetime.strptime(
                    child["info"][key]["timestamp"], "%Y-%m-%dT%H:%M:%S.%f"
                )
                if "request" in child["info"][key]["info"].keys():
                    path = child["info"][key]["info"]["request"]["path"]
                    scheme = child["info"][key]["info"]["request"]["scheme"]
                    method = child["info"][key]["info"]["request"]["method"]

            if matches_stop:
                timestamp_stop = datetime.strptime(
                    child["info"][key]["timestamp"], "%Y-%m-%dT%H:%M:%S.%f"
                )

        delta_seconds = (timestamp_stop - timestamp_start).total_seconds()

        # node_features = [span_id, physical_host, delta_seconds, path, scheme, method]
        # print(node_features)

        child_node = Trace(
            span_id=span_id,
            name=span_id,
            physical_host=physical_host,
            execution_time=delta_seconds,
            path=path,
            scheme=scheme,
            method=method,
            level=parent_level + 1
        )
        child_node.save()

        if parent_level == 0:
            edge_value = None
        else:
            edge_value = (timestamp_start - parent_stop_time).total_seconds() * 1000
            edge_value = abs(edge_value)

        child_node.parent.connect(parent_node, {"ms_parent_to_child": edge_value})
        generate_graph(child, child_node, parent_level=parent_level + 1, parent_stop_time=timestamp_stop)


@db.transaction
def file_to_db(folder_name, file_name):
    """Initialization and execution in transaction of the process saving JSON file to database.
    Open the file, create root node, generate graph starting from the root node, create ProcessedFile for recovery.
    Transaction prevents partial results saved in database.
    """

    with open(folder_name + "/" + file_name) as read_file:
        json_data = json.load(read_file)

    root_span_id = file_name.replace(".json", "")  # json_file name

    root_node = Trace(span_id=root_span_id, physical_host=None, execution_time=None, path=None,
                      scheme=None,
                      method=None, level=0)
    root_node.save()

    # no info for root execution stop time
    generate_graph(parent_data=json_data, parent_node=root_node, parent_level=0, parent_stop_time=0)

    pf = ProcessedFile(name=file_name)
    pf.save()


def get_processed_files_hash():
    return {pf.name for pf in ProcessedFile.nodes.all()}


@db.transaction
def delete_all_traces():
    query = '''MATCH (n:Trace)
        DETACH DELETE n
    '''
    matches, _ = neomodel.db.cypher_query(query)


@db.transaction
def delete_all_processed_files():
    query = '''MATCH (n:ProcessedFile)
        DETACH DELETE n
    '''
    matches, _ = neomodel.db.cypher_query(query)


@db.transaction
def delete_all_from_db():
    query = '''MATCH (n)
        DETACH DELETE n
    '''
    matches, _ = neomodel.db.cypher_query(query)

