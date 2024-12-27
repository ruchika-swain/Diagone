class PathRequest:
    def __init__(self, client, service, api_split, topic, consumer_split, min_length, max_length, num_paths):
        self.client = client
        self.service = service
        self.api_split = api_split
        self.topic = topic
        self.consumer_split = consumer_split
        self.min_length = min_length
        self.max_length = max_length
        self.num_paths = num_paths
