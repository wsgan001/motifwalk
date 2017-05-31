import pickle
from itertools import combinations
import numpy as np
import networkx as nx
from motifwalk.utils.Graph import GraphContainer
from motifwalk.motifs import all_u3, all_3, all_u4, all_4
from graph_tool.all import Graph, motifs

def count_motif(g, motif_object, rm=True):
    """Count the number of given motif and return the mapping list
    to the vertices belongs to the motif. Note that `motifs` function
    return a triplet, lossing pointer to the first element in This
    triplet will make all PropertyMap orphan.

    Parameters:
    graph_container - GraphContainer - Graph storage object
    motif_object - Motif - Motif container
    rm - boolean - Return Maps

    Returns:
    motifs - list - contains gt.Graph objects
    counts - list - corresponding counts for motifs
    vertex_map - list - contains lists of gt.PropertyMap
    """
    m = motif_object.gt_motif
    # graph_tool.clustering.motifs
    rm, c, v_map = motifs(g, m.num_vertices(), motif_list=[m], return_maps=rm)
    return rm, c, v_map

def construct_motif_graph(graph_container, motif, vertex_maps=None):
    """Construct and return a undirected gt graph containing
    motif relationship.

    Parameters:
    graph_container - GraphContainer - Store the original network
    motif - Motif - Motif in study

    Returns:
    m_graph - gt.Graph - Undirected graph for motif cooccurence
    """
    if motif.anchors is None:
        print("Warning: Turning motif groups into cliques.")
    graph = graph_container.get_gt_graph()
    # graph_tool.Graph
    m_graph = Graph(directed=False)
    if vertex_maps is None:
        m, c, vertex_maps = count_motif(graph, motif)
    for prop_list in vertex_maps:
        for prop in prop_list:
            edges = [i for i in motif.anchored_edges(graph, prop.get_array())]
            m_graph.add_edge_list(edges)
    return m_graph
