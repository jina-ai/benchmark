import pytest
from jina import Document

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5


def test_empty_document_graph_adjacency(json_writer):
    def _input_graphdoc():
        return ((), {"gdoc": GraphDocument()})

    def _doc_get_adjacency(gdoc):
        _ = gdoc.adjacency

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_get_adjacency, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_graph_adjacency/test_empty_document_graph_adjacency",
            iterations=num_docs,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )


def test_document_graph_adjacency(json_writer):
    def _input_graphdoc():
        gdoc = GraphDocument()
        gdoc.add_edges(
            [Document(id=1), Document(id=2)], [Document(id=3), Document(id=1)]
        )

        return ((), {"gdoc": gdoc})

    def _doc_get_adjacency(gdoc):
        _ = gdoc.adjacency

    mean_time, std_time = benchmark_time(
        setup=_input_docs, func=_doc_get_adjacency, n=NUM_REPETITIONS
    )

    json_writer.append(
        dict(
            name="document_graph_adjacency/test_empty_document_graph_adjacency",
            iterations=num_docs,
            mean_time=mean_time,
            std_time=std_time,
            metadata=dict(num_docs=num_docs),
        )
    )
