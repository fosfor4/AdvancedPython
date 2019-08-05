import logging
from functools import wraps


logger = logging.getLogger('decorators')


def logged(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        logger.debug(f'Function: {func.__name__}, Input_Data: {request}')
        return func(request, *args, **kwargs)
    return wrapper