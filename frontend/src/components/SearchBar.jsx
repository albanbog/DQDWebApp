import React, { useState } from 'react';
import '../styles/SearchBar.css';

export const SearchBar = ({ onSearch }) => {
  const [inputValue, setInputValue] = useState('');

  const handleSearch = () => {
    onSearch(inputValue);
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="search-bar">
      <input
        type="text"
        placeholder="Search participants reports by their IDs"
        value={inputValue}
        onChange={(e) => setInputValue(e.target.value)}
        onKeyPress={handleKeyPress}
      />
      <img
        src="/search.png"
        alt="Search Icon"
        className="search-icon"
        onClick={handleSearch}
        style={{ cursor: 'pointer' }} // Ensure the icon is clickable
      />
    </div>
  );
};
