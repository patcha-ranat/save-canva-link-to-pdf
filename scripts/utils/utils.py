import logging


def set_logger(level_name: str):
    # set logger
    logger = logging.getLogger(level_name)
    logger.setLevel(logging.DEBUG)
    
    # set formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="%Y-%m-%d %I:%M:%S %p")
    
    # set handler
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger

def list_union(*lists) -> list:
    """
    Just like .union() in set, but maintain order

    list_union(A: list, B: list, C: list)
    """
    seen = set()
    result = []
    for lst in lists:
        for item in lst:
            if item not in seen:
                seen.add(item)
                result.append(item)
    return result

if __name__ == '__main__':
    a = [1, 2, 3]
    b = [2, 3, 4]
    c = [1, "a"]
    
    print(list_union(a, b, c))
