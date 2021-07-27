from jina import Document, Flow


def __doc_generator():
    # Document generator
    for i in range(1000):
        yield Document(
            text=f'This is the document number: {i}',
        )


fs = [
    Flow().add(),
    Flow().add().add(),
    Flow().add().add().add(),
    Flow().add().add().add(needs='gateway'),
]

for f in fs:
    with f:
        f.post(on='/', inputs=__doc_generator, request_size=10)