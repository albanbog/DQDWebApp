// src/components/ParticipantView/SemicircleGauge.jsx
import React from 'react';

const SemicircleGauge = ({ value, maxValue, title, width = 150, height = 120 }) => {
  const percentage = (value / maxValue) * 100;
  const strokeWidth = width * 0.21; // Adjusted stroke width for a less thick gauge
  const titleHeight = 25;
  const gaugeHeight = height - titleHeight;
  const radius = (Math.min(width, gaugeHeight * 2) / 2) - (strokeWidth / 2);
  const circumference = radius * Math.PI;
  const strokeDashoffset = circumference - (percentage / 100) * circumference;

  const getColor = (percent) => {
    if (percent <= 33) return '#FF4136'; // Red
    if (percent <= 66) return '#FF851B'; // Orange
    return '#2ECC40'; // Green
  };

  return (
    <div
      className="semicircle-gauge"
      style={{
        width,
        height,
        backgroundColor: '#325a74',
        borderRadius: '10px',
        padding: '5px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      <div
        className="gauge-title"
        style={{
          height: `${titleHeight}px`,
          fontSize: '18px',
          color: 'white',
          textAlign: 'center',
          fontWeight: 'bold',
        }}
      >
        {title}
      </div>
      <svg width={width - 16} height={gaugeHeight - 8} viewBox={`0 0 ${width} ${gaugeHeight}`}>
        <path
          d={`M ${strokeWidth / 2},${gaugeHeight - strokeWidth / 2} A ${radius},${radius} 0 0 1 ${width - strokeWidth / 2},${gaugeHeight - strokeWidth / 2}`}
          fill="none"
          stroke="#1a2e3d" // Darker color for the gauge background
          strokeWidth={strokeWidth}
        />
        <path
          d={`M ${strokeWidth / 2},${gaugeHeight - strokeWidth / 2} A ${radius},${radius} 0 0 1 ${width - strokeWidth / 2},${gaugeHeight - strokeWidth / 2}`}
          fill="none"
          stroke={getColor(percentage)}
          strokeWidth={strokeWidth}
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
        />
        <text
          x="50%"
          y={gaugeHeight - strokeWidth / 2}
          textAnchor="middle"
          dominantBaseline="middle"
          fill="white"
          fontSize={`${width * 0.12}px`}
          fontWeight="bold"
        >
          {value.toFixed(2)}%
        </text>
      </svg>
    </div>
  );
};

export default SemicircleGauge;
