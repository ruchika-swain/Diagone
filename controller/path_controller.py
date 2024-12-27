from flask import Blueprint, request, jsonify
from repository.path_repository import generate_paths

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

        return jsonify({'paths': paths}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
