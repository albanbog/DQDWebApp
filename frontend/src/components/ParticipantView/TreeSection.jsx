// src/components/ParticipantView/TreeSection.jsx
import React from 'react';
import '../../styles/ParticipantView/TreeSection.css';

const TreeSection = ({ selectedGauge }) => {
  return (
    <div className="tree-section">
      <div className="tree-title-container">
        <h3 className="tree-title">{selectedGauge}</h3>
      </div>
      {/* Placeholder for the tree structure, to be added later */}
      <p className="tree-placeholder" style={{ color: 'white', textAlign: 'center' }}>
        Tree structure will appear here.
      </p>
    </div>
  );
};

export default TreeSection;
