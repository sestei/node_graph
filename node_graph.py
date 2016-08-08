#!/usr/bin/env python

import pygraphviz as pgv
import pykat

def node_graph(kat, output):
    """
    node_graph(kat, output)

    Generate node visualisation of pykat node network using the
    pygraphviz package. The generated graphics is saved in output, where the
    output format is determined from the file extension. The exact formats
    available depend on how graphviz was built, but generally .pdf and .png
    should work.
    """

    def add_kat_node(G, from_id, node):
        color = 'black' if node.name == 'dump' else 'red'
        G.add_node(node.id, label='', xlabel=node.name, width=0.2,
                   shape='point', fontsize=11, color=color)
        G.add_edge(from_id, node.id)

    G = pgv.AGraph(strict=False)
    G.graph_attr['pencolor'] = 'black'
    G.node_attr['style'] = 'filled'
    G.node_attr['fontname'] = 'helvetica'

    # add components and associated nodes
    for comp in kat.components.itervalues():
        if isinstance(comp, pykat.components.laser):
            attr = {'fillcolor': 'Orange', 'shape': 'box'}
        elif isinstance(comp, pykat.components.space):
            attr = {'fillcolor': 'MediumSlateBlue', 'shape': 'diamond'}
        else:
            attr = {'fillcolor': 'LightSkyBlue', 'shape': 'box'}
        G.add_node(comp.name, **attr)
        for node in comp.nodes:
            add_kat_node(G, comp.name, node)

    # add detectors and associated nodes
    for det in kat.detectors.itervalues():
        # slightly ugly, but unfortunately detectors don't have the .nodes
        # property like components do.
        if len(det._nodes) > 0:
            G.add_node(det.name, fillcolor='YellowGreen', shape='ellipse')
            for node in det._nodes:
                add_kat_node(G, det.name, node)
    
    G.draw(output, prog='neato')


if __name__ == '__main__':
    kat = pykat.finesse.kat()
    kat.loadKatFile('test.kat')
    node_graph(kat, 'test.pdf')
