import random

def get_random_element(service, split, element_type):
    while True:
        service_index = random.randint(1, service)
        if element_type == "m" and split[service_index - 1] > 0:
            index = random.randint(1, split[service_index - 1])
            return f"s{str(service_index).zfill(2)}{element_type}{str(index).zfill(2)}"
        elif element_type != "m":
            index = random.randint(1, split[service_index - 1])
            return f"s{str(service_index).zfill(2)}{element_type}{str(index).zfill(2)}"
