import requests
from requests.adapters import HTTPAdapter
from requests.adapters import HTTPAdapter, Retry



class ReadOnlyDict(dict):
    def __setitem__(self, *args, **kwargs):
        raise ValueError("Readonly dictionary.")


class CyclicList(list):
    def __iter__(self):
        self.current = 0
        return self

    def __next__(self):
        if len(self) == 0:
            raise StopIteration
        value = self[self.current]
        self.current += 1

        if self.current == len(self):
            self.current = 0

        return value


def wrap_exception(exception):
    def wraps(func):
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ConnectionError:
                raise exception

        return inner

    return wraps


class ServiceUnavailable(Exception):
    pass


class HttpService:
    exception_class = ServiceUnavailable

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

    @property
    def url(self):
        return f"http://{self.host}:{self.port}/dfs"
    
    def get_session(self):
        session = requests.Session()
        session.mount(self.url, HTTPAdapter(max_retries=self.retries))
        return session

    @wrap_exception(ServiceUnavailable)
    def get(self, path, *args, **kwargs):

        return self.get_session().get(self.url + path, *args, **kwargs)

    @wrap_exception(ServiceUnavailable)
    def post(self, path, *args, **kwargs):
        return self.get_session().post(self.url + path, *args, **kwargs)

    @wrap_exception(ServiceUnavailable)
    def put(self, path, *args, **kwargs):
        return self.get_session().put(self.url + path, *args, **kwargs)

    @wrap_exception(ServiceUnavailable)
    def delete(self, path, *args, **kwargs):
        return self.get_session().delete(self.url + path, *args, **kwargs)

    @wrap_exception(ServiceUnavailable)
    def patch(self, path, *args, **kwargs):
        return self.get_session().patch(self.url + path, *args, **kwargs)
