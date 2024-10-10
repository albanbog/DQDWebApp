// src/components/HomePage/SidebarMenu.jsx
import React from 'react';
import '../../styles/HomePage/SidebarMenu.css';

export const SidebarMenu = () => {
  const handleDashboardClick = () => {
    window.location.reload();
  };

  return (
    <div className="sidebar-container">
      {/* Menu Section */}
      <div className="menu-items">
        <h2 className="menu-title">
          Data Quality <br /> Report
        </h2>
        
        <hr className="menu-line" />

        <ul>
          <li className="menu-item" onClick={handleDashboardClick}>
            <svg xmlns="http://www.w3.org/2000/svg" className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="3" y1="9" x2="21" y2="9"></line>
              <line x1="9" y1="21" x2="9" y2="9"></line>
            </svg>
            Dashboard
          </li>
          <li className="menu-item">
            <svg xmlns="http://www.w3.org/2000/svg" className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
            Profile
          </li>
          <li className="menu-item">
            <svg xmlns="http://www.w3.org/2000/svg" className="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            Sign Out
          </li>
        </ul>
      </div>
    </div>
  );
};
