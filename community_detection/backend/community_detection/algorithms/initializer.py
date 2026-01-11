import random
import networkx as nx
from collections import deque
from .core import InstanceCore


class Initializer(InstanceCore):

    def _should_assign_node(self, graph: nx.Graph, node: int, community: str) -> bool | None:
        inside = 0
        outside = 0
        none = 0

        for neighbor in graph.neighbors(node):
            neighbor_comm = graph.nodes[neighbor].get("community")
            if neighbor_comm == community:
                inside += 1
            elif neighbor_comm == None:
                none += 1
            else:
                outside += 1

        result = inside > (outside + none) or (inside + outside == 0) or (inside == 0 and outside != 0)
        return result
    
    def _evaluate_community(self, graph: nx.Graph, node: int, community: str):
        # Candidatos: nodo y vecinos asignables
        candidates = {node}
        for nbr in graph.neighbors(node):
            if graph.nodes[nbr]["community"] is None:
                candidates.add(nbr)

        original_communities = {n: graph.nodes[n].get("community") for n in candidates}

        # Asignar comunidad temporal
        for n in candidates:
            graph.nodes[n]["community"] = community

        # Se evalua parcicalmente
        new_eval = self.evaluator.half_evaluation(graph, community, candidates)

        # Revertir cambios antes de probar otra comunidad
        for n, com in original_communities.items():
            graph.nodes[n]["community"] = com

        return new_eval, candidates
        
    def initialize_greedy(self, graph: nx.Graph, communities: list) -> None:
        for node in graph.nodes:
            graph.nodes[node]["community"] = None

        unassigned_nodes = set(graph.nodes)

        queue = deque()
        first_node = random.choice(list(graph.nodes)) # coger nodo aleatorio
        queue.append(first_node)

        while unassigned_nodes:
            if not queue:
                next_node = unassigned_nodes.pop()
                queue.append(next_node)
                unassigned_nodes.add(next_node)

            node  = queue.popleft()

            # Si el nodo ya fue asignado se salta
            if node not in unassigned_nodes:
                continue

            best_eval = float('-inf')
            best_assignment = None

            # Probar comunidades de vecinos
            neighbor_communities = set()
            for nbr in graph.neighbors(node):
                comm = graph.nodes[nbr].get("community")
                if comm is not None:
                    neighbor_communities.add(comm)

            # comunidades candidatas: comunidades de vecinos + una comunidad nueva si hay
            candidate_communities = list(neighbor_communities)

            # Añadir una comunidad nueva (de las disponibles) si no están en vecinos
            new_communities = [c for c in communities if c not in neighbor_communities]
            if new_communities:
                candidate_communities.append(new_communities[0])

            for community in candidate_communities:

                if not self._should_assign_node(graph, node, community):
                    continue

                new_eval, candidates = self._evaluate_community(graph, node, community)

                if new_eval > best_eval:
                    best_eval = new_eval
                    best_assignment = (community, candidates)


            # Si hay mejor asignación se actualizan las comunidades y se eliminan los nodos ya asignados
            if best_assignment:
                community, candidates = best_assignment

                for n in candidates:
                    graph.nodes[n]["community"] = community
                unassigned_nodes -= candidates

                for n in candidates:
                    for nbr in graph.neighbors(n):
                        if graph.nodes[nbr]["community"] is None and nbr in unassigned_nodes:
                            queue.append(nbr)

            else:

                # Buscar comunidades de los vecinos
                neighbor_communities = [
                    graph.nodes[nbr].get("community") for nbr in graph.neighbors(node)
                    if graph.nodes[nbr].get("community") is not None
                ]
                
                # Asignar la comunidad  más frecuente entre los vecinos
                if neighbor_communities:
                    community = max(set(neighbor_communities), key=neighbor_communities.count)
                else:
                    community = random.choice(communities)
                
                graph.nodes[node]["community"] = community
                unassigned_nodes.discard(node)
                for neighbor in graph.neighbors(node):
                    if graph.nodes[neighbor]["community"] is None and neighbor in unassigned_nodes:
                        queue.append(neighbor)
    
    def initialize_random(self, graph: nx.Graph, communities: list):
        for node in graph.nodes(): 
            graph.nodes[node]["community"] = f"{communities[random.randint(0,len(communities)-1)]}"