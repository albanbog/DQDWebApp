import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import '../../styles/HomePage/ReportsList.css';

export const ReportsList = ({ searchQuery }) => {
  const reportsPerPage = 12;
  const [selectedReports, setSelectedReports] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [sortOption, setSortOption] = useState(0); // 0: date asc, 1: date desc, 2: name asc, 3: name desc
  const navigate = useNavigate();

  const initialReports = useMemo(() => [
    { id: 'p01', score: 5.86, date: '04/05/2024' },
    { id: 'p01', score: 15.32, date: '11/05/2024' },
    { id: 'p02', score: 90.00, date: '04/05/2024' },
    { id: 'p02', score: 92.50, date: '18/05/2024' },
    { id: 'p03', score: 35.80, date: '03/05/2024' },
    { id: 'p04', score: 98.25, date: '29/04/2024' },
    { id: 'p04', score: 99.00, date: '13/05/2024' },
    { id: 'p05', score: 94.06, date: '01/04/2024' },
    { id: 'p06', score: 45.81, date: '21/04/2024' },
    { id: 'p06', score: 52.30, date: '07/05/2024' },
    { id: 'p07', score: 93.18, date: '16/03/2024' },
    { id: 'p08', score: 67.50, date: '05/05/2024' },
    { id: 'p09', score: 34.25, date: '23/03/2024' },
    { id: 'p09', score: 41.75, date: '20/04/2024' },
    { id: 'p10', score: 40.06, date: '04/05/2024' },
    { id: 'p11', score: 49.09, date: '14/03/2024' },
    { id: 'p11', score: 55.62, date: '28/04/2024' },
    { id: 'p12', score: 100.00, date: '04/04/2024' },
    { id: 'p13', score: 22.35, date: '07/05/2024' },
    { id: 'p14', score: 78.84, date: '20/04/2024' },
    { id: 'p14', score: 82.91, date: '15/05/2024' },
    { id: 'p15', score: 56.75, date: '09/05/2024' },
    { id: 'p16', score: 29.16, date: '20/04/2024' },
    { id: 'p16', score: 33.50, date: '06/05/2024' },
  ], []);

  const [reports, setReports] = useState(initialReports);

  const sortReports = useCallback(() => {
    let sortedReports = [...initialReports];
    switch (sortOption) {
      case 0: // date ascending
        sortedReports.sort((a, b) => new Date(a.date) - new Date(b.date));
        break;
      case 1: // date descending
        sortedReports.sort((a, b) => new Date(b.date) - new Date(a.date));
        break;
      case 2: // name ascending
        sortedReports.sort((a, b) => a.id.localeCompare(b.id));
        break;
      case 3: // name descending
        sortedReports.sort((a, b) => b.id.localeCompare(a.id));
        break;
      default:
        break;
    }
    setReports(sortedReports);
  }, [sortOption, initialReports]);

  useEffect(() => {
    sortReports();
  }, [sortReports]);

  const handleSort = () => {
    setSortOption((prevOption) => (prevOption + 1) % 4);
  };

  const getSortIcon = () => {
    switch (sortOption) {
      case 0:
        return '↑ Date';
      case 1:
        return '↓ Date';
      case 2:
        return '↑ Name';
      case 3:
        return '↓ Name';
      default:
        return 'Sort';
    }
  };

  // Filter reports based on the search query
  const filteredReports = reports.filter((report) =>
    report.id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const totalPages = Math.ceil(filteredReports.length / reportsPerPage);

  const toggleSelectReport = (reportKey) => {
    if (reportKey === 'all') {
      if (selectedReports.length === filteredReports.length) {
        setSelectedReports([]);
      } else {
        setSelectedReports(filteredReports.map(report => `${report.id}-${report.date}`));
      }
    } else {
      if (selectedReports.includes(reportKey)) {
        setSelectedReports(selectedReports.filter(key => key !== reportKey));
      } else {
        setSelectedReports([...selectedReports, reportKey]);
      }
    }
  };

  const handlePrevPage = () => {
    setCurrentPage((prevPage) => Math.max(prevPage - 1, 1));
  };

  const handleNextPage = () => {
    setCurrentPage((prevPage) => Math.min(prevPage + 1, totalPages));
  };

  const startIndex = (currentPage - 1) * reportsPerPage;
  const currentReports = filteredReports.slice(startIndex, startIndex + reportsPerPage);

  // Function to handle clicking a report item
  const handleReportClick = () => {
    navigate('/participant-view');
  };

  return (
    <div className="reports-list-container">
      <div className="reports-header-section">
        <div className="header-controls">
          <input
            type="checkbox"
            className="select-all-checkbox"
            onChange={() => toggleSelectReport('all')}
            checked={selectedReports.length === filteredReports.length}
          />
          <button className="sort-button" onClick={handleSort}>
            {getSortIcon()}
          </button>
          {selectedReports.length > 0 && (
            <div className="action-buttons">
              <button className="download-button">Download</button>
              <button className="delete-button">Delete</button>
            </div>
          )}
        </div>

        <div className="pagination">
          <span>{`${startIndex + 1}-${Math.min(startIndex + reportsPerPage, filteredReports.length)} of ${filteredReports.length}`}</span>
          <div className="pagination-controls">
            <button onClick={handlePrevPage} disabled={currentPage === 1}>❮</button>
            <button onClick={handleNextPage} disabled={currentPage === totalPages}>❯</button>
          </div>
        </div>
      </div>

      <hr className="header-separator-line" />

      <div className="reports-header">
        <div className="checkbox-header"></div>
        <div className="id-header">Participant ID</div>
        <div className="score-header">Overall Score</div>
        <div className="date-header">Date</div>
      </div>

      {currentReports.length > 0 ? (
        <div className="reports-list">
          {currentReports.map((report) => {
            const reportKey = `${report.id}-${report.date}`;
            return (
              <div
                key={reportKey}
                className="report-item"
                onClick={handleReportClick} // Add the click handler here
              >
                <div className="checkbox-container" onClick={(e) => e.stopPropagation()}>
                  <input
                    type="checkbox"
                    className="report-checkbox"
                    checked={selectedReports.includes(reportKey)}
                    onChange={() => toggleSelectReport(reportKey)}
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
                          backgroundColor: report.score > 66 ? 'green' : report.score > 33 ? 'orange' : 'red',
                        }}
                      ></div>
                    </div>
                    <div className="percentage">{report.score.toFixed(2)}%</div>
                  </div>
                </div>
                <div className="date">{report.date}</div>
              </div>
            );
          })}
        </div>
      ) : (
        <div className="no-reports-found">
          <p>No reports found</p>
        </div>
      )}
    </div>
  );
};
