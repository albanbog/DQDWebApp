// src/components/ParticipantView/MetricsInfo.jsx
import React, { useState } from 'react';
import { Info } from 'lucide-react';
import '../../styles/ParticipantView/MetricsInfo.css';

const MetricsInfo = ({ metricsInfo }) => {
  const [showPopup, setShowPopup] = useState(false);
  const togglePopup = () => setShowPopup(!showPopup);

  return (
    <div className="metrics-info-wrapper relative flex justify-center items-center h-full">
      <div className="metrics-info-container p-4 flex items-center rounded-lg" style={{ minWidth: '360px', backgroundColor: '#333E5A' }}>
        <div className="bg-black w-8 h-8 rounded-full absolute left-4"></div>
        <div className="w-full pl-12">
          <div className="info-row mb-2 pb-1">
            <span className="text-white font-semibold text-lg italic">
              Metric Name: {metricsInfo.name}
            </span>
            <Info
              className="info-icon text-white"
              size={28}
              onClick={togglePopup}
            />
            {showPopup && (
              <div className="metrics-info-popup">
                <h3>Metric Information</h3>
                <p>Description: {metricsInfo.description}</p>
                <p>Issues Found: {metricsInfo.issues}</p>
              </div>
            )}
          </div>
          <div className="info-row text-white pb-1 mb-2 text-lg italic">
            Last Updated: {metricsInfo.lastUpdated}
          </div>
          <div className="info-row-left text-white pb-1 text-lg italic">
            Status: {metricsInfo.status}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MetricsInfo;
