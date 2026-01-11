import React, { useEffect, useState } from 'react'; 

const ComparisonView = () => {
  const [summary, setSummary] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estado para ordenar: key es la columna, order es 'asc' o 'desc'
  const [sortConfig, setSortConfig] = useState({ key: null, order: 'asc' });

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/comparison_summary');
        if (!response.ok) throw new Error(`Error ${response.status}`);
        const data = await response.json();
        setSummary(data);
      } catch (err) {
        console.error('Error fetching summary:', err);
        setError('No se pudo cargar el resumen de comparaciones.');
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, []);

  // Función para ordenar al hacer clic en encabezado
  const handleSort = (key) => {
    let order = 'asc';
    if (sortConfig.key === key && sortConfig.order === 'asc') {
      order = 'desc';
    }
    setSortConfig({ key, order });
  };

  // Transformar summary en array para ordenar
  const summaryEntries = Object.entries(summary).map(([label, values]) => {
    const parts = label.split(" - ");
    const dataset = parts[1];
    return { label, dataset, values };
  });

  // Función para comparar según el campo
  const compare = (a, b) => {
    if (!sortConfig.key) return 0; // No ordenar si no hay clave

    let aVal, bVal;

    switch (sortConfig.key) {
      case 'Dataset':
        aVal = a.dataset;
        bVal = b.dataset;
        break;
      case 'Construcción':
        aVal = a.values["Construccion"];
        bVal = b.values["Construccion"];
        break;
      case 'Mejora':
        aVal = a.values["Mejora"];
        bVal = b.values["Mejora"];
        break;
      case 'Prom. función objetivo':
        aVal = a.values["Prom. función objetivo"];
        bVal = b.values["Prom. función objetivo"];
        break;
      case 'Tiempo total (mins)':
        // Recuerda que en el API tienes "Tiempo total (s)", pero en tabla es en mins
        aVal = a.values["Tiempo total (s)"] / 60;
        bVal = b.values["Tiempo total (s)"] / 60;
        break;
      case 'Desv. % respecto al mejor':
        aVal = a.values["Desv. % respecto al mejor"];
        bVal = b.values["Desv. % respecto al mejor"];
        break;
      case 'N° veces mejor resultado':
        aVal = a.values["N° veces mejor resultado"];
        bVal = b.values["N° veces mejor resultado"];
        break;
      case 'N° ejecuciones':
        aVal = a.values["N° ejecuciones"];
        bVal = b.values["N° ejecuciones"];
        break;
      default:
        return 0;
    }

    if (aVal == null) return 1;
    if (bVal == null) return -1;

    if (typeof aVal === 'string') {
      const result = aVal.localeCompare(bVal);
      return sortConfig.order === 'asc' ? result : -result;
    } else {
      const result = aVal - bVal;
      return sortConfig.order === 'asc' ? result : -result;
    }
  };

  // Ordenar los datos
  const sortedEntries = [...summaryEntries].sort(compare);

  const handleDownloadCSV = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/comparison_summary/download');
      if (!response.ok) throw new Error(`Error ${response.status}`);
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const now = new Date();
      const timestamp = now.toISOString().replace(/[:.]/g, '-');
      const filename = `comparison_summary_${timestamp}.csv`;
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading CSV:', err);
      alert('No se pudo descargar el archivo CSV.');
    }
  };

  if (loading) return <p style={{ padding: '1rem' }}>Cargando resumen...</p>;
  if (error) return <p style={{ padding: '1rem', color: 'red' }}>{error}</p>;

  // Para indicar en el header el orden (flechas)
  const getSortIndicator = (key) => {
    if (sortConfig.key !== key) return '';
    return sortConfig.order === 'asc' ? ' ▲' : ' ▼';
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2 style={{ marginBottom: '1rem' }}>Resumen Comparativo de Algoritmos</h2>

      <button
        onClick={handleDownloadCSV}
        style={{
          marginBottom: '1rem',
          padding: '0.5rem 1rem',
          backgroundColor: '#646cff',
          color: 'white',
          border: 'none',
          borderRadius: '6px',
          cursor: 'pointer',
        }}
      >
        Descargar CSV
      </button>

      <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: '#1e1e1e', color: '#fff' }}>
        <thead>
          <tr style={{ backgroundColor: '#646cff' }}>
            <th style={thStyle} onClick={() => handleSort('Dataset')}>
              Dataset{getSortIndicator('Dataset')}
            </th>
            <th style={thStyle} onClick={() => handleSort('Construcción')}>
              Construcción{getSortIndicator('Construcción')}
            </th>
            <th style={thStyle} onClick={() => handleSort('Mejora')}>
              Mejora{getSortIndicator('Mejora')}
            </th>
            <th style={thStyle} onClick={() => handleSort('Prom. función objetivo')}>
              Prom. función objetivo{getSortIndicator('Prom. función objetivo')}
            </th>
            <th style={thStyle} onClick={() => handleSort('Tiempo total (mins)')}>
              Tiempo medio (mins){getSortIndicator('Tiempo total (mins)')}
            </th>
            <th style={thStyle} onClick={() => handleSort('Desv. % respecto al mejor')}>
              Desv. % respecto al mejor{getSortIndicator('Desv. % respecto al mejor')}
            </th>
            <th style={thStyle} onClick={() => handleSort('N° veces mejor resultado')}>
              N° veces mejor resultado{getSortIndicator('N° veces mejor resultado')}
            </th>
            <th style={thStyle} onClick={() => handleSort('N° ejecuciones')}>
              N° ejecuciones{getSortIndicator('N° ejecuciones')}
            </th>
          </tr>
        </thead>
        <tbody>
          {sortedEntries.map(({ label, dataset, values }) => (
            <tr key={label}>
              <td style={tdStyle}>{dataset}</td>
              <td style={tdStyle}>{values["Construccion"]}</td>
              <td style={tdStyle}>{values["Mejora"]}</td>
              <td style={tdStyle}>{values["Prom. función objetivo"]?.toFixed(4)}</td>
              <td style={tdStyle}>{(values["Tiempo total (s)"])?.toFixed(2)}</td>
              <td style={tdStyle}>{values["Desv. % respecto al mejor"]?.toFixed(2)}%</td>
              <td style={tdStyle}>{values["N° veces mejor resultado"]}</td>
              <td style={tdStyle}>{values["N° ejecuciones"]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

const thStyle = {
  padding: '0.6rem',
  border: '1px solid #ccc',
  textAlign: 'left',
  cursor: 'pointer', // Mostrar que es clickeable
  userSelect: 'none',
};

const tdStyle = {
  padding: '0.6rem',
  border: '1px solid #ccc',
};

export default ComparisonView;
