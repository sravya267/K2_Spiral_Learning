import React, { useState } from 'react';
import { Row, Col, Form, Button, Card } from 'react-bootstrap';
import WorksheetTypeSelector from './WorksheetTypeSelector';
import DifficultySelector from './DifficultySelector';
import ConceptSelector from './ConceptSelector';

const WorksheetForm = () => {
  const [worksheetType, setWorksheetType] = useState('spiral');
  const [difficulty, setDifficulty] = useState('beginner');
  const [selectedConcepts, setSelectedConcepts] = useState([]);
  const [includeAnswerKey, setIncludeAnswerKey] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (selectedConcepts.length === 0) {
      alert('Please select at least one math concept');
      return;
    }
    
    if (worksheetType === 'fluency' && selectedConcepts.length > 1) {
      alert('Fluency Practice mode allows only one concept. Please select only one concept.');
      return;
    }
    
    setIsGenerating(true);
    
    try {
      // Use API format that matches your backend
      const response = await fetch('/api/generate-worksheet', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          worksheet_type: worksheetType,
          difficulty: difficulty,
          concepts: selectedConcepts,
          include_answer_key: includeAnswerKey,
          question_count: 15 // Default value
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate worksheet');
      }
      
      const data = await response.json();
      
      // Download the file using the URL from the response
      window.location.href = data.download_url;
      
    } catch (error) {
      console.error('Error generating worksheet:', error);
      alert('Error connecting to server. Please try again later.');
    } finally {
      setIsGenerating(false);
    }
  };
  
  return (
    <Card className="form-card">
      <Card.Body>
        <Form id="worksheetForm" onSubmit={handleSubmit}>
          <div className="form-steps">
            <div className="step">
              <div className="step-number">1</div>
              <div className="step-content">
                <h3 className="step-title">Choose Worksheet Type</h3>
                <WorksheetTypeSelector 
                  worksheetType={worksheetType} 
                  setWorksheetType={setWorksheetType} 
                />
              </div>
            </div>
            
            <div className="step">
              <div className="step-number">2</div>
              <div className="step-content">
                <h3 className="step-title">Select Difficulty Level</h3>
                <DifficultySelector 
                  difficulty={difficulty} 
                  setDifficulty={setDifficulty} 
                />
              </div>
            </div>
            
            <div className="step">
              <div className="step-number">3</div>
              <div className="step-content">
                <h3 className="step-title">Choose Math Concepts</h3>
                <ConceptSelector 
                  selectedConcepts={selectedConcepts}
                  setSelectedConcepts={setSelectedConcepts}
                  worksheetType={worksheetType}
                />
              </div>
            </div>
          </div>
          
          <div className="form-footer">
            <div className="answer-key-toggle">
              <Form.Check
                type="switch"
                id="includeAnswerKey"
                checked={includeAnswerKey}
                onChange={(e) => setIncludeAnswerKey(e.target.checked)}
                label="Include Answer Key"
              />
            </div>
            
            <Button 
              type="submit" 
              className="generate-btn"
              disabled={isGenerating}
            >
              {isGenerating ? (
                <>
                  <span className="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Generating...
                </>
              ) : (
                <>
                  <i className="fas fa-file-download me-2"></i>
                  Generate Worksheet
                </>
              )}
            </Button>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default WorksheetForm;
