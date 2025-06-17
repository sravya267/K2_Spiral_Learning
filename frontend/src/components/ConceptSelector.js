import React, { useState, useEffect } from 'react';
import { Button, Row, Col } from 'react-bootstrap';
import { fetchConcepts } from '../services/api'; // Import from API service

const ConceptSelector = ({ selectedConcepts, setSelectedConcepts, worksheetType }) => {
  const [concepts, setConcepts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [apiStatus, setApiStatus] = useState('loading');

  // Predefined list of all concepts
  const allConcepts = [
    { id: 'number_sense', name: 'Number Sense', icon: '#' },
    { id: 'addition', name: 'Addition', icon: '+' },
    { id: 'subtraction', name: 'Subtraction', icon: '−' },
    { id: 'time_telling', name: 'Time Telling', icon: '🕒' },
    { id: 'money_counting', name: 'Money', icon: '💰' },
    { id: 'place_value', name: 'Place Value', icon: '1️⃣' },
    { id: 'word_problems', name: 'Word Problems', icon: '📝' },
    { id: 'shapes', name: 'Shapes', icon: '⭐' },
    { id: 'skip_counting', name: 'Skip Counting', icon: '2️⃣' },
    { id: 'fractions', name: 'Fractions', icon: '½' },
    { id: 'measurement', name: 'Measurement', icon: '📏' },
    { id: 'patterns_algebra', name: 'Patterns & Algebra', icon: '🔄' },
    { id: 'graphing_data', name: 'Graphing & Data', icon: '📊' },
    { id: 'odd_even', name: 'Odd & Even', icon: '🔢' }
  ];

  useEffect(() => {
    const loadConcepts = async () => {
      try {
        console.log('Fetching concepts using API service');
        const data = await fetchConcepts();
        console.log('API response:', data);
        
        // Check if we got a valid response with categories
        if (data && Object.keys(data).length > 0) {
          setConcepts(data);
          setApiStatus('api_success');
          console.log('Successfully loaded concepts from API');
        } else {
          console.warn('API returned empty data, using fallback');
          setConcepts(allConcepts);
          setApiStatus('fallback');
        }
      } catch (error) {
        console.error('Error fetching concepts:', error);
        setConcepts(allConcepts);
        setApiStatus('api_error');
      } finally {
        setLoading(false);
      }
    };

    loadConcepts();
  }, []);

  // Added handleConceptToggle function
  const handleConceptToggle = (conceptId) => {
    // In fluency mode, we only allow one selection
    if (worksheetType === 'fluency') {
      setSelectedConcepts([conceptId]);
      return;
    }

    // In spiral mode, toggle the selection
    setSelectedConcepts(prev =>
      prev.includes(conceptId)
        ? prev.filter(id => id !== conceptId)
        : [...prev, conceptId]
    );
  };

  const selectAll = () => {
    if (worksheetType === 'fluency') {
      alert('Fluency Practice mode allows only one concept. Please select concepts individually.');
      return;
    }

    // Use allConcepts to select all concepts
    const allConceptIds = allConcepts.map(concept => concept.id);
    console.log('Selecting All Concepts:', allConceptIds);

    setSelectedConcepts(allConceptIds);
  };

  const deselectAll = () => {
    setSelectedConcepts([]);
  };

  if (loading) {
    return <div>Loading math concepts...</div>;
  }

  return (
    <div>
      <div className="concept-header">
        <div className="concept-buttons">
          <Button
            variant="outline-primary"
            size="sm"
            className="select-btn me-2"
            onClick={selectAll}
          >
            <i className="fas fa-check-double me-1"></i> Select All
          </Button>
          <Button
            variant="outline-secondary"
            size="sm"
            className="select-btn"
            onClick={deselectAll}
          >
            <i className="fas fa-times me-1"></i> Deselect All
          </Button>
        </div>
      </div>

      {apiStatus !== 'api_success' && (
        <div style={{
          marginBottom: '10px',
          padding: '8px',
          background: '#fff3cd',
          color: '#856404',
          borderRadius: '4px'
        }}>
          Concepts loaded from local configuration
        </div>
      )}

      <Row className="concept-grid g-2">
        {allConcepts.map(concept => (
          <Col xs={6} sm={4} md={3} key={concept.id}>
            <div
              className={`concept-chip ${selectedConcepts.includes(concept.id) ? 'selected' : ''}`}
              onClick={() => handleConceptToggle(concept.id)}
            >
              <div className="concept-icon">
                {concept.icon}
              </div>
              <div className="concept-label">{concept.name}</div>
              {selectedConcepts.includes(concept.id) && (
                <div className="concept-check">
                  <i className="fas fa-check"></i>
                </div>
              )}
            </div>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default ConceptSelector;