import networkx as nx

class Evaluator:
    """Evalúa soluciones de comunidades usando la modularidad de Newman."""

    def evaluate_solution(self, graph: nx.Graph, communities: list) -> float:
        total_edges = graph.number_of_edges()
        if total_edges == 0:
            return 0

        modularity = 0.0
        for community in communities:
            edges_in = abs(self._community_edges_in(graph, community))
            edges_out = abs(self._community_edges_out(graph, community))
            modularity += (edges_in / total_edges) - (((2 * edges_in + edges_out) / (2 * total_edges)) ** 2)

        return modularity

    def _community_edges_in(self, graph: nx.Graph, community: str) -> int:
        edges_in = 0
        for u, v in graph.edges():
            if graph.nodes[u]["community"] == community and graph.nodes[v]["community"] == community:
                edges_in += 1
        return edges_in

    def _community_edges_out(self, graph: nx.Graph, community: str) -> int:
        edges_out = 0
        for u, v in graph.edges():
            if (graph.nodes[u]["community"] == community and graph.nodes[v]["community"] != community) or \
               (graph.nodes[v]["community"] == community and graph.nodes[u]["community"] != community):
                edges_out += 1
        return edges_out
    
    def half_evaluation(self, graph, community, nodes: set):
        inside = 0
        outside = 0
        for node in nodes:
            for neighbor in graph.neighbors(node):
                neighbor_comm = graph.nodes[neighbor].get("community")
                if neighbor_comm == community:
                    inside += 1
                else:
                    outside += 1
        return inside