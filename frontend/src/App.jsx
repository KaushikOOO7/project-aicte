import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [demoData, setDemoData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [datasetName, setDatasetName] = useState('Supermarket_Sales.csv');

  const fetchDemoData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('http://localhost:8000/api/demo');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setDemoData(data);
      setDatasetName(data.dataset);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDemoData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Data Analyst</h1>
        <p>Turn raw data into intelligent decisions.</p>
        <div className="dataset-info">
          <span>Dataset: {datasetName}</span>
          <span>Status: Ready</span>
        </div>
      </header>

      <main>
        <div className="upload-section">
          <h2>Upload Your Dataset</h2>
          <p>Upload CSV or Excel file for analysis</p>
          <button className="upload-btn">Upload CSV / Excel</button>
        </div>

        {loading && <p>Loading demo data...</p>}
        {error && <p className="error">Error: {error}</p>}

        {demoData && (
          <div className="demo-section">
            <h2>Explore Demo Dataset</h2>
            <div className="profile-card">
              <div className="profile-header">
                <h3>Dataset Profile</h3>
                <div className="profile-stats">
                  <span>Rows: {demoData.profile.rows}</span>
                  <span>Columns: {demoData.profile.columns}</span>
                  <span>Memory: {demoData.profile.memory_mb} MB</span>
                </div>
              </div>
              <div className="profile-details">
                <div className="stat-group">
                  <h4>Data Types</h4>
                  <div className="stat-item">
                    <span>Numeric:</span> {demoData.profile.numeric_columns}</div>
                  <div className="stat-item">
                    <span>Categorical:</span> {demoData.profile.categorical_columns}</div>
                  </div>
                </div>
                <div className="stat-group">
                  <h4>Missing Values</h4>
                  <div className="stat-item">
                    <span>Total:</span> {demoData.profile.missing_values}</div>
                </div>
                <div className="stat-group">
                  <h4>Duplicate Rows</h4>
                  <div className="stat-item">
                    <span>Found:</span> {demoData.profile.duplicate_rows}</div>
                </div>
              </div>
            </div>

            <div className="statistics-section">
              <h3>Key Statistics</h3>
              <div className="statistics-grid">
                {Object.entries(demoData.statistics).map(([col, stats]) => (
                  <div key={col} className="stat-card">
                    <h4>{col}</h4>
                    <div className="stat-values">
                      <span>Mean: {stats.mean.toFixed(2)}</span>
                      <span>Median: {stats.median.toFixed(2)}</span>
                      <span>Std Dev: {stats.std.toFixed(2)}</span>
                    </div>
                    <div className="stat-extremes">
                      <span>Min: {stats.min.toFixed(2)}</span>
                      <span>Max: {stats.max.toFixed(2)}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>
      <footer className="App-footer">
        <p>© 2026 AI Data Analyst. All rights reserved.</p>
      </footer>
    </div>
  );
}

export default App;