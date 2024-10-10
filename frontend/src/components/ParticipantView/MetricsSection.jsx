// src/components/ParticipantView/MetricsSection.jsx
import React, { useEffect, useMemo, useState } from 'react';
import { ChevronRight } from 'lucide-react'; // Import the icon
import '../../styles/ParticipantView/MetricsSection.css';

const MetricsSection = ({ selectedGauge }) => {
  const [selectedDomain, setSelectedDomain] = useState('');

  const domainOptions = useMemo(() => {
    switch (selectedGauge) {
      case 'Integrity':
        return [
          'Structural data set error',
          'Data set combination error',
          'Value format error',
        ];
      case 'Completeness':
        return ['Crude missingness'];
      case 'Consistency':
        return ['Range and value violations', 'Contradictions'];
      case 'Accuracy':
        return ['Unexpected distributions', 'Unexpected associations'];
      default:
        return [];
    }
  }, [selectedGauge]);

  const metrics = {
    'Structural data set error': [
      { name: 'Unexpected data elements', issues: 2 },
      { name: 'Unexpected data records', issues: 5 },
      { name: 'Duplicates', issues: 0 },
    ],
    'Data set combination error': [
      { name: 'Data record mismatch', issues: 3 },
      { name: 'Data element mismatch', issues: 0 },
    ],
    'Value format error': [
      { name: 'Data type mismatch', issues: 1 },
      { name: 'Inhomogeneous value formats', issues: 4 },
      { name: 'Uncertain missingness status', issues: 2 },
    ],
    'Crude missingness': [
      {
        name: 'Missing values',
        issues: 7,
        hasActions: true, // Add this to specify that this metric has actions
      },
    ],
    'Range and value violations': [
      { name: 'Inadmissible numerical values', issues: 2 },
      { name: 'Inadmissible time-date values', issues: 1 },
      { name: 'Inadmissible categorical values', issues: 0 },
      { name: 'Inadmissible standardized vocabulary', issues: 3 },
      { name: 'Inadmissible precision', issues: 1 },
      { name: 'Uncertain numerical values', issues: 4 },
      { name: 'Uncertain time-date values', issues: 0 },
    ],
    Contradictions: [
      { name: 'Logical contradictions', issues: 1 },
      { name: 'Empirical contradictions', issues: 0 },
    ],
    'Unexpected distributions': [
      { name: 'Univariate outlier', issues: 3 },
      { name: 'Unexpected location', issues: 2 },
    ],
    'Unexpected associations': [
      { name: 'Unexpected association direction', issues: 1 },
    ],
  };

  useEffect(() => {
    if (domainOptions.length > 0) {
      setSelectedDomain(domainOptions[0]);
    }
  }, [domainOptions]);

  return (
    <div className="metrics-section">
      {selectedGauge !== 'Overall Score' && (
        <div className="domains">
          {domainOptions.map((domain) => (
            <div
              key={domain}
              className={`domain-button ${selectedDomain === domain ? 'active' : ''}`}
              onClick={() => setSelectedDomain(domain)}
            >
              {domain}
            </div>
          ))}
        </div>
      )}

      <div className="metrics-menu">
        {selectedGauge !== 'Overall Score' &&
          selectedDomain &&
          metrics[selectedDomain] &&
          metrics[selectedDomain].map((metric) => (
            <div key={metric.name} className="metric-item">
              <div className="metric-text">
                <span className="metric-name">{metric.name}</span>
                <span className={`metric-issues ${metric.issues > 0 ? 'clickable' : ''}`}>
                  {metric.issues} {metric.issues === 1 ? 'issue' : 'issues'} found
                </span>
              </div>
              {metric.hasActions && (
                <ChevronRight className="expand-icon" size={24} />
              )}
            </div>
          ))}
      </div>

      {selectedGauge !== 'Overall Score' && (
        <div className="buttons">
          <button className="discard-button">Discard</button>
          <button className="save-button">Save changes</button>
        </div>
      )}
    </div>
  );
};

export default MetricsSection;
