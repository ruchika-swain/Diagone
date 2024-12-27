import random

def get_random_element(service, split, element_type):
    while True:
        service_index = random.randint(1, service)
        if element_type == "m" and split[service_index - 1] > 0:
            index = random.randint(1, split[service_index - 1])
            return f"s{service_index}{element_type}{index}"
        elif element_type != "m":
            index = random.randint(1, split[service_index - 1])
            return f"s{service_index}{element_type}{index}"
