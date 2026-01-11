import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend
} from "recharts";

const EvaluationCharts = ({ results }) => {
  if (!results || !results.evaluations_1 || !results.evaluations_2) return null;

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Evaluaciones: CollegeMsg</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={results.evaluations_1} margin={{ top: 20, right: 0, bottom: 30, left: 0 }}>
          <XAxis dataKey="snapshot" interval={0} angle={-45} textAnchor="end"/>
          <YAxis />
          <Tooltip />
          <Legend layout="vertical" align="right" verticalAlign="middle" wrapperStyle={{ right:-10 }}/>
          <CartesianGrid stroke="#ccc" />
          <Line type="monotone" dataKey="score" stroke="#8884d8" />
        </LineChart>
      </ResponsiveContainer>

      <h2 style={{ marginTop: '3rem' }}>Evaluaciones: Email-Eu-core</h2>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={results.evaluations_2} margin={{ top: 20, right: 0, bottom: 30, left: 0 }}>
          <XAxis dataKey="snapshot" interval={0} angle={-45} textAnchor="end"/>
          <YAxis />
          <Tooltip />
          <Legend layout="vertical" align="right" verticalAlign="middle" wrapperStyle={{ right:-10 }}/>
          <CartesianGrid stroke="#ccc" />
          <Line type="monotone" dataKey="score" stroke="#82ca9d" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default EvaluationCharts;
