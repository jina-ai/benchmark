import random

import numpy as np
import pytest
from jina import Document
from jina.types.document.graph import GraphDocument

from .utils.benchmark import benchmark_time

NUM_REPETITIONS = 5
NUM_DOCS = 1000


@pytest.mark.parametrize('n_edges', [10_000, 20_000])
@pytest.mark.parametrize('n_nodes', [1000, 10_000])
def test_graph_add_edges_assuming_no_nodes_present(n_nodes, n_edges, json_writer):

    docs = [Document(text=f'Document{i}') for i in range(n_nodes)]
    sources = [random.choice(docs) for i in range(n_edges)]
    targets = [random.choice(docs) for i in range(n_edges)]
    edge_features = [
        {'text': f'I connect Doc{i} and Doc{j}'} for i, j in zip(sources, targets)
    ]

    def _build_graph_doc():
        graph = GraphDocument()
        graph.add_edges(sources, targets, edge_features=edge_features)
        return graph

    mean_time, std_time = benchmark_time(func=_build_graph_doc, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_graph_construction/test_graph_add_edges_assuming_no_nodes_present',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(n_nodes=n_nodes, n_edges=n_edges),
        )
    )


@pytest.mark.parametrize('n_edges', [10_000, 20_000])
@pytest.mark.parametrize('n_nodes', [1000, 10_000])
def test_graph_add_edges_assuming_all_nodes_present(n_nodes, n_edges, json_writer):

    docs = [Document(text=f'Document{i}') for i in range(n_nodes)]
    sources = [random.choice(docs) for i in range(n_edges)]
    targets = [random.choice(docs) for i in range(n_edges)]
    edge_features = [
        {'text': f'I connect Doc{i} and Doc{j}'} for i, j in zip(sources, targets)
    ]
    graph = GraphDocument()
    graph.add_nodes(docs)

    def _build_graph_doc():
        graph.add_edges(sources, targets, edge_features=edge_features)
        return graph

    mean_time, std_time = benchmark_time(func=_build_graph_doc, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_graph_construction/test_graph_add_edges_assuming_all_nodes_present',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(n_nodes=n_nodes, n_edges=n_edges),
        )
    )


@pytest.mark.parametrize('n_edges', [10_000, 20_000])
@pytest.mark.parametrize('n_nodes', [1000, 10_000])
def test_graph_node_additions(n_nodes, n_edges, json_writer):

    docs = [Document(text=f'Document{i}') for i in range(n_nodes)]

    def _build_graph_doc():
        graph = GraphDocument()
        graph.add_nodes(docs)
        return graph

    mean_time, std_time = benchmark_time(func=_build_graph_doc, n=NUM_REPETITIONS)

    json_writer.append(
        dict(
            name='document_graph_construction/test_graph_node_additions',
            iterations=NUM_DOCS,
            mean_time=mean_time,
            std_time=std_time,
            unit='ms',
            metadata=dict(n_nodes=n_nodes, n_edges=n_edges),
        )
    )
