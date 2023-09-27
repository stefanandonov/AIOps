import os
from neomodel import config, db
from dotenv import load_dotenv

load_dotenv()
environment_variables_list = list(os.environ.keys())
environment_variables_dict = {
    env_var: os.getenv(env_var) for env_var in environment_variables_list
}

for variable_name, variable_value in environment_variables_dict.items():
    if not variable_value:
        raise RuntimeError(f"{variable_name} is not set!")


def set_environment_variables(connection_string: str) -> str:
    for env_variable in environment_variables_list:
        if env_variable in connection_string:
            connection_string = connection_string.replace(env_variable, environment_variables_dict[env_variable])
    return connection_string


def connect_to_neo4j() -> bool:
    config.DATABASE_URL = set_environment_variables(environment_variables_dict['CONNECTION_STRING'])
    try:
        db.cypher_query('RETURN 1')
        print("Successfully connected to Neo4j database")
        return True
    except Exception as e:
        print(f"Failed to connect to Neo4j database: {e}")
        return False



