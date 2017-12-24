from copy import deepcopy

all = [
        'GraphCyclesError',
        'DirectedGraph',
        ]

class GraphCyclesError(Exception):
    def __init__(self, graph):
        self.graph = graph
    def __str__(self):
        return 'Cycles detected: {}'.format(self.graph)

class DirectedGraph(object):
    def __init__(self, graph=None, node_attrs=None, edge_attrs=None):
        self.edges = {}
        self.graph = {}
        self.nodes = {}
        self.rev_graph = {}

        if graph:
            for a, edges in graph.items():
                self.add_node(a)
                for b in edges:
                    self.add_edge((a, b))
        if node_attrs:
            for node, attrs in node_attrs.items():
                self.add_node(node)
                self.nodes[node] = deepcopy(attrs)
        if edge_attrs:
            for edge, attrs in edge_attrs.items():
                self.add_edge(edge)
                self.edges[edge] = deepcopy(attrs)

    def __repr__(self):
        return '{}(graph={}, node_attrs={}, edge_attrs={})'.format(
                self.__class__.__name__,
                self.simple_graph(),
                self.nodes,
                self.edges
                )

    def __str__(self):
        return '<{} instance at {}, nodes: {}, edges: {}>'.format(
                self.__class__.__name__,
                hex(id(self)),
                len(self.graph),
                sum(map(len, self.graph.values())))

    def _topological_sort(self):
        results = []
        while self.graph:
            free = self.no_outgoing_edges()
            if not free:
                raise GraphCyclesError(self.graph)
            for node in free:
                self.remove_node(node)
                results.append(node)
        return results

    def add_edge(self, edge):
        a, b = edge
        if a not in self.graph or b not in self.graph[a]:
            self.add_node(a)
            self.add_node(b)
            self.graph[a].add(b)
            self.rev_graph[b].add(a)
            self.edges[edge] = {}

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = set()
            self.rev_graph[node] = set()
            self.nodes[node] = {}

    def no_outgoing_edges(self):
        return sorted(node for node, edges in self.graph.items() if not edges)

    def remove_edge(self, edge):
        a, b = edge
        self.graph[a].remove(b)
        self.rev_graph[b].remove(a)
        del self.edges[edge]

    def remove_node(self, node):
        for other in self.graph[node]:
            del self.edges[(node, other)]
        del self.graph[node]
        for other in self.rev_graph[node]:
            self.graph[other].remove(node)
            del self.edges[(other, node)]
        del self.rev_graph[node]
        del self.nodes[node]

    def inverse(self):
        rev_edges = dict(((other, node), self.edges[(node, other)]) for node, others in self.graph.items() for other in others)
        return self.__class__(self.rev_graph, self.nodes, rev_edges)

    def simple_graph(self):
        return dict((node, sorted(others)) for node, others in self.graph.items())

    def topological_sort(self):
        return self.__class__(self.graph)._topological_sort()

    def to_graphviz(self):
        pass

    def to_graphviz_annotated(self):
        # any node or edge attributes prefixed with graphviz_ are converted
        # to graphviz attributes
        pass
