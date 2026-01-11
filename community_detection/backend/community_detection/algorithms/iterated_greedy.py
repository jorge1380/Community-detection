import random
import networkx as nx
from ..config import REPS_LIMIT
from .core import InstanceCore
from .local_search import LocalSearch


class IteratedGreedy(InstanceCore):


    def iterated_greedy(self, snapshots: dict[(str, str), nx.Graph], communities: list) -> dict:
        first_snapshot = True
        prev_snap = None
        prev_nodes = []
        ls = LocalSearch()
        beta = 0.1 # Número de nodos a quitar comunidades en Iterated Greedy

        for (year, month), graph in snapshots.items():
            
            # Inicio las variables para las condiciones (independiente de cada snapshot)
            first_eval = InstanceCore.evaluations_per_snapshot.get((year, month))
            
            if first_eval is None:
                first_eval = self.evaluator.evaluate_solution(graph, communities)

            reps_wout_improvement = 0

            node_list = list(graph.nodes)

            if prev_nodes:
                for node, community in prev_nodes:
                    if node in graph:
                        graph.nodes[node]['community'] = community
                prev_nodes = []

            while reps_wout_improvement < REPS_LIMIT:
                actual_nodes, backup = self._destroy_and_rebuild(graph, node_list, beta)

                # Aplico la búsqueda local
                snapshots[(year, month)] = self._apply_local_search(graph, communities, ls, first_snapshot, prev_snap, (year, month))


                evaluation = self.evaluator.evaluate_solution(graph,communities)


                if evaluation > first_eval + 1e-4: # Se comprueba que la mejora es mayor que 0.001
                    InstanceCore.evaluations_per_snapshot[(year, month)] = evaluation
                    first_eval = evaluation
                    reps_wout_improvement = 0
                    prev_nodes += actual_nodes
                    
                else:
                    reps_wout_improvement += 1 # Aumento el número de veces que se ha repetido el algoritmo sin mejora
                    # Revierto el cambio de comunidades en los nodos
                    for node, comm in backup.items():
                        graph.nodes[node]['community'] = comm
                    

            print("Cambiando de snapshot")
            first_snapshot = False
            prev_snap = graph.copy()
        return snapshots

    def _destroy_and_rebuild(self, graph, node_list, beta):
        sampled = random.sample(node_list, int(len(node_list) * beta))
        backup = {node: graph.nodes[node]['community'] for node in sampled}
        updated = []

        for node in sampled:
            graph.nodes[node]['community'] = None
            rep = {}

            for neighbor in graph.neighbors(node):
                comm = graph.nodes[neighbor].get('community')
                if comm is not None:
                    rep[comm] = rep.get(comm, 0) + 1

            if rep:
                best_comm = max(rep, key=rep.get) 
            else: 
                best_comm = backup[node]

            graph.nodes[node]['community'] = best_comm
            updated.append((node, best_comm))

        return updated, backup
    
    def _apply_local_search(self, graph, communities, ls: LocalSearch, first_snapshot, prev_snap, snap_key):
        if first_snapshot:
            return ls.local_search_front(graph, communities, snap_key)
        else:
            return ls.local_search_added(graph, communities, prev_snap, snap_key)