import React from 'react';
import '../styles/SearchBar.css'; // Search bar-specific styles

export const SearchBar = () => {
  return (
    <div className="search-bar">
      <input type="text" placeholder="Search participants reports by their IDs" />
      <i className="search-icon">🔍</i>
    </div>
  );
};
