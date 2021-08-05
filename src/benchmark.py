from jina import Document, DocumentArray
from timecontext import TimeContext


def benchmark(cls, function, *args, **kwargs):
    def wrapper(*args, **kwargs):
        with TimeContext() as timer:
            func = function(*args, **kwargs)

        cls.profile[f'{function.__name__}']['time'] += timer.duration
        cls.profile[f'{function.__name__}']['calls'] += 1
        return func

    return wrapper


class BenchmarkedDocument(Document):
    import inspect
    setattr(Document, 'profile', {})
    for _, f in inspect.getmembers(Document, predicate=inspect.isfunction):
        Document.profile[f'{f.__name__}'] = {'time': 0.0, 'calls': 0}
        setattr(Document, f.__name__, benchmark(Document, f))


class BenchmarkedDocumentArray(DocumentArray):
    import inspect
    setattr(DocumentArray, 'profile', {})
    for _, f in inspect.getmembers(DocumentArray, predicate=inspect.isfunction):
        DocumentArray.profile[f'{f.__name__}'] = {'time': 0.0, 'calls': 0}
        setattr(DocumentArray, f.__name__, benchmark(DocumentArray, f))

