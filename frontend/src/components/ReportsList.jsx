import React, { useState } from 'react';
import '../styles/ReportsList.css';

export const ReportsList = () => {
  const reportsPerPage = 12;
  const [selectedReports, setSelectedReports] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [sortOption, setSortOption] = useState(0);

  const reports = [
    { id: 'p01', score: 5.86, date: '04/05/2024' },
    { id: 'p01', score: 10.34, date: '03/05/2024' },
    { id: 'p02', score: 35.80, date: '03/05/2024' },
    { id: 'p02', score: 45.80, date: '29/04/2024' },
    { id: 'p03', score: 98.25, date: '29/04/2024' },
    { id: 'p03', score: 80.50, date: '15/04/2024' },
    { id: 'p04', score: 78.84, date: '20/04/2024' },
    { id: 'p04', score: 60.22, date: '10/04/2024' },
    { id: 'p05', score: 100.00, date: '04/04/2024' },
    { id: 'p05', score: 92.10, date: '01/04/2024' },
    { id: 'p06', score: 94.06, date: '01/04/2024' },
    { id: 'p06', score: 89.00, date: '25/03/2024' },
    { id: 'p07', score: 49.09, date: '14/03/2024' },
    { id: 'p07', score: 45.00, date: '10/03/2024' },
    { id: 'p08', score: 90.00, date: '04/05/2024' },
    { id: 'p08', score: 87.50, date: '25/04/2024' },
    { id: 'p09', score: 67.50, date: '05/05/2024' },
    { id: 'p09', score: 55.30, date: '15/04/2024' },
    { id: 'p10', score: 22.35, date: '07/05/2024' },
    { id: 'p10', score: 40.06, date: '04/05/2024' },
    { id: 'p11', score: 56.75, date: '09/05/2024' },
    { id: 'p11', score: 65.90, date: '08/05/2024' },
    { id: 'p12', score: 84.21, date: '10/05/2024' },
    { id: 'p12', score: 70.50, date: '05/05/2024' },
    { id: 'p13', score: 91.75, date: '12/05/2024' },
    { id: 'p13', score: 78.90, date: '10/05/2024' },
    { id: 'p14', score: 29.16, date: '20/04/2024' },
    { id: 'p14', score: 30.45, date: '15/04/2024' },
    { id: 'p15', score: 45.81, date: '21/04/2024' },
    { id: 'p15', score: 60.10, date: '19/04/2024' },
    { id: 'p16', score: 5.86, date: '04/05/2024' },
    { id: 'p16', score: 10.12, date: '02/05/2024' }
  ];

  const totalPages = Math.ceil(reports.length / reportsPerPage);

  const toggleSelectReport = (reportId, reportDate) => {
    const uniqueKey = `${reportId}-${reportDate}`;
    if (selectedReports.includes(uniqueKey)) {
      setSelectedReports(selectedReports.filter((id) => id !== uniqueKey));
    } else {
      setSelectedReports([...selectedReports, uniqueKey]);
    }
  };

  const toggleSelectAll = () => {
    const allVisibleKeys = currentReports.map((report) => `${report.id}-${report.date}`);
    const allSelected = allVisibleKeys.every((key) => selectedReports.includes(key));

    if (allSelected) {
      setSelectedReports(
        selectedReports.filter((key) => !allVisibleKeys.includes(key))
      );
    } else {
      setSelectedReports([...selectedReports, ...allVisibleKeys.filter((key) => !selectedReports.includes(key))]);
    }
  };

  const handlePrevPage = () => {
    setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));
  };

  const handleNextPage = () => {
    setCurrentPage((prevPage) => Math.min(prevPage + 1, totalPages));
  };

  const sortReports = (reports) => {
    const sortedReports = [...reports];
    switch (sortOption) {
      case 0: // Ascending by Date
        return sortedReports.sort((a, b) => new Date(a.date) - new Date(b.date));
      case 1: // Descending by Date
        return sortedReports.sort((a, b) => new Date(b.date) - new Date(a.date));
      case 2: // Ascending by Name
        return sortedReports.sort((a, b) => a.id.localeCompare(b.id));
      case 3: // Descending by Name
        return sortedReports.sort((a, b) => b.id.localeCompare(a.id));
      default:
        return sortedReports;
    }
  };

  const sortedReports = sortReports(reports);
  const startIndex = (currentPage - 1) * reportsPerPage;
  const currentReports = sortedReports.slice(startIndex, startIndex + reportsPerPage);

  const toggleSortOption = () => {
    setSortOption((prevSortOption) => (prevSortOption + 1) % 4);
  };

  // Mock functions for Download and Delete
  const handleDownload = () => {
    alert('Download selected reports');
  };

  const handleDelete = () => {
    alert('Delete selected reports');
  };

  return (
    <div className="reports-list-container">
      <div className="reports-header-section">
        <div className="header-controls">
          <input
            type="checkbox"
            className="select-all-checkbox"
            onChange={toggleSelectAll}
            checked={currentReports.every((report) => selectedReports.includes(`${report.id}-${report.date}`))}
          />
          <div className="sort-icon" onClick={toggleSortOption}>
            <img src="/sort.png" alt="Sort" />
          </div>
          
          {/* Conditionally render Download and Delete buttons */}
          {selectedReports.length > 0 && (
            <div className="action-buttons">
              <button className="download-button" onClick={handleDownload}>
                Download
              </button>
              <button className="delete-button" onClick={handleDelete}>
                Delete
              </button>
            </div>
          )}
        </div>

        <div className="pagination">
          <span>{`${startIndex + 1}-${Math.min(
            startIndex + reportsPerPage,
            reports.length
          )} of ${reports.length}`}</span>
          <div className="pagination-controls">
            <button onClick={handlePrevPage} disabled={currentPage === 1}>❮</button>
            <button onClick={handleNextPage} disabled={currentPage === totalPages}>❯</button>
          </div>
        </div>
      </div>

      <hr className="header-separator-line" />

      <div className="reports-header">
        <div className="checkbox-header"></div>
        <div className="id-header">ID</div>
        <div className="score-header">Overall Score</div>
        <div className="date-header">Date</div>
      </div>

      <div className="reports-list">
        {currentReports.map((report) => (
          <div key={`${report.id}-${report.date}`} className="report-item">
            <div className="checkbox-container">
              <input
                type="checkbox"
                className="report-checkbox"
                checked={selectedReports.includes(`${report.id}-${report.date}`)}
                onChange={() => toggleSelectReport(report.id, report.date)}
              />
            </div>
            <div className="report-bar">
              <div className="id">{report.id}</div>
              <div className="progress-section">
                <div className="progress-bar">
                  <div
                    className="progress"
                    style={{
                      width: `${report.score}%`,
                      backgroundColor:
                        report.score > 66 ? 'green' : report.score > 33 ? 'orange' : 'red',
                    }}
                  ></div>
                </div>
                <div className="percentage">{report.score}%</div>
              </div>
            </div>
            <div className="date">{report.date}</div>
          </div>
        ))}
      </div>
    </div>
  );
};
