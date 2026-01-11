from collections import defaultdict

class AlgorithmComparator:
    def __init__(self):
        self.executions = {}

    def add_execution(self, algorithm_name: str, dataset_name: str, score_dict: dict[str, float], execution_time: float, build_greedy: bool):
        key = f"{algorithm_name} - {dataset_name}"
        avg_score = sum(score_dict.values()) / len(score_dict)

        if key not in self.executions:
            self.executions[key] = {
                "scores": [],
                "times": [],
                "evaluations": [],
                "build_greedy_flags": [],
            }

        self.executions[key]["scores"].append(avg_score)
        self.executions[key]["times"].append(execution_time)
        self.executions[key]["evaluations"].append(score_dict)
        self.executions[key]["build_greedy_flags"].append(build_greedy)

    def summarize(self) -> dict:
        summary = {}

        # Primero agrupar ejecuciones por dataset y construcción
        grouped_data = defaultdict(lambda: {"scores": [], "times": [], "build_greedy_flags": []})

        for key, data in self.executions.items():
            algorithm, dataset = key.split(" - ")
            build_greedy_flags = data.get("build_greedy_flags", [])
            scores = data["scores"]
            times = data["times"]

            # Agrupar según construcción (Greedy o Aleatorio)
            # Si no hay flags, lo pongo como "Desconocido"
            if build_greedy_flags:
                # Agrupar según flag en True o False
                for score, time, flag in zip(scores, times, build_greedy_flags):
                    constr_str = "Greedy" if flag else "Aleatorio"
                    group_key = (algorithm, dataset, constr_str)
                    grouped_data[group_key]["scores"].append(score)
                    grouped_data[group_key]["times"].append(time)
                    grouped_data[group_key]["build_greedy_flags"].append(flag)
            else:
                # No hay flags, grupo todo en "Desconocido"
                group_key = (algorithm, dataset, "Desconocido")
                grouped_data[group_key]["scores"].extend(scores)
                grouped_data[group_key]["times"].extend(times)
                grouped_data[group_key]["build_greedy_flags"].extend([None]*len(scores))

        # Calcular el mejor promedio por dataset
        best_per_dataset = {}
        for (algorithm, dataset, constr), data in grouped_data.items():
            avg_score = sum(data["scores"]) / len(data["scores"]) if data["scores"] else 0
            if dataset not in best_per_dataset or avg_score > best_per_dataset[dataset]:
                best_per_dataset[dataset] = avg_score

        # Ahora armar el resumen por grupo (algoritmo, dataset y construcción)
        for (algorithm, dataset, constr), data in grouped_data.items():
            scores = data["scores"]
            times = data["times"]
            avg_score = sum(scores) / len(scores) if scores else 0
            total_time = sum(times) / len(times) if times else 0
            best_score = best_per_dataset.get(dataset, 0)

            std_dev_percent = 0.0
            if best_score > 0:
                 std_dev_percent = abs(avg_score - best_score) / best_score * 100

            best_count = sum(1 for score in scores if score == best_score)

            label = f"{algorithm} - {dataset} - {constr}"

            summary[label] = {
                "Construccion": constr,
                "Mejora": algorithm,
                "Prom. función objetivo": round(avg_score, 4),
                "Tiempo total (s)": round(total_time, 2),
                "Desv. % respecto al mejor": round(std_dev_percent, 2),
                "N° veces mejor resultado": best_count,
                "N° ejecuciones": len(scores),
            }

        return summary

    def get_raw_data(self) -> dict:
        return self.executions
