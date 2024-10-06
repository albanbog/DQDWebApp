/* App.jsx */
import React from 'react';
import './App.css'; // Import your CSS
import { SidebarMenu } from './components/SidebarMenu'; // SidebarMenu component
import { SearchBar } from './components/SearchBar'; // SearchBar component
import { ProfileSection } from './components/ProfileSection'; // Profile Section component
import { ReportsList } from './components/ReportsList'; // ReportsList component

function App() {
  return (
    <div className="app-container">
      
      {/* Logo is outside and isolated from other components */}
      <div className="logo-container">
        <img src="/smartNTx-logo.png" alt="Logo" className="logo" />
      </div>
      
      {/* SidebarMenu component */}
      <aside className="sidebar">
        <SidebarMenu />
      </aside>
      
      {/* Main content */}
      <main className="main-content">
        <SearchBar />
        <div className="profile-section-wrapper">
          <ProfileSection />
        </div>
        
        <section className="reports-section">
          <ReportsList />
        </section>
      </main>
    </div>
  );
}

export default App;
