import logging
import os
import sys
import uuid
from pathlib import Path

from jina import Document, DocumentArray, __version__
from memory_profiler import LogFile, profile

from timecontext import TimeContext

NUM_DOCS = 100000
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


def _get_document_array():
    da = DocumentArray(
        (Document(text=f'This is the document number: {i}') for i in range(NUM_DOCS))
    )

    return da


@profile
def benchmark(fp, document_array, binfile):
    with TimeContext() as timer:
        document_array.save(binfile, file_format='binary')
    fp.write(
        'Saving DocumentArray in a binary file took {}, {} per doc\n'.format(
            timer.duration, timer.duration / NUM_DOCS
        )
    )

    with TimeContext() as timer:
        DocumentArray.load(binfile, file_format='binary')
    fp.write(
        'Loading DocumentArray from a binary file took {}, {} per doc\n'.format(
            timer.duration, timer.duration / NUM_DOCS
        )
    )


if __name__ == '__main__':
    Path('tmp').mkdir(parents=True, exist_ok=True)
    binfile = 'tmp/{}.bin'.format(str(uuid.uuid4()))
    da = _get_document_array()

    fp = open(
        os.path.join(
            output_dir,
            '{}_time_context.txt'.format(os.path.basename(__file__)).replace('.py', ''),
        ),
        'w+',
    )
    with fp:
        benchmark(fp, da, binfile)
