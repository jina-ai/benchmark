import logging
import os
import sys
from pathlib import Path

from jina import Document, Flow, __version__
from memory_profiler import LogFile, profile

os.environ['JINA_LOG_LEVEL'] = 'CRITICAL'
output_dir = 'docs/static/artifacts/{}'.format(__version__)
Path(output_dir).mkdir(parents=True, exist_ok=True)
log_file = os.path.join(
    output_dir,
    '{}_memory_profile.txt'.format(os.path.basename(__file__)).replace('.py', ''),
)

# create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler(log_file, 'w+')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)
sys.stdout = LogFile(__name__)


def __doc_generator():
    # Document generator
    for i in range(1000):
        yield Document(
            text=f'This is the document number: {i}',
        )


@profile
def benchmark():
    fs = [
        Flow().add(),
        Flow().add().add(),
        Flow().add().add().add(),
        Flow().add().add().add(needs='gateway'),
    ]

    for f in fs:
        with f:
            f.post(on='/', inputs=__doc_generator, request_size=10)


if __name__ == '__main__':
    benchmark()
