import logging
import os
import sys
from pathlib import Path

from jina import Flow, __version__
from jina.helloworld.fashion.app import set_hw_parser
from jina.helloworld.fashion.helper import (
    download_data,
    index_generator,
    query_generator,
)
from memory_profiler import LogFile, profile

try:
    from jina.helloworld.fashion.executors import MyEncoder, MyEvaluator, MyIndexer
except:
    from jina.helloworld.fashion.my_executors import MyEncoder, MyEvaluator, MyIndexer

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


def prepare():
    args = set_hw_parser().parse_args()
    args.hello = 'fashion'
    args.workdir = os.path.join('tmp', args.workdir)

    targets = {
        'index-labels': {
            'url': args.index_labels_url,
            'filename': os.path.join(args.workdir, 'index-labels'),
        },
        'query-labels': {
            'url': args.query_labels_url,
            'filename': os.path.join(args.workdir, 'query-labels'),
        },
        'index': {
            'url': args.index_data_url,
            'filename': os.path.join(args.workdir, 'index-original'),
        },
        'query': {
            'url': args.query_data_url,
            'filename': os.path.join(args.workdir, 'query-original'),
        },
    }

    # download the data
    Path(args.workdir).mkdir(parents=True, exist_ok=True)
    download_data(targets, args.download_proxy)

    # reduce the network load by using `fp16`, or even `uint8`
    os.environ['JINA_ARRAY_QUANT'] = 'fp16'

    return args, targets


@profile
def benchmark(args, targets):
    f = (
        Flow()
        .add(uses=MyEncoder, parallel=2)
        .add(uses=MyIndexer, workspace=args.workdir)
        .add(uses=MyEvaluator)
    )

    # run it!
    with f:
        f.index(
            index_generator(num_docs=targets['index']['data'].shape[0], target=targets),
            request_size=args.request_size,
            show_progress=True,
        )

        f.post(
            '/eval',
            query_generator(
                num_docs=args.num_query, target=targets, with_groundtruth=True
            ),
            shuffle=True,
            request_size=args.request_size,
            parameters={'top_k': args.top_k},
            show_progress=True,
        )


if __name__ == '__main__':
    args, targets = prepare()
    benchmark(args, targets)