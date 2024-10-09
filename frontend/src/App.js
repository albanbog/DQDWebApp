// src/App.jsx
import React, { useState } from 'react';
import './App.css';
import { SidebarMenu } from './components/HomePage/SidebarMenu';
import { SearchBar } from './components/HomePage/SearchBar';
import { ProfileSection } from './components/HomePage/ProfileSection';
import { ReportsList } from './components/HomePage/ReportsList';
import ParticipantView from './components/ParticipantView/ParticipantView';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';

function Layout() {
  const [searchQuery, setSearchQuery] = useState('');
  const location = useLocation();

  // Check if the current path is the home page
  const isHomePage = location.pathname === '/';

  return (
    <div className="app-container">
      {isHomePage && (
        <div className="logo-container">
          <img src="/smartNTx-logo.png" alt="Logo" className="logo" />
        </div>
      )}
      
      {isHomePage && (
        <aside className="sidebar">
          <SidebarMenu />
        </aside>
      )}
      
      <main className="main-content">
        {isHomePage && (
          <SearchBar onSearch={setSearchQuery} />
        )}
        {isHomePage && (
          <div className="profile-section-wrapper">
            <ProfileSection />
          </div>
        )}
        
        <section className="reports-section">
          <Routes>
            {/* Default HomePage route */}
            <Route 
              path="/" 
              element={<ReportsList searchQuery={searchQuery} />} 
            />
            
            {/* Add route for ParticipantView */}
            <Route 
              path="/participant-view" 
              element={<ParticipantView />} 
            />
          </Routes>
        </section>
      </main>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Layout />
    </Router>
  );
}

export default App;
