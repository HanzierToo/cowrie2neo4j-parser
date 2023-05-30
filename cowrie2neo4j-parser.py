import argparse
import json
import re
from datetime import datetime
from neo4j import GraphDatabase
import codecs
import binascii

# Connect to the Neo4j server -- Replace <BOLT_IP> with your Neo4j instance, and <USERNAME> and <PASSWORD>.
driver = GraphDatabase.driver("bolt://<BOLT_IP>:7687", auth=("<USERNAME>", "<PASSWORD>"))

# Define the Cypher queries
queries = []


def get_node_category(node):
    # Extract the category from the node data
    # Modify this logic based on your specific requirements
    if "login" in node:
        return "Login"
    elif "connection" in node:
        return "Connection"
    elif "version" in node:
        return "Version"
    elif re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", node):  # Check if node is an IP address
        return "IP_Address"
    elif re.match(r"[a-fA-F0-9]{12}", node):  # Check if node is a session/instance ID
        return "Session_ID"
    else:
        return "Other"


def insert_node_cypher(node, label):
    # Generate a unique name for the node based on its data
    node_name = f"{node.replace(' ', '_')}"
    cypher = f'MERGE (:{label} {{property: "{node}", name: "{node_name}"}})'
    queries.append(cypher)


def insert_relationship_cypher(source, target, relationship):
    # Generate unique names for the source and target nodes based on their data
    source_name = f"{source.replace(' ', '_')}"
    target_name = f"{target.replace(' ', '_')}"
    # Generate a unique type for the relationship based on its data
    relationship_type = f"Type_{re.sub('[^a-zA-Z0-9_]', '', relationship.replace(' ', '_'))}"
    cypher = f'MATCH (a), (b) WHERE a.name = "{source_name}" AND b.name = "{target_name}" MERGE (a)-[:{relationship_type}]->(b)'
    queries.append(cypher)


# Parse and process the JSON log file
def process_json_log(file_path, log_date):
    with open(file_path, "r") as file:
        unique_nodes = set()
        unique_relationships = set()

        for line in file:
            data = json.loads(line)

            # Assign the log date to all data entries from the file
            data["log_date"] = log_date

            # Determine the event type
            event_id = data.get("eventid", "")

            if event_id == "cowrie.session.connect":
                # Extract relevant data and create nodes
                src_ip = data.get("src_ip", "")
                dst_ip = data.get("dst_ip", "")
                session = data.get("session", "")

                # Check for duplicate nodes
                if src_ip not in unique_nodes:
                    insert_node_cypher(src_ip, "IP_Address")
                    unique_nodes.add(src_ip)

                if dst_ip not in unique_nodes:
                    insert_node_cypher(dst_ip, "IP_Address")
                    unique_nodes.add(dst_ip)

                if session not in unique_nodes:
                    insert_node_cypher(session, "Session_ID")
                    unique_nodes.add(session)

                # Check for duplicate relationships
                relationship1 = f"{src_ip}_{session}"
                relationship2 = f"{session}_{dst_ip}"

                if relationship1 not in unique_relationships:
                    insert_relationship_cypher(src_ip, session, "CONNECTED_TO")
                    unique_relationships.add(relationship1)

                if relationship2 not in unique_relationships:
                    insert_relationship_cypher(session, dst_ip, "CONNECTED_TO")
                    unique_relationships.add(relationship2)

            elif event_id == "cowrie.login.failed":
                # Extract relevant data and create nodes
                src_ip = data.get("src_ip", "")
                username = data.get("username", "")
                password = data.get("password", "")
                session = data.get("session", "")

                # Check for duplicate nodes
                if src_ip not in unique_nodes:
                    insert_node_cypher(src_ip, "IP_Address")
                    unique_nodes.add(src_ip)

                if username not in unique_nodes:
                    insert_node_cypher(username, "Login")
                    unique_nodes.add(username)

                if session not in unique_nodes:
                    insert_node_cypher(session, "Session_ID")
                    unique_nodes.add(session)

                # Check for duplicate relationships
                relationship1 = f"{session}_{username}"
                relationship2 = f"{session}_{password}"

                if relationship1 not in unique_relationships:
                    insert_relationship_cypher(session, username, "FAILED_LOGIN")
                    unique_relationships.add(relationship1)

                if relationship2 not in unique_relationships:
                    insert_relationship_cypher(session, password, "USED_PASSWORD")
                    unique_relationships.add(relationship2)

            elif event_id == "cowrie.command.input":
                # Extract relevant data and create nodes
                src_ip = data.get("src_ip", "")
                session = data.get("session", "")
                input_data = data.get("input", "")

                # Check for duplicate nodes
                if src_ip not in unique_nodes:
                    insert_node_cypher(src_ip, "IP_Address")
                    unique_nodes.add(src_ip)

                if session not in unique_nodes:
                    insert_node_cypher(session, "Session_ID")
                    unique_nodes.add(session)

                # Check if input data is in hexadecimal format
                try:
                    decoded_input_data = codecs.decode(input_data.encode(), "hex").decode()
                except binascii.Error:
                    # Input data is not in hexadecimal format, treat it as a regular string
                    decoded_input_data = input_data.replace("\\", "\\\\").replace('"', "'")

                # Check for duplicate command nodes
                command_node_label = f"Command_{session}"
                if decoded_input_data not in unique_nodes:
                    insert_node_cypher(decoded_input_data, command_node_label)
                    unique_nodes.add(decoded_input_data)

                # Check for duplicate relationships
                relationship = f"{session}_{decoded_input_data}"
                if relationship not in unique_relationships:
                    insert_relationship_cypher(session, decoded_input_data, "EXECUTED_COMMAND")
                    unique_relationships.add(relationship)

            # Add more conditions for other event types if needed


def execute_cypher_queries():
    with driver.session() as session:
        for query in queries:
            session.run(query)


def close_connection():
    driver.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse JSON log file and insert data into Neo4j.")
    parser.add_argument("--file", dest="file_path", help="Path to the JSON log file")
    args = parser.parse_args()

    file_path = args.file_path

    if file_path:
        # Extract the date from the file name (if present)
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", file_path)
        if date_match:
            log_date = date_match.group()
        else:
            log_date = input("Enter the date (YYYY-MM-DD) for the log file: ")

        # Validate the date format
        try:
            datetime.strptime(log_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please enter the date in the format YYYY-MM-DD.")
            exit(1)

        # Process the JSON log file
        process_json_log(file_path, log_date)
        execute_cypher_queries()
        close_connection()
    else:
        print("Please provide the path to the JSON log file using the --file argument.")
