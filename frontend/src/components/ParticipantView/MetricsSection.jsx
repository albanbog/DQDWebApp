// src/components/ParticipantView/MetricsSection.jsx
import React, { useEffect, useMemo, useState } from 'react';
import { ChevronRight, Check, Info } from 'lucide-react'; // Import the icon
import '../../styles/ParticipantView/MetricsSection.css';

const MetricsSection = ({ selectedGauge }) => {
  const [selectedDomain, setSelectedDomain] = useState('');
  const [activeMetric, setActiveMetric] = useState(null);
  const [selectedAction, setSelectedAction] = useState('');
  const [showPopup, setShowPopup] = useState(false);

  const domainOptions = useMemo(() => {
    switch (selectedGauge) {
      case 'Integrity':
        return [
          'Structural data set error',
          'Data set combination error',
          'Value format error',
        ];
      case 'Completeness':
        return ['Crude missingness'];
      case 'Consistency':
        return ['Range and value violations', 'Contradictions'];
      case 'Accuracy':
        return ['Unexpected distributions', 'Unexpected associations'];
      default:
        return [];
    }
  }, [selectedGauge]);

  const domainDetails = {
    'Structural data set error': {
      definition: 'The observed structure of a data set differs from the expected structure.',
      popupDescription:
        'There may be expectations about the technical structure of a data set such as the number of data records (e.g. cases, observational units, the rows in a data set), the number of data elements (e.g. variables, the columns in a data set). Deviations from expected data set structures are targeted by the indicators within this domain.',
      metrics: [
        {
          name: 'Unexpected data element count',
          code: 'DQI-1001',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_1_1_2_1.html',
          definition: 'The observed number of data elements does not match the expected number.',
        },
        {
          name: 'Unexpected data record count',
          code: 'DQI-1002',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_1_1_2_2.html',
          definition: 'The observed number of available data records does not match the expected count.',
        },
        {
          name: 'Duplicates',
          code: 'DQI-1003',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_1_1_2_2.html',
          definition: 'The same data elements or data records appear multiple times.',
        },
      ],
    },
    'Data set combination error': {
      definition: 'The observed correspondence between different data sets differs from the expected correspondence.',
      popupDescription:
        'Before the conduct of data quality assessments, information from different files may need to be combined. This may be the merging of different study data sets into a single analysis file for data quality assessments but also the appropriate match between a study data and the related metadata file. Indicators in this domain target the mismatch between different files.',
      metrics: [
        {
          name: 'Data record mismatch',
          code: 'DQI-1004',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_1_1_2_2.html',
          definition: 'Data records across different data sets do not match as expected.',
        },
        {
          name: 'Data element mismatch',
          code: 'DQI-1005',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_1_1_2_4.html',
          definition: 'Data elements across different data sets do not match as expected.',
        },
      ],
    },
    'Value format error': {
      definition: 'The technical representation of data values within a data set does not conform to the expected representation.',
      popupDescription:
        'Value format integrity targets the formatting of data values against a defined reference standard. Study and metadata may be targeted alike. The reference for study data is the corresponding metadata. In case of metadata, the reference standard may be provided by other metadata sets.',
      metrics: [
        {
          name: 'Data type mismatch',
          code: 'DQI-1006',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_1_2_4_1.html',
          definition: 'The observed data type does not match the expected data type.',
        },
        {
          name: 'Inhomogeneous value formats',
          code: 'DQI-1007',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_1_2_4_2.html',
          definition: 'The observed data values have an inhomogeneous format across different data fields.',
        },
        {
          name: 'Uncertain missingness status',
          code: 'DQI-1008',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_1_2_4_3.html',
          definition: 'No or uninformative missing value codes (e.g. NA/./Null…) appear where a qualified missing code is expected.',
        },
      ],
    },
    'Crude missingness': {
      definition: 'Metrics of missing data values that ignore the underlying reasons for missing data.',
      popupDescription:
        'Computations of missing data values in the domain “Crude missingness” treat missing data and value codes without differentiation. This is necessary in the absence of a complete and differentiated user-defined missing coding or in the case of unclear missing codes.',
      metrics: [
        {
          name: 'Missing values',
          code: 'DQI-2001',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_2_1_1_1.html',
          definition: 'Data fields without a measurement value.',
        },
      ],
    },
    'Range and value violations': {
      definition: 'Observed data values do not comply with admissible data values or value ranges.',
      popupDescription: '',
      metrics: [
        {
          name: 'Inadmissible numerical values',
          code: 'DQI-3001',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_1_1_1.html',
          definition: 'Observed numerical data values are not admissible according to the allowed ranges.',
        },
        {
          name: 'Inadmissible time-date values',
          code: 'DQI-3002',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_1_1_2.html',
          definition: 'Observed time date values are not admissible according to the allowed time and date ranges.',
        },
        {
          name: 'Inadmissible categorical values',
          code: 'DQI-3003',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_1_1_3.html',
          definition: 'Observed categorical data values are not admissible according to the allowed categories.',
        },
        {
          name: 'Inadmissible standardized vocabulary',
          code: 'DQI-3004',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_1_1_4.html',
          definition: 'Data values are not admissible according to a reference vocabulary.',
        },
        {
          name: 'Inadmissible precision',
          code: 'DQI-3005',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_1_1_5.html',
          definition: 'The precision of observed numerical data values does not match the expected precision.',
        },
        {
          name: 'Uncertain numerical values',
          code: 'DQI-3006',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_1_3_6.html',
          definition: 'Observed numerical values are uncertain or improbable because they are outside the expected ranges.',
        },
        {
          name: 'Uncertain time-date values',
          code: 'DQI-3007',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_1_3_7.html',
          definition: 'Observed time date values are uncertain or improbable because they are outside the expected ranges.',
        },
      ],
    },
    'Contradictions': {
      definition: 'Observed data values appear in impossible or improbable combinations.',
      popupDescription:
        'Contradictions are mostly investigated within an observational unit, i.e. across measurements within the same participant or patient. Contrary to other indicators of the data quality dimension consistency wherein e.g. violations of specified limits are examined, this indicator should focus on eligible values that have passed checks related to range and value violations.',
      metrics: [
        {
          name: 'Logical contradictions',
          code: 'DQI-3008',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_1_2_1.html',
          definition: 'Different data values appear in impossible combinations.',
        },
        {
          name: 'Empirical contradictions',
          code: 'DQI-3009',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_1_2_1.html',
          definition: 'Different data values appear in seemingly erroneous combinations.',
        },
      ],
    },
    'Unexpected distributions': {
      definition: 'Observed distributional characteristics differ from expected distributional characteristics.',
      popupDescription:
        'Indicators within this domain check observed distributions against reference distributions. Addressed aspects of distributions are location parameters (e.g. mean, median), scale parameters (the spread of a distribution, e.g. standard deviation) or skewness or kurtosis. Distribution related checks may be applied to any type of numerical variables.',
      metrics: [
        {
          name: 'Univariate outliers',
          code: 'DQI-4001',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_2_1_1.html',
          definition: 'Numerical data values deviate markedly from others in a univariate analysis.',
        },
        {
          name: 'Unexpected location',
          code: 'DQI-4003',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_2_1_3.html',
          definition: 'Observed location parameters differ from the expected location parameter.',
        },
      ],
    },
    'Unexpected associations': {
      definition: 'Observed associations differ from expected associations.',
      popupDescription:
        'Implementations within this domain examine observed associations against reference associations. Reference associations may comprise permissible ranges of associations as well. Furthermore, in case of reliability or validity associated measures, no explicit reference is specified. Rather common Interpretation ranges apply based on the range of these measures.',
      metrics: [
        {
          name: 'Unexpected association direction',
          code: 'DQI-4008',
          link: 'https://dataquality.qihs.uni-greifswald.de/PDQC_DQ_3_2_2_2.html',
          definition: 'The observed direction of an association (e.g. negative, positive) deviates from the expected direction.',
        },
      ],
    },
  };

  const overallScoreDetails = {
    definition: 'The mean score across the 4 dimensions',
    popupDescription: `
      Data quality dimensions
      The following overview illustrates the hierarchy of the data quality taxonomy. It comprises the data quality dimension at the top level.
      To better orient users and to safeguard comparability to other concepts, we distinguish four common data quality dimensions:
      - Integrity targets the formal usability of data for analyses.
      - Data completeness addresses facets of missing data.
      - Data correctness is conceived as (1) consistency, which addresses the degree to which data values are free of convention breaks or contradictions and (2) accuracy, which denotes the degree of agreement between observed and expected distributions or associations.
      
      The ordering of dimensions in our concept reflects a recommended workflow for data quality assessments. Integrity-related indicators are assessed first, followed by completeness and finally correctness-related indicators.
    `,
  };

  const metrics = {
    'Structural data set error': [
      { name: 'Unexpected data elements', issues: 2 },
      { name: 'Unexpected data records', issues: 5 },
      { name: 'Duplicates', issues: 0 },
    ],
    'Data set combination error': [
      { name: 'Data record mismatch', issues: 3 },
      { name: 'Data element mismatch', issues: 0 },
    ],
    'Value format error': [
      { name: 'Data type mismatch', issues: 1 },
      { name: 'Inhomogeneous value formats', issues: 4 },
      { name: 'Uncertain missingness status', issues: 2 },
    ],
    'Crude missingness': [
      {
        name: 'Missing values',
        issues: 7,
        hasActions: true,
      },
    ],
    'Range and value violations': [
      { name: 'Inadmissible numerical values', issues: 2 },
      { name: 'Inadmissible time-date values', issues: 1 },
      { name: 'Inadmissible categorical values', issues: 0 },
      { name: 'Inadmissible standardized vocabulary', issues: 3 },
      { name: 'Inadmissible precision', issues: 1 },
      { name: 'Uncertain numerical values', issues: 4 },
      { name: 'Uncertain time-date values', issues: 0 },
    ],
    Contradictions: [
      { name: 'Logical contradictions', issues: 1 },
      { name: 'Empirical contradictions', issues: 0 },
    ],
    'Unexpected distributions': [
      { name: 'Univariate outlier', issues: 3 },
      { name: 'Unexpected location', issues: 2 },
    ],
    'Unexpected associations': [
      { name: 'Unexpected association direction', issues: 1 },
    ],
  };

  useEffect(() => {
    if (domainOptions.length > 0) {
      setSelectedDomain(domainOptions[0]);
    }
    setActiveMetric(null);
    setSelectedAction('');
    setShowPopup(false); // Close the popup when changing the dimension
  }, [domainOptions]);

  const handleDomainChange = (domain) => {
    setSelectedDomain(domain);
    setActiveMetric(null);
    setSelectedAction('');
    setShowPopup(false); // Close the popup when changing domains
  };

  const handleMetricClick = (metric) => {
    if (metric.hasActions) {
      setActiveMetric((prev) => (prev === metric.name ? null : metric.name));
    } else {
      setActiveMetric(null);
    }
  };

  const handleActionClick = (action) => {
    setSelectedAction(action);
  };

  const handleApplyChanges = () => {
    setActiveMetric(null);
    setSelectedAction('');
  };

  const handleDiscardChanges = () => {
    setActiveMetric(null);
    setSelectedAction('');
  };

  const togglePopup = () => {
    setShowPopup(!showPopup);
  };

  return (
    <div className="metrics-section">
      {/* Only show domains if not "Overall Score" */}
      {selectedGauge !== 'Overall Score' && (
        <div className="domains">
          {domainOptions.map((domain) => (
            <div
              key={domain}
              className={`domain-button ${selectedDomain === domain ? 'active' : ''}`}
              onClick={() => handleDomainChange(domain)}
            >
              {domain}
            </div>
          ))}
        </div>
      )}

      {/* Metrics Info Box */}
      <div className="metrics-info-box">
        <span className="info-text">
          {selectedGauge === 'Overall Score'
            ? overallScoreDetails.definition
            : domainDetails[selectedDomain]?.definition || 'Metrics Information'}
        </span>
        <Info className="info-icon" size={24} onClick={togglePopup} />
        {showPopup && (
          <div className="metrics-info-popup">
            <h3>{selectedGauge === 'Overall Score' ? 'Overall Score Details' : `${selectedDomain} Details`}</h3>
            <p>
              {selectedGauge === 'Overall Score'
                ? overallScoreDetails.popupDescription
                : domainDetails[selectedDomain]?.popupDescription}
            </p>
            {selectedGauge !== 'Overall Score' && (
              <ul>
                {domainDetails[selectedDomain]?.metrics.map((metric) => (
                  <li key={metric.code}>
                    <a href={metric.link} target="_blank" rel="noopener noreferrer">
                      {metric.name} ({metric.code})
                    </a>
                    : {metric.definition}
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>

      {/* Hide the metrics menu for "Overall Score" */}
      {selectedGauge !== 'Overall Score' && (
        <div className="metrics-menu">
          {selectedDomain &&
            metrics[selectedDomain]?.map((metric) => (
              <div
                key={metric.name}
                className="metric-item"
                onClick={() => handleMetricClick(metric)}
              >
                <div className="metric-text">
                  <span className="metric-name">{metric.name}</span>
                  <span className={`metric-issues ${metric.issues > 0 ? 'clickable' : ''}`}>
                    {metric.issues} {metric.issues === 1 ? 'issue' : 'issues'} found
                  </span>
                </div>
                {metric.hasActions && <ChevronRight className="expand-icon" size={24} />}
              </div>
            ))}
        </div>
      )}

      {activeMetric === 'Missing values' && (
        <div className="actions-menu">
          {['LOCF', 'NOCB', 'Linear Interpolation', 'TS Model Imputation'].map((action) => (
            <div
              key={action}
              className={`action-item ${selectedAction === action ? 'selected' : ''}`}
              onClick={() => handleActionClick(action)}
            >
              {action}
              {selectedAction === action && <Check className="action-tick" size={16} />}
            </div>
          ))}
        </div>
      )}

      {selectedGauge !== 'Overall Score' && (
        <div className="buttons">
          <button className="discard-button" onClick={handleDiscardChanges}>
            Discard
          </button>
          <button className="save-button" onClick={handleApplyChanges}>
            Apply changes
          </button>
        </div>
      )}
    </div>
  );
};

export default MetricsSection;
