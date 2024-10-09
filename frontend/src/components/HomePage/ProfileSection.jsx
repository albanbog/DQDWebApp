import React from 'react';
import '../../styles/HomePage/ProfileSection.css';

export const ProfileSection = () => {
  return (
    <div className="profile-section">
      <span className="username">Max Mustermann</span>
      <img src="/profile.png" alt="Profile" className="profile-icon" />
    </div>
  );
};