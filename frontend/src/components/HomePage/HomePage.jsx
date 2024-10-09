 
// src/components/HomePage/HomePage.jsx
import React, { useState } from 'react';
import { SidebarMenu } from './SidebarMenu';
import { SearchBar } from './SearchBar';
import { ProfileSection } from './ProfileSection';
import { ReportsList } from './ReportsList';
import '../../styles/HomePage/HomePage.css';

const HomePage = () => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="home-page">
      <div className="logo-container">
        <img src="/smartNTx-logo.png" alt="SmartNTx Logo" className="logo" />
      </div>
      
      <aside className="sidebar">
        <SidebarMenu />
      </aside>
      
      <main className="main-content">
        <SearchBar onSearch={setSearchQuery} />
        <div className="profile-section-wrapper">
          <ProfileSection />
        </div>
        
        <section className="reports-section">
          <ReportsList searchQuery={searchQuery} />
        </section>
      </main>
    </div>
  );
};

export default HomePage;
