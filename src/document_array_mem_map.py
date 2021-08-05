import logging
import os
import sys
import uuid
from pathlib import Path

from jina import Document, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap
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


@profile
def benchmark():
    dlist = []
    dam_size = 1000000
    mem_map_path = os.path.join(os.getcwd(), 'tmp/{}'.format(str(uuid.uuid4())))
    Path(mem_map_path).mkdir(parents=True, exist_ok=True)
    dam = DocumentArrayMemmap(mem_map_path)

    for i in range(dam_size):
        dlist.append(
            Document(
                text=f'This is the document number: {i}',
            )
        )

    dam.extend(dlist)


if __name__ == '__main__':
    benchmark()