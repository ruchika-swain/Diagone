import requests
import json
from flask import Blueprint, request, jsonify

def post_graph_paths(base_url, paths):
    """
    Post graph paths to an external API.

    Args:
        base_url (str): The base URL of the external API (e.g., "http://localhost:8081/api/graph-paths").
        paths (list): A list of paths where each path is a string (e.g., "c1-s1a1-s2a2").
    """
    for path in paths:
        path_elements = path.split("-")
        previous_path_key = None

        # Process each element in the path
        for i, element in enumerate(path_elements):
            if element.startswith("s"):  # Service and API element
                service = f"s{element[1]}"
                api = f"a{element[3]}"
                path_key = f"{path_elements[i-1]}-{service}{api}-post"
                incoming_path = previous_path_key
                payload = [{
                    "pathKey": path_key,
                    "graphPathNode": {
                        "incomingPath": incoming_path,
                        "graphPathElement": {
                            "type": "HttpService",
                            "httpMethod": "POST",
                            "httpRoute": f"/{api}"
                        }
                    }
                }]
                endpoint = f"{base_url}/{service}"
                previous_path_key = path_key  # Update for the next element
            elif element.startswith("c"):  # Client element
                client = f"c{element[1]}"
                service = f"s{path_elements[1][1]}"
                path_key = f"NULL-{client}-{service}-inbound"
                payload = [{
                    "pathKey": path_key,
                    "graphPathNode": {
                        "incomingPath": None,
                        "graphPathElement": {
                            "type": "ExternalClient",
                            "clientId": client,
                            "requestType": "INBOUND"
                        }
                    }
                }]
                endpoint = f"{base_url}/{service}"
                previous_path_key = path_key  # Update for the next element
            else:
                continue

            print(json.dumps(payload, indent=4))
            response = requests.post(endpoint, json=payload)

