from datetime import datetime
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
from algorithm_service import AlgorithmService
from io import StringIO
import csv

# from xhtml2pdf import pisa

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}}) 

snapshots_college = {}
snapshots_email = {}
communities = []
evaluations = {}

algorithm_service = AlgorithmService()

@app.route('/api/run', methods=['POST'])
def run():
    data = request.get_json()

    construccion = data.get('construccion', 'aleatorio')
    mejora = data.get('mejora', 'ninguna')

    build_greedy = (construccion == 'greedy')
    local_search = (mejora  == 'local_search')
    iterated_greedy = (mejora  == 'iterated_greedy')

    # Ejecuta los algoritmos
    algorithm_service.run(local_search, iterated_greedy, build_greedy)
    evaluations_college, evaluations_email = algorithm_service.get_evaluations()

    # Obtiene comunidades
    communities = algorithm_service.get_communities() 

    # Obtiene grafos
    graphs = algorithm_service.get_graphs() 

    # Prepara los datos para enviar al frontend
    eval_college_list = [
        {'snapshot': f"{year}-{month:02d}", 'score': round(score, 4)}
        for (year, month), score in sorted(evaluations_college.items())
    ]

    eval_email_list = [
        {'snapshot': f"{year}-Q{quarter}", 'score': round(score, 4)}
        for (year, quarter), score in sorted(evaluations_email.items())
    ]

    return jsonify({
        'evaluations_1': eval_college_list,
        'evaluations_2': eval_email_list,
        'communities': communities,
        'graphs': graphs
    })


@app.route('/api/comparison_summary', methods=['GET'])
def comparison_summary():
    summary = algorithm_service.get_comparison_summary()
    return jsonify(summary)


@app.route('/api/comparison_summary/download', methods=['GET'])
def download_comparison_summary_csv():
    summary = algorithm_service.get_comparison_summary()

    # Se crea un CSV en memoria
    si = StringIO()
    writer = csv.writer(si, delimiter=';')

    # Escribir encabezados
    writer.writerow(["Configuración"] + list(next(iter(summary.values())).keys()))

    # Escribir filas
    for config_name, metrics in summary.items():
        writer.writerow([config_name] + list(metrics.values()))

    now_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"comparison_summary_{now_str}.csv"

    # Devolver archivo cdv
    output = si.getvalue()
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


if __name__ == '__main__':
    app.run(debug=True)