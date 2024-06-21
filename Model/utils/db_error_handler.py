from functools import wraps

# this dicorator will handle:
# a. error handling
# b. connecting to db 
# c. closing the connection to db
def handle_database_errors(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            self._before()
            result = func(self, *args, **kwargs)
            return result

        except Exception as e:
            # TODO log into a file instead of printing
            print(f"an unexpected error occurred in {func.__name__}: {e}")
            raise

        finally:
            self._after()

    return wrapper
