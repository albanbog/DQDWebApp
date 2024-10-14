// src/components/ParticipantView/ParticipantView.jsx
import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import GaugesSection from './GaugesSection';
import ParticipantInfo from './ParticipantInfo';
import TreeSection from './TreeSection';
import MetricsSection from './MetricsSection';
import '../../styles/ParticipantView/ParticipantView.css';

const ParticipantView = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Get report data from location state
  const report = location.state?.report;

  const [selectedGauge, setSelectedGauge] = useState('Overall Score');
  const [selectedNode, setSelectedNode] = useState('lightly_active_minutes');

  // Update participantInfo and report score with report data
  const [participantInfo] = useState({
    id: report?.id || 'p05',
    timePeriod: 'January 2024 – February 2024', // Example time period
    reportDate: report?.date || '03.03.2024',
  });

  const reportScore = report?.score || 60; // Use report score or a default value of 60

  const handleHomeClick = () => {
    navigate('/');
  };

  return (
    <div className="participant-view">
      <div className="home-icon" onClick={handleHomeClick}>
        <img src="/home.png" alt="Home" className="home-icon-image" />
      </div>

      <div className="top-section">
        <GaugesSection
          selectedGauge={selectedGauge}
          setSelectedGauge={setSelectedGauge}
          score={reportScore} // Pass the report score to the GaugesSection
        />
        <ParticipantInfo participantInfo={participantInfo} />
      </div>

      <div className="content-section">
        <TreeSection
          selectedGauge={selectedGauge}
          selectedNode={selectedNode}
          setSelectedNode={setSelectedNode}
          participantId={participantInfo.id} // Pass the participant ID
          score={reportScore} // Pass the report score to the TreeSection
        />
        <MetricsSection selectedGauge={selectedGauge} selectedNode={selectedNode} />
      </div>
    </div>
  );
};

export default ParticipantView;
