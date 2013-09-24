from graph.core import edges
import pydot

def dotgraph(dag):
    import pydot
    return pydot.graph_from_edges(sorted(edges(dag)), directed=True)

def dotstr(dag):
    return dotgraph(dag).to_string()

def pdf(dag, filename):
    dotgraph(dag).write_pdf(filename)
