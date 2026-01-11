
import networkx as nx
from collections import deque
from .core import InstanceCore


class LocalSearch(InstanceCore):
    
    def local_search(self, snapshots: dict, communities: list) -> nx.Graph:
        first_snap = True
        prev_snap = None
        InstanceCore.evaluations_per_snapshot = {}

        for (year, month), graph in snapshots.items():
            if first_snap:
                snapshots[(year, month)] = self.local_search_front(graph, communities, (year, month))
                first_snap = False
            else:
                snapshots[(year, month)] = self.local_search_added(graph, communities, prev_snap, (year, month)) # Cambiar los nodos que se añaden o los adyacentes de los que se eliminan

            prev_snap = snapshots[(year, month)].copy()
        
        return snapshots

    def _assign_nodes(self, queue: deque, neighbor_comms: map, communities: list, graph: nx.Graph, snap_key) -> nx.Graph:

        if snap_key in InstanceCore.evaluations_per_snapshot:
            current_eval = InstanceCore.evaluations_per_snapshot[snap_key]
        else:
            current_eval = self.evaluator.evaluate_solution(graph, communities)
            InstanceCore.evaluations_per_snapshot[snap_key] = current_eval

        while queue:
            node, community_index = queue.pop()

            # Obtengo la lista de comunidades de los vecinos del nodo
            list_neighbor_comms = neighbor_comms[node]

            # Se comprueba que el índice de las comunidades este dentro del rango
            if community_index >= len(list_neighbor_comms):
                continue

            # Se obtiene la comunidad a evaluar
            community_test = list_neighbor_comms[community_index]
            
            original_community = graph.nodes[node]['community']
            graph.nodes[node]['community'] = community_test

            new_eval = self.evaluator.evaluate_solution(graph, communities)

            # Si la evaluación mejora
            if new_eval > current_eval:
                InstanceCore.evaluations_per_snapshot[snap_key] = new_eval
                current_eval = new_eval      
            else:
                # Se restablece la comunidad a la de antes del cambio
                graph.nodes[node]['community'] = original_community

                # Se vuelve a añadir el nodo a la cola
                queue.append((node, community_index + 1))

        return graph

    def local_search_front(self, graph: nx.Graph, communities: list, snap_key) -> nx.Graph:

        # Creo la cola de nodos frontera
        front = deque()

        neighbor_comms = {}
        # Busco nodos frontera (vecinos en 2 o más comunidades distintas)
        for node in graph.nodes():
            # Obtengo las comunidades de los vecinos
            neighbor_communities = set()
            for neighbour in graph.neighbors(node):
                if graph.nodes[neighbour]['community'] != graph.nodes[node]['community']:
                    neighbor_communities.add(graph.nodes[neighbour]['community'])

            # Si hay más de 1 comunidad diferente entre los vecinos es un nodo frontera
            if len(neighbor_communities) >= 2:
                front.append((node, 0))
                neighbor_comms[node] = list(neighbor_communities)
        
        sorted_frontier = deque(sorted(front, key=lambda x: len(neighbor_comms[x[0]]), reverse=True)) # Se ordenan de más comunidades vecinas a menos
        
        return self._assign_nodes(sorted_frontier, neighbor_comms, communities, graph, snap_key)
    
    def local_search_added(self, graph: nx.Graph, communities: list, previous_graph: nx.Graph, snap_key) -> nx.Graph:
        
        previous_snap = set(previous_graph.nodes())
        actual_snap = set(graph.nodes())
        added_nodes = actual_snap - previous_snap # Obtengo el conjunto con los nodos añadidos
        deleted_nodes = previous_snap - actual_snap # Obtengo el conjunto con los nodos eliminados
    
        # Comunidades de los vecinos de los nodos añadidos
        neighbor_comms = {}
        for node in added_nodes:
            neighbour_communities = set()
            for neighbor in graph.neighbors(node):
                neighbour_communities.add(graph.nodes[neighbor]['community'])
            neighbor_comms[node] = list(neighbour_communities)
        
        # Obtener vecinos de los nodos añadidos y sus comunidades
        deleted_neighbours = set()
        for node in deleted_nodes:
            for neighbor in previous_graph.neighbors(node):
                # Si el vecino del nodo eliminado está en la snapshot actual lo añado al conjunto de candidatos
                if neighbor in graph.nodes:
                    deleted_neighbours.add(neighbor)
            
        for node in deleted_neighbours:
            neighbour_communities = set()
            for neighbor in graph.neighbors(node):
                neighbour_communities.add(graph.nodes[neighbor]['community'])
            neighbor_comms[node] = list(neighbour_communities)

        # Añado los nodos a las colas junto al índice de la comunidad a probar
        deleted_queue = deque((node, 0) for node in deleted_neighbours)
        added_queue = deque((node, 0) for node in added_nodes)

        # Se combinan las colas con los nodos eliminados y los añadidos
        combined_queue = deque()
        combined_queue.extend(added_queue)
        combined_queue.extend(deleted_queue) 

        return self._assign_nodes(combined_queue, neighbor_comms, communities, graph, snap_key)
    