
import time
from community_detection.algorithm_comparator import AlgorithmComparator
from community_detection.run import run_all
import networkx as nx

class AlgorithmService:

    def __init__(self):
        self.comparator = AlgorithmComparator()

        # Última ejecución, útil para frontend
        self.snapshots_college = {}
        self.snapshots_email = {}
        self.communities = []
        self.evaluations_college = {}
        self.evaluations_email = {}

    def run(self, local_search: bool, iterated_greedy: bool, build_greedy: bool):

        if not local_search and not iterated_greedy:
            alg_name = "Ninguno"
        elif local_search and not iterated_greedy:
            alg_name = "Local Search"
        else:
            alg_name = "Iterated Greedy"

        # Ejecutar algoritmo
        start = time.time()
        self.snapshots_college, self.snapshots_email, self.communities, self.evaluations_college, self.evaluations_email, time_college, time_email = run_all(local_search, iterated_greedy, build_greedy)
        elapsed = time.time() - start

        # Registrar resultados
        self.comparator.add_execution(alg_name, "CollegeMsg", self.evaluations_college, time_college, build_greedy)
        self.comparator.add_execution(alg_name, "email-Eu-core", self.evaluations_email, time_email, build_greedy)




    def get_evaluations(self):
        return self.evaluations_college, self.evaluations_email
    
    def get_communities(self) -> list:
        return self.communities
    
    def graph_to_json(self, graph: nx.Graph) -> dict:


        return {
            "nodes": [
                {
                    "id": str(n),
                    "community": graph.nodes[n].get("community", 0),
                }
                for n in graph.nodes
            ],
            "links": [
                {"source": str(u), "target": str(v)}
                for u, v in graph.edges
            ]
        }


    def get_graphs(self) -> dict:
        data = {
            "CollegeMsg": {},
            "email-Eu-core": {}
        }

        for (year, month), graph in self.snapshots_college.items():
            snapshot_id = f"{year}-{month}"
            data["CollegeMsg"][snapshot_id] = self.graph_to_json(graph)

        for (year, month), graph in self.snapshots_email.items():
            snapshot_id = f"{year}-{month}"
            data["email-Eu-core"][snapshot_id] = self.graph_to_json(graph)

        return data
    
    def get_comparison_summary(self) -> dict:
        return self.comparator.summarize()

    def get_raw_comparison_data(self) -> dict:
        return self.comparator.get_raw_data()