import React from 'react';
import '../styles/ProfileSection.css'; // Profile section-specific styles

export const ProfileSection = () => {
  return (
    <div className="profile-section">
      <i className="profile-icon">👤</i>
      <span className="username">Max Mustermann</span>
    </div>
  );
};
