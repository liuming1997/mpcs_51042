def weight(param):
    def outer(func):
        def inner(*args, **kwargs):
            func(*args, **kwargs)

        return inner

    return outer


def number(param):
    def outer(func):
        def inner(*args, **kwargs):
            func(*args, **kwargs)

        return inner

    return outer
