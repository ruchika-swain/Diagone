from flask import Blueprint, request, jsonify
from repository.path_repository import generate_paths
from service.post_paths_to_db import post_graph_paths

path_blueprint = Blueprint("path", __name__)

@path_blueprint.route('/generate-paths', methods=['POST'])
def generate_paths_api():
    try:
        # Parse input parameters
        data = request.json

        # Validate input parameters
        required_fields = ['client', 'service', 'api_split', 'topic', 'consumer_split', 'min_length', 'max_length', 'num_paths']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required parameters'}), 400

        # Generate paths using the repository logic
        paths = generate_paths(
            client=data['client'],
            service=data['service'],
            api_split=data['api_split'],
            topic=data['topic'],
            consumer_split=data['consumer_split'],
            min_length=data['min_length'],
            max_length=data['max_length'],
            num_paths=data['num_paths']
        )
        base_url = "http://localhost:8081/api/graph-paths"
        post_graph_paths(base_url, paths)

        return jsonify({'paths': paths}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@path_blueprint.route('/insert-paths', methods=['POST'])
def insert_custom_paths():
    try:
        # Parse input parameters
        data = request.json

        # Validate input
        if 'paths' not in data or not isinstance(data['paths'], list):
            return jsonify({'error': 'Invalid payload. Expected a "paths" array.'}), 400

        paths = data['paths']

        # Base URL for posting paths
        base_url = "http://localhost:8081/api/graph-paths"

        # Post paths to the external API
        responses = []
        for path in paths:
            post_graph_paths(base_url, [path])
            # try:
            #     response = post_graph_paths(base_url, [path])  # Reusing the post_graph_paths function
            #     responses.append({
            #         'path': path,
            #         'status_code': response.status_code,
            #         'response': response.json() if response.status_code == 200 else response.text
            #     })
            # except Exception as e:
            #     responses.append({
            #         'path': path,
            #         'error': str(e)
            #     })

        return jsonify({'paths': paths}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

