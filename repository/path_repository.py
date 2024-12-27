from utils.random_utils import get_random_element
import random
import logging
import threading
from queue import Queue

def generate_elements(client, service, api_split, topic, consumer_split):
    elements = [f"c{i + 1}" for i in range(client)]
    elements += [f"s{i + 1}a{j + 1}" for i in range(service) for j in range(api_split[i])]
    elements += [f"t{i + 1}" for i in range(topic)]
    elements += [f"s{i + 1}m{j + 1}" for i in range(service) for j in range(consumer_split[i])]
    return elements

def generate_random_paths(elements, client, service, api_split, consumer_split, min_length, max_length, num_paths, queue):
    random_paths = []

    for _ in range(num_paths):
        path_length = random.randint(min_length, max_length)
        path = [f"c{random.randint(1, client)}"]
        used_elements = set(f"c{i + 1}" for i in range(client))

        while len(path) < path_length:
            next_element = random.choice(elements[1:])
            while next_element in used_elements:
                next_element = random.choice(elements[1:])
            path.append(next_element)
            used_elements.add(next_element)

        ensure_topic_constraints(path, service, api_split, consumer_split, used_elements)
        handle_m_elements(path, service, api_split, used_elements)
        check_three_consecutive_services(path)
        random_paths.append("-".join(path))

    queue.put(random_paths)

def check_three_consecutive_services(path):
    i = 2
    while i < len(path):
        if path[i].startswith("s") and (path[i][1] == path[i - 1][1] or path[i][1] == path[i - 2][1]):
            path.pop(i)
        else:
            i += 1

    return path

def ensure_topic_constraints(path, service, api_split, consumer_split, used_elements):
    idx = 0
    while idx < len(path):
        element = path[idx]
        if element.startswith("t"):
            if idx == 0 or not (path[idx - 1].startswith("s") and path[idx - 1][2] == "a"):
                preceding = get_random_element(service, api_split, "a")
                while preceding in used_elements:
                    preceding = get_random_element(service, api_split, "a")
                path.insert(idx, preceding)
                used_elements.add(preceding)
                idx += 1
            if idx == len(path) - 1 or not (path[idx + 1].startswith("s") and path[idx + 1][2] == "m"):
                succeeding = get_random_element(service, consumer_split, "m")
                while succeeding in used_elements:
                    succeeding = get_random_element(service, consumer_split, "m")
                path.insert(idx + 1, succeeding)
                used_elements.add(succeeding)
        idx += 1

def handle_m_elements(path, service, api_split, used_elements):
    for idx, element in enumerate(path):
        if element.startswith("s") and element[2] == "m" and idx > 0:
            prev = path[idx - 1]
            if prev.startswith("c") or (prev.startswith("s") and prev[2] in {"a", "m"}):
                replacement = get_random_element(service, api_split, "a")
                while replacement in used_elements:
                    replacement = get_random_element(service, api_split, "a")
                path[idx] = replacement
                used_elements.add(replacement)

def add_missing_lengths(paths, min_length, max_length, client, service, api_split):
    """Ensure paths of all lengths are present."""
    unique_paths = set(paths)
    path_lengths = {length: False for length in range(min_length, max_length + 1)}

    for path in paths:
        path_lengths[len(path.split("-"))] = True

    for length, covered in path_lengths.items():
        if not covered:
            path = [f"c{random.randint(1, client)}"]
            used_elements = set(f"c{i + 1}" for i in range(client))
            for _ in range(length - 1):
                element = get_random_element(service, api_split, "a")
                while element in used_elements:
                    element = get_random_element(service, api_split, "a")
                path.append(element)
                used_elements.add(element)
            check_three_consecutive_services(path)
            unique_paths.add("-".join(path))

    return list(unique_paths)

def generate_random_paths_multithreaded(elements, client, service, api_split, consumer_split, min_length, max_length, num_paths):
    """Generate random paths using multithreading."""
    logging.info("Started generating random paths with multithreading")
    no_threads = 3
    num_paths_per_thread= num_paths // no_threads
    queue = Queue()
    threads = []

    # Create threads
    for _ in range(no_threads):  # Two threads, each handling half of the paths
        thread = threading.Thread(
            target=generate_random_paths,
            args=(elements, client, service, api_split, consumer_split, min_length, max_length, num_paths_per_thread, queue)
        )
        threads.append(thread)
        thread.start()

    # Wait for threads to complete
    for thread in threads:
        thread.join()

    # Combine results
    all_paths = []
    while not queue.empty():
        all_paths.extend(queue.get())

    # Ensure all lengths are covered and remove duplicates
    logging.info("Ensuring all lengths are covered and removing duplicates")
    unique_paths = add_missing_lengths(all_paths, min_length, max_length, client, service, api_split)
    return list(set(unique_paths))

def generate_paths(client, service, api_split, topic, consumer_split, min_length, max_length, num_paths):
    elements = generate_elements(client, service, api_split, topic, consumer_split)
    return generate_random_paths_multithreaded(elements, client, service, api_split, consumer_split, min_length, max_length, num_paths)
