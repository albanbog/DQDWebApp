// src/components/ParticipantView/GaugesSection.jsx
import React from 'react';
import SemicircleGauge from './SemicircleGauge';
import '../../styles/ParticipantView/GaugesSection.css';

const GaugesSection = ({ selectedGauge, setSelectedGauge }) => {
  const scores = {
    Integrity: 60.23,
    Completeness: 49.31,
    Consistency: 31.25,
    Accuracy: 81.23,
  };

  // Calculate the overall score as an average of the other four scores
  const overallScore = parseFloat(
    (
      (scores.Integrity +
        scores.Completeness +
        scores.Consistency +
        scores.Accuracy) /
      4
    ).toFixed(2)
  );

  const gauges = [
    { title: 'Overall Score', value: overallScore },
    { title: 'Integrity', value: scores.Integrity },
    { title: 'Completeness', value: scores.Completeness },
    { title: 'Consistency', value: scores.Consistency },
    { title: 'Accuracy', value: scores.Accuracy },
  ];

  return (
    <div className="gauges-section">
      {gauges.map((gauge, index) => (
        <div
          key={index}
          className={`gauge-box ${selectedGauge === gauge.title ? 'selected' : ''}`}
          onClick={() => setSelectedGauge(gauge.title)}
        >
          <SemicircleGauge
            value={gauge.value}
            maxValue={100}
            title={gauge.title}
            width={150}
            height={120}
          />
        </div>
      ))}
    </div>
  );
};

export default GaugesSection;
