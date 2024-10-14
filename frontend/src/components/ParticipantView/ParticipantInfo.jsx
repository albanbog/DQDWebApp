// src/components/ParticipantView/ParticipantInfo.jsx
import React, { useState } from 'react';
import { Info } from 'lucide-react';
import '../../styles/ParticipantView/ParticipantInfo.css';

const ParticipantInfo = ({ participantInfo }) => {
  const [showPopup, setShowPopup] = useState(false);
  const togglePopup = () => setShowPopup(!showPopup);

  return (
    <div className="participant-info-wrapper relative flex justify-center items-center h-full">
      <div className="participant-info-container p-4 flex items-center rounded-lg" style={{ minWidth: '360px', backgroundColor: '#333E5A' }}>
        <div className="bg-black w-8 h-8 rounded-full absolute left-4"></div>
        <div className="w-full pl-12">
          <div className="info-row mb-2 pb-1">
            <span className="text-white font-semibold text-lg italic">
              Participant ID: {participantInfo.id}
            </span>
            <Info
              className="info-icon text-white"
              size={28}
              onClick={togglePopup}
            />
            {showPopup && (
              <div className="participant-info-popup">
                <h3>Participant Information</h3>
                <p>Participant ID: {participantInfo.id}</p>
                <p>Age: 48</p>
                <p>Height: 195 cm</p>
                <p>Gender: Male</p>
              </div>
            )}
          </div>
          <div className="info-row text-white pb-1 mb-2 text-lg italic">
            Time Period: {participantInfo.timePeriod}
          </div>
          <div className="info-row-left text-white pb-1 text-lg italic">
            Report Date: {participantInfo.reportDate}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ParticipantInfo;