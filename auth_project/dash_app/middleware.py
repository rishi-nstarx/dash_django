import logging
import re

# Custom log handler to capture cache_id dynamically
class CacheIdLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.cache_id = None

    def emit(self, record):
        # Extract cache_id from log messages dynamically
        log_message = self.format(record)
        print(f"//////{log_message}///////")
        cache_id_match = re.search(r'dpd-initial-args-([a-f0-9]{32})', log_message)
        if cache_id_match:
            self.cache_id = cache_id_match.group(1)  # Extract the cache_id

    def get_cache_id(self):
        return self.cache_id


# Set up custom log handler
cache_id_handler = CacheIdLogHandler()
def setup_custom_logging():
    """
    Adds the custom CacheIdLogHandler to the Django logger.
    """

    logger = logging.getLogger('django')  # Or your specific logger name
    if not any(isinstance(handler, CacheIdLogHandler) for handler in logger.handlers):
        logger.addHandler(cache_id_handler)
        logger.setLevel(logging.DEBUG)  # Adjust log level as needed


def get_current_cache_id():
    """
    Retrieves the latest cache_id captured by the custom log handler.
    """
    return cache_id_handler.get_cache_id()



# middleware.py
class ReloadFunctionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Function to reload for every request
        self.my_function()

        response = self.get_response(request)
        return response

    def my_function(self):
        # Your logic here
        cache_id = get_current_cache_id()
        # print(f"//////{cache_id}///////")
