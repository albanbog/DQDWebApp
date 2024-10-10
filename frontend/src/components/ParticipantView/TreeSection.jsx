import React, { useState, useRef, useEffect, useCallback } from 'react';
import '../../styles/ParticipantView/TreeSection.css';

// Move these outside the component
const rootNode = { name: "Participant ID: p04", value: 60 };
const folderData = [
  { name: "fitbit", value: 50, expandable: true },
  { name: "pmsys", value: 0, expandable: false },
  { name: "googledocs", value: 0, expandable: false },
];

const leafData = {
  fitbit: [
    { name: "lightly_active_minutes", value: 38 },
    { name: "moderately_active_minutes", value: 85 },
    { name: "resting_heart_rate", value: 76 },
    { name: "sedentary_minutes", value: 28 },
    { name: "time_in_heart_rate_zones", value: 70 },
    { name: "very_active_minutes", value: 97 },
    { name: "steps", value: 66 },
    { name: "distance", value: 52 },
    { name: "exercise", value: 13 },
    { name: "calories", value: 42 },
    { name: "heart_rate", value: 85 },
    { name: "sleep", value: 91 },
  ],
  pmsys: [],
  googledocs: [],
};

const ProgressBar = ({ value }) => {
  const getProgressBarColor = (value) => {
    if (value <= 33) return '#FF4136'; // Red
    if (value <= 66) return '#FF851B'; // Orange
    return '#2ECC40'; // Green
  };

  return (
    <div className="progress-bar">
      <div className="progress-fill" style={{ width: `${value}%`, backgroundColor: getProgressBarColor(value) }} />
    </div>
  );
};

const Node = React.forwardRef(({ name, value, isSelected, onClick }, ref) => (
  <div ref={ref} className={`node ${isSelected ? 'selected' : ''}`} onClick={onClick}>
    <div className="node-content">
      <span className="node-name">{name}</span>
      <span className="node-value">{value}%</span>
    </div>
    <ProgressBar value={value} />
  </div>
));

const TreeSection = ({ selectedGauge }) => {
  const [selectedFolder, setSelectedFolder] = useState('fitbit');
  const [selectedLeaf, setSelectedLeaf] = useState(null);
  const [connections, setConnections] = useState([]);

  const rootNodeRef = useRef(null);
  const folderRefs = useRef({});
  const leafRefs = useRef({});

  const calculateConnections = useCallback(() => {
    const newConnections = [];

    if (rootNodeRef.current) {
      const rootRect = rootNodeRef.current.getBoundingClientRect();
      folderData.forEach((folder) => {
        const folderRef = folderRefs.current[folder.name];
        if (folderRef) {
          const folderRect = folderRef.getBoundingClientRect();
          newConnections.push({
            x1: rootRect.right,
            y1: rootRect.top + rootRect.height / 2,
            x2: folderRect.left,
            y2: folderRect.top + folderRect.height / 2,
            type: 'root-to-folder',
            folderName: folder.name,
          });
        }
      });
    }

    const selectedFolderRef = folderRefs.current[selectedFolder];
    if (selectedFolderRef && selectedFolder === 'fitbit') {
      const folderRect = selectedFolderRef.getBoundingClientRect();
      leafData[selectedFolder].forEach((leaf) => {
        const leafRef = leafRefs.current[leaf.name];
        if (leafRef) {
          const leafRect = leafRef.getBoundingClientRect();
          newConnections.push({
            x1: folderRect.right,
            y1: folderRect.top + folderRect.height / 2,
            x2: leafRect.left,
            y2: leafRect.top + leafRect.height / 2,
            type: 'folder-to-leaf',
            folderName: selectedFolder,
            leafName: leaf.name,
          });
        }
      });
    }

    setConnections(newConnections);
  }, [selectedFolder]);

  useEffect(() => {
    calculateConnections();
    window.addEventListener('resize', calculateConnections);

    return () => {
      window.removeEventListener('resize', calculateConnections);
    };
  }, [calculateConnections]);

  return (
    <div className="tree-section">
      <div className="tree-title-container">
        <h3 className="tree-title">{selectedGauge}</h3>
      </div>
      <div className="tree-content">
        <div className="root-node">
          <Node
            ref={rootNodeRef}
            name={rootNode.name}
            value={rootNode.value}
            isSelected={false}
            onClick={() => {}}
          />
        </div>
        <div className="folders">
          {folderData.map((folder) => (
            <Node
              key={folder.name}
              ref={(el) => (folderRefs.current[folder.name] = el)}
              name={folder.name}
              value={folder.value}
              isSelected={selectedFolder === folder.name}
              onClick={() => setSelectedFolder(folder.name)}
            />
          ))}
        </div>
        <div className="leaves">
          {leafData[selectedFolder] && selectedFolder === 'fitbit' && leafData[selectedFolder].map((leaf) => (
            <Node
              key={leaf.name}
              ref={(el) => (leafRefs.current[leaf.name] = el)}
              name={leaf.name}
              value={leaf.value}
              isSelected={selectedLeaf === leaf.name}
              onClick={() => setSelectedLeaf(leaf.name)}
            />
          ))}
        </div>
      </div>
      <svg className="connection-lines">
      {connections.map((connection, index) => (
        <path
          key={index}
          data-type={connection.type}
          d={`M${connection.x1},${connection.y1} C${connection.x1 + 50},${connection.y1} ${connection.x2 - 50},${connection.y2} ${connection.x2},${connection.y2}`}
          stroke={
            (connection.type === 'root-to-folder' && connection.folderName === selectedFolder) ||
            (connection.type === 'folder-to-leaf' && connection.leafName === selectedLeaf)
              ? "yellow"
              : "white"
          }
          strokeWidth="2"
          fill="none"
        />
      ))}
    </svg>
  </div>
  );
};

export default TreeSection;