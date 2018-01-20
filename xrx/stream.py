from rx import Observable


def x_stream(iterable):
    return Observable \
        .from_(iterable)
