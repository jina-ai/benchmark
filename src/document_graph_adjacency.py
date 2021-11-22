from jina import Document
from jina.types.document.graph import GraphDocument

from .utils.benchmark import benchmark_time
from .pages import Pages


def test_empty_document_graph_adjacency(json_writer):
    def _input_graphdoc():
        return ((), {"gdoc": GraphDocument()})

    def _doc_get_adjacency(gdoc):
        _ = gdoc.adjacency

    result = benchmark_time(setup=_input_graphdoc, func=_doc_get_adjacency)

    json_writer.append(
        page=Pages.DOCUMENT_META,
        result=result,
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

    result = benchmark_time(setup=_input_graphdoc, func=_doc_get_adjacency)

    json_writer.append(
        page=Pages.DOCUMENT_META,
        result=result,
    )
