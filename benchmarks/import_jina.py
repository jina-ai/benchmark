import os

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
    import jina


if __name__ == '__main__':
    benchmark()
    fp.close()
