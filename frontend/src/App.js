/* App.jsx */
import React, { useState } from 'react';
import './App.css';
import { SidebarMenu } from './components/SidebarMenu';
import { SearchBar } from './components/SearchBar';
import { ProfileSection } from './components/ProfileSection';
import { ReportsList } from './components/ReportsList';

function App() {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="app-container">
      <div className="logo-container">
        <img src="/smartNTx-logo.png" alt="Logo" className="logo" />
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
}

export default App;
