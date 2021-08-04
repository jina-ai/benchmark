import logging
import os
import sys
from pathlib import Path

from jina import __version__
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
    import jina


if __name__ == '__main__':
    benchmark()
