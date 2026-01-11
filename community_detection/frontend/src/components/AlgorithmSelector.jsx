import React, { useState } from 'react';

const AlgorithmSelector = ({ construccion, setConstruccion, mejora, setMejora,runAlgorithmApi, loading }) => {

  const runAlgorithm = () => {
    runAlgorithmApi({ construccion, mejora});
  };

  return (
    <section style={{ marginBottom: '1.5rem' }} className="algorithm-selector">
      <label htmlFor="construccion-select" style={{ marginRight: '0.5rem', fontWeight: 'bold' }}>
        Construcción:
      </label>
      <select
        id="construccion-select"
        value={construccion}
        onChange={e => setConstruccion(e.target.value)}
        disabled={loading}
        style={{ padding: '0.3rem', marginRight: '1rem' }}
      >
        <option value="aleatorio">Aleatorio</option>
        <option value="greedy">Greedy</option>
      </select>

      <label htmlFor="mejora-select" style={{ marginRight: '0.5rem', fontWeight: 'bold' }}>
        Mejora:
      </label>
      <select
        id="mejora-select"
        value={mejora}
        onChange={e => setMejora(e.target.value)}
        disabled={loading}
        style={{ padding: '0.3rem', marginRight: '1rem' }}
      >
        <option value="ninguna">Ninguna</option>
        <option value="local_search">Local Search</option>
        <option value="iterated_greedy">Iterated Greedy</option>
      </select>

      <button onClick={runAlgorithm} disabled={loading} style={{ padding: '0.4rem 1rem' }}>
        {loading ? 'Ejecutando...' : 'Ejecutar'}
      </button>
    </section>
  );
};

export default AlgorithmSelector;
