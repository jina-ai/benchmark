# import random
#
# import pytest
# from jina import Document
# from jina.types.document.graph import GraphDocument
#
# from .pages import Pages
# from .utils.benchmark import benchmark_time
#
#
# @pytest.mark.parametrize('n_edges', [200, 2_000])
# @pytest.mark.parametrize('n_nodes', [100, 1_000])
# def test_graph_add_edges_assuming_no_nodes_present(n_nodes, n_edges, json_writer):
#     def _setup():
#         docs = [Document(text=f'Document{i}') for i in range(n_nodes)]
#         sources = [random.choice(docs) for i in range(n_edges)]
#         targets = [random.choice(docs) for i in range(n_edges)]
#         edge_features = [
#             {'text': f'I connect Doc{i} and Doc{j}'} for i, j in zip(sources, targets)
#         ]
#         return (), dict(sources=sources, targets=targets, edge_features=edge_features)
#
#     def _build_graph_doc(sources, targets, edge_features):
#         graph = GraphDocument()
#         graph.add_edges(sources, targets, edge_features=edge_features)
#
#     result = benchmark_time(
#         setup=_setup,
#         func=_build_graph_doc,
#     )
#
#     json_writer.append(
#         page=Pages.DOCUMENT_GRAPH,
#         result=result,
#         metadata=dict(n_nodes=n_nodes, n_edges=n_edges),
#     )
#
#
# @pytest.mark.parametrize('n_edges', [200, 2_000])
# @pytest.mark.parametrize('n_nodes', [100, 1_000])
# def test_graph_add_edges_assuming_all_nodes_present(n_nodes, n_edges, json_writer):
#     def _setup():
#         docs = [Document(text=f'Document{i}') for i in range(n_nodes)]
#         sources = [random.choice(docs) for i in range(n_edges)]
#         targets = [random.choice(docs) for i in range(n_edges)]
#         edge_features = [
#             {'text': f'I connect Doc{i} and Doc{j}'} for i, j in zip(sources, targets)
#         ]
#         graph = GraphDocument()
#         graph.add_nodes(docs)
#         return (), dict(
#             graph=graph, sources=sources, targets=targets, edge_features=edge_features
#         )
#
#     def _build_graph_doc(graph, sources, targets, edge_features):
#         graph.add_edges(sources, targets, edge_features=edge_features)
#
#     result = benchmark_time(
#         setup=_setup,
#         func=_build_graph_doc,
#     )
#
#     json_writer.append(
#         page=Pages.DOCUMENT_GRAPH,
#         result=result,
#         metadata=dict(n_nodes=n_nodes, n_edges=n_edges),
#     )
#
#
# @pytest.mark.parametrize('n_edges', [200, 2_000])
# @pytest.mark.parametrize('n_nodes', [100, 1_000])
# def test_graph_add_single_edge_assuming_all_nodes_present(
#     n_nodes, n_edges, json_writer
# ):
#     def _setup():
#         docs = [Document(text=f'Document{i}') for i in range(n_nodes)]
#         sources = [random.choice(docs) for i in range(n_edges)]
#         targets = [random.choice(docs) for i in range(n_edges)]
#         graph = GraphDocument()
#         graph.add_nodes(docs)
#         return (), dict(graph=graph, sources=sources, targets=targets)
#
#     def _build_graph_doc(graph, sources, targets):
#         for source, target in zip(sources, targets):
#             graph.add_single_edge(source, target)
#         return graph
#
#     result = benchmark_time(setup=_setup, func=_build_graph_doc)
#
#     json_writer.append(
#         page=Pages.DOCUMENT_GRAPH,
#         result=result,
#         metadata=dict(n_nodes=n_nodes, n_edges=n_edges),
#     )
#
#
# @pytest.mark.parametrize('n_edges', [200, 2_000])
# @pytest.mark.parametrize('n_nodes', [100, 1_000])
# def test_graph_add_single_edge_assuming_no_nodes_present(n_nodes, n_edges, json_writer):
#     def _setup():
#         docs = [Document(text=f'Document{i}') for i in range(n_nodes)]
#         sources = [random.choice(docs) for i in range(n_edges)]
#         targets = [random.choice(docs) for i in range(n_edges)]
#         return (), dict(sources=sources, targets=targets)
#
#     def _build_graph_doc(sources, targets):
#         graph = GraphDocument()
#         for source, target in zip(sources, targets):
#             graph.add_single_edge(source, target)
#         return graph
#
#     result = benchmark_time(setup=_setup, func=_build_graph_doc)
#
#     json_writer.append(
#         page=Pages.DOCUMENT_GRAPH,
#         result=result,
#         metadata=dict(n_nodes=n_nodes, n_edges=n_edges),
#     )
#
#
# @pytest.mark.parametrize('n_nodes', [100, 1_000])
# def test_graph_add_single_node(n_nodes, json_writer):
#     def _setup():
#         docs = [Document(text=f'Document{i}') for i in range(n_nodes)]
#         graph = GraphDocument()
#         return (), dict(graph=graph, docs=docs)
#
#     def _build_graph_doc(graph, docs):
#         for doc in docs:
#             graph.add_single_node(doc)
#
#     result = benchmark_time(
#         setup=_setup,
#         func=_build_graph_doc,
#     )
#
#     json_writer.append(
#         page=Pages.DOCUMENT_GRAPH,
#         result=result,
#         metadata=dict(n_nodes=n_nodes),
#     )
#
#
# @pytest.mark.parametrize('n_nodes', [100, 1_000])
# def test_graph_add_nodes(n_nodes, json_writer):
#     def _setup():
#         docs = [Document(text=f'Document{i}') for i in range(n_nodes)]
#         graph = GraphDocument()
#         graph.add_nodes(docs)
#         return (), dict(graph=graph, docs=docs)
#
#     def _build_graph_doc(graph, docs):
#         graph.add_nodes(docs)
#
#     result = benchmark_time(
#         setup=_setup,
#         func=_build_graph_doc,
#     )
#
#     json_writer.append(
#         page=Pages.DOCUMENT_GRAPH,
#         result=result,
#         metadata=dict(n_nodes=n_nodes),
#     )
