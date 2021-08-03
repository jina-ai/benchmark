import os
import uuid
from pathlib import Path

from jina import Document, __version__
from jina.types.arrays.memmap import DocumentArrayMemmap
from memory_profiler import profile as memory_profiler

output_dir = os.path.join(
    os.getcwd().replace('/src', ''), 'docs/static/artifacts/{}'.format(__version__)
)
Path(output_dir).mkdir(parents=True, exist_ok=True)
fp = open(
    os.path.join(
        output_dir,
        '{}_memory_profile.txt'.format(os.path.basename(__file__)).replace('.py', ''),
    ),
    'w+',
)


@memory_profiler(stream=fp)
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
    fp.close()
