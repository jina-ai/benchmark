from enum import Enum


class PAGES(Enum):
    DA_APPEND = 'document_array_append'
    DA_CLEAR = 'document_array_clear'
    DA_CONSTRUCT = 'document_array_construct'
    DA_EXTEND = 'document_array_extend'
    DA_GET_ATTRIBUTES = 'document_array_get_attributes'
    DA_INSERT = 'document_array_insert'
    DA_MATCH = 'document_array_match'
    DA_PERSISTENCE = 'document_array_persistence'
    DA_SHUFFLE = 'document_array_shuffle'
    DA_SORT = 'document_array_sort'
    DA_TRAVERSE = 'document_array_traverse'
    DOCUMENT_CONSTRUCT = 'document_construct'
    DOCUMENT_GET_ATTRIBUTES = 'document_get_attributes'
    DOCUMENT_GRAPH_CONSTRUCTION = 'document_graph_construction'
    DOCUMENT_PROPERTY_GETTER = 'document_property_getter'
    DOCUMENT_SET_ATTRIBUTES = 'document_set_attributes'
    EXECUTOR = 'executor'
    FLOW = 'flow'
