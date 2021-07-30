import os
from jina import Document
from jina.types.arrays.memmap import DocumentArrayMemmap
from memory_profiler import profile as memory_profiler


output_dir = os.path.join(os.getcwd().replace('/benchmarks', ''), 'outputs')
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
    dam = DocumentArrayMemmap(os.path.join(os.getcwd(), 'MyMemMap'))

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