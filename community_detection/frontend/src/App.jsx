import React, { useState } from 'react';
import Header from './components/Header';
import AlgorithmSelector from './components/AlgorithmSelector';
import CommunityResults from './components/CommunityResults';
import EvaluationCharts from './components/EvaluationCharts';
import Footer from './components/Footer';
import ComparisonView from './components/ComparisonView'; // Renombrado aquí
import GraphView from './components/GraphView';

const App = () => {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [view, setView] = useState('main'); // 'main', 'comparison', 'graph'
  const [selectedDataset, setSelectedDataset] = useState("CollegeMsg");
  const [selectedSnapshot, setSelectedSnapshot] = useState("");
  const [graphData, setGraphData] = useState(null);
  const [graphs, setGraphs] = useState({});
  const [construccion, setConstruccion] = useState('aleatorio');
  const [mejora, setMejora] = useState('ninguna');

  const runAlgorithm = async () => {
  setLoading(true);
  setResults(null);
  setError(null);
  setGraphData(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ construccion, mejora }),
      });
      if (!response.ok) throw new Error(`Error ${response.status}: ${response.statusText}`);
      
      const data = await response.json();
      setResults(data);
      setGraphs(data.graphs);

      const firstDataset = Object.keys(data.graphs)[0];
      const firstSnapshot = Object.keys(data.graphs[firstDataset])[0];
      setSelectedDataset(firstDataset);
      setSelectedSnapshot(firstSnapshot);
      setGraphData(data.graphs[firstDataset][firstSnapshot])

    } catch (err) {
      console.error('API request failed:', err);
      setError('No se pudo obtener resultados. Intenta nuevamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <nav className="nav-tabs">
        <button
          className={`tab-button ${view === 'main' ? 'active' : ''}`}
          onClick={() => setView('main')}
        >
          Ejecutar Algoritmo
        </button>
        <button
          className={`tab-button ${view === 'comparison' ? 'active' : ''}`}
          onClick={() => setView('comparison')}
        >
          Comparación
        </button>
        <button
          className={`tab-button ${view === 'graph' ? 'active' : ''}`}
          onClick={() => setView('graph')}
        >
          Grafos
        </button>
      </nav>

      {view === 'main' && (
        <>
          <Header />
          <AlgorithmSelector
            construccion={construccion}
            setConstruccion={setConstruccion}
            mejora={mejora}
            setMejora={setMejora}
            runAlgorithmApi={runAlgorithm}
            loading={loading}
          />
          {error && <div style={{ color: 'red', marginBottom: '1rem' }}>{error}</div>}
          <EvaluationCharts results={results} />
          <CommunityResults results={results} />
          <Footer />
        </>
      )}

      {view === 'comparison' && <ComparisonView />} {/* Renombrado aquí */}

      {view === 'graph' && (
        <div className="graph-view-container">
          <div style={{ padding: '1rem' }}>
            <div style={{ marginBottom: '1rem' }}>
              <label>Dataset: </label>
              <select
                value={selectedDataset}
                onChange={(e) => {
                  const dataset = e.target.value;
                  setSelectedDataset(dataset);
                  const firstSnapshot = Object.keys(graphs[dataset])[0];
                  setSelectedSnapshot(firstSnapshot);
                  setGraphData(graphs[dataset][firstSnapshot]);
                }}
              >
                {Object.keys(graphs).map((name) => (
                  <option key={name} value={name}>
                    {name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <label>Snapshot: </label>
            <select
              value={selectedSnapshot}
              onChange={(e) => {
                const snapshot = e.target.value;
                setSelectedSnapshot(snapshot);
                setGraphData(graphs[selectedDataset][snapshot]);
              }}
            >
              {selectedDataset &&
                graphs[selectedDataset] &&
                Object.keys(graphs[selectedDataset]).map((snap) => (
                  <option key={snap} value={snap}>
                    {snap}
                  </option>
                ))}
            </select>
          </div>

          <GraphView graphData={graphData} />
        </div>
      )}
    </div>
  );
};

export default App;
