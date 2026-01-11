from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import os
import time
import networkx as nx
from datetime import datetime, timezone
import logging

from .config import config_log, NUMBER_OF_COMMUNITIES, DATA_DIR
from .algorithms import Instance
from .evaluator import Evaluator


def load_snapshots_collegemsg(graph):
    snapshots = {}
    nodes_months = []
    months = set()

    for u, v, data in graph.edges(data=True):
        if "timestamp" in data:
            timestamp = data["timestamp"]
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
            year_month = (dt.year, dt.month)
            graph.nodes[u]["year_month"] = year_month
            graph.nodes[v]["year_month"] = year_month
            months.add(year_month)
            nodes_months.append((u, year_month))
            nodes_months.append((v, year_month))

    months = sorted(months)

    for year_month in months:
        nodes = [node for node, y in nodes_months if y == year_month]
        snapshot = graph.subgraph(nodes).copy()
        snapshots[year_month] = snapshot

    return snapshots


def load_snapshots_email_core(graph):
    nodes_months = []
    months = set()

    for u, v, data in graph.edges(data=True):
        ts = data.get("timestamp")
        if ts is not None:
            dt = datetime.fromtimestamp(ts, tz=timezone.utc)
            year_month = (dt.year, dt.month)
            graph.nodes[u]["year_month"] = year_month
            graph.nodes[v]["year_month"] = year_month
            months.add(year_month)
            nodes_months.append((u, year_month))
            nodes_months.append((v, year_month))

    months = sorted(months)

    quarter_nodes = {}
    for node, (year, month) in nodes_months:
        quarter = (month - 1) // 3 + 1
        key = (year, quarter)
        quarter_nodes.setdefault(key, []).append(node)

    snapshots = {}
    for (year, quarter), nodes in quarter_nodes.items():
        snapshot = graph.subgraph(nodes).copy()
        snapshots[(year, quarter)] = snapshot

    return snapshots


def process_collegemsg(communities, local_search, iterated_greedy, build_greedy):  
    graph1_path = os.path.join(DATA_DIR, "CollegeMsg.txt")
    instance = Instance()

    print("Cargando CollegeMsg...")
    graph1 = nx.read_edgelist(graph1_path, create_using=nx.Graph(), nodetype=int, data=[("timestamp", int)])

    if build_greedy:
        print("Inicializando CollegeMsg vorazmente...")
        instance.initialize_greedy(graph1, communities)
    else:
        instance.initialize_random(graph1, communities)
    
    print("Generando snapshots...")
    snapshots = load_snapshots_collegemsg(graph1)


    if local_search or iterated_greedy:
        print("Aplicando Local Search...")
        snapshots = instance.local_search(snapshots, communities)
    if iterated_greedy:
        print("Aplicando Iterated Greedy...")
        snapshots = instance.iterated_greedy(snapshots, communities)
    return snapshots


def process_email_core(communities, local_search, iterated_greedy, build_greedy):
    graph2_path = os.path.join(DATA_DIR, "email-Eu-core-temporal.txt")
    instance = Instance()

    print("Cargando email-Eu-core...")
    graph2 = nx.read_edgelist(graph2_path, create_using=nx.Graph(), nodetype=int, data=[("timestamp", int)])

    if build_greedy:
        print("Inicializando email-Eu-core vorazmente...")
        instance.initialize_greedy(graph2, communities)
    else:
        instance.initialize_random(graph2, communities)

    
    print("Generando snapshots...")
    snapshots = load_snapshots_email_core(graph2)
    
    
    if local_search or iterated_greedy:
        print("Aplicando Local Search...")
        snapshots = instance.local_search(snapshots, communities)
    if iterated_greedy:
        print("Aplicando Iterated Greedy...")
        snapshots = instance.iterated_greedy(snapshots, communities)
    return snapshots

def run_all(local_search = True, iterated_greedy = True, build_greedy = True):
    config_log()
    alg_used = ""
    if local_search:
        alg_used += "Local Search"

    if iterated_greedy:
        alg_used +=  " - Iterated Greedy"

    logging.info(f"Algoritmos usados: {alg_used}")
    start_total = time.time()

    communities = [f"Community {i + 1}" for i in range(NUMBER_OF_COMMUNITIES)]
    evaluator = Evaluator()

    # --- CollegeMsg ---
    start = time.time()
    snapshots_CollegeMsg = process_collegemsg(communities, local_search, iterated_greedy, build_greedy)
    time_college = (time.time() - start) 
    print(f"CollegeMsg listo en {time_college:.2f} segundos")

    # --- email-Eu-core ---
    start = time.time()
    snapshots_email = process_email_core(communities, local_search, iterated_greedy, build_greedy)
    time_email = (time.time() - start) 
    print(f"email-Eu-core listo en {time_email:.2f} segundos")

    evaluations_CollegeMsg = {}
    evaluations_email = {}

    # --- Logging resultados ---
    for (year, month), graph in snapshots_CollegeMsg.items():
        score = evaluator.evaluate_solution(graph, communities)
        evaluations_CollegeMsg[(year, month)] = score
        logging.info(f"CollegeMsg, {year}-{month:02d}: {score}")

    logging.info("")

    for (year, quarter), graph in snapshots_email.items():
        score = evaluator.evaluate_solution(graph, communities)
        evaluations_email[(year, quarter)] = score
        logging.info(f"email-Eu-core, {year}-C{quarter}: {score}")

    print(f"Tiempo total: {(time.time() - start_total) / 60:.2f} segundos\n")
    logging.info(f"Tiempo total: {(time.time() - start_total) / 60:.2f} segundos")

    return snapshots_CollegeMsg, snapshots_email, communities, evaluations_CollegeMsg, evaluations_email, time_college, time_email


if __name__ == "__main__":
    run_all()