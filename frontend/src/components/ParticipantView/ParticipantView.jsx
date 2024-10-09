// src/components/ParticipantView/ParticipantView.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import GaugesSection from './GaugesSection';
import ParticipantInfo from './ParticipantInfo';
import TreeSection from './TreeSection';
import MetricsSection from './MetricsSection';
import '../../styles/ParticipantView/ParticipantView.css';

const ParticipantView = () => {
  const [selectedGauge, setSelectedGauge] = useState('Overall Score');
  const [selectedNode, setSelectedNode] = useState('lightly_active_minutes');
  const [participantInfo] = useState({
    id: 'p05',
    timePeriod: 'January 2024 – February 2024',
    reportDate: '03.03.2024',
  });

  const navigate = useNavigate();

  const handleHomeClick = () => {
    navigate('/');
  };

  return (
    <div className="participant-view">
      <div className="home-icon" onClick={handleHomeClick}>
        <img src="/home.png" alt="Home" className="home-icon-image" />
      </div>

      <div className="top-section">
        <GaugesSection selectedGauge={selectedGauge} setSelectedGauge={setSelectedGauge} />
        <ParticipantInfo participantInfo={participantInfo} />
      </div>

      <div className="content-section">
        <TreeSection selectedGauge={selectedGauge} selectedNode={selectedNode} setSelectedNode={setSelectedNode} />
        <MetricsSection selectedGauge={selectedGauge} selectedNode={selectedNode} />
      </div>
    </div>
  );
};

export default ParticipantView;
