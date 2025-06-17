import React, { useState } from 'react';
import { Row, Col, Form, Button, Card } from 'react-bootstrap';
import WorksheetTypeSelector from './WorksheetTypeSelector';
import DifficultySelector from './DifficultySelector';
import ConceptSelector from './ConceptSelector';
import { generateWorksheet, downloadWorksheetPDF } from '../services/api';

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
      // Create request data 
      const requestData = {
        worksheet_type: worksheetType,
        number_range: difficulty, // We'll keep using number_range here since our api.js will handle the mapping
        concepts: selectedConcepts,
        include_answer_key: includeAnswerKey
      };
      
      // Let the api.js function handle all the details
      const pdfBlob = await generateWorksheet(requestData);
      
      // Use the helper function to download
      downloadWorksheetPDF(pdfBlob, `math_worksheet_${worksheetType}_${difficulty}.pdf`);
      
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
              <div className="step-content worksheet-type-step">
                <h3 className="step-title">Choose Worksheet Type</h3>
                <WorksheetTypeSelector 
                  worksheetType={worksheetType} 
                  setWorksheetType={setWorksheetType} 
                />
              </div>
            </div>
            
            <div className="step">
              <div className="step-number">2</div>
              <div className="step-step-content difficulty-type-step">
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