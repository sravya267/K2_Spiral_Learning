import React from 'react';
import { Form } from 'react-bootstrap';
import './WorksheetTypeSelector.css';

const WorksheetTypeSelector = ({ worksheetType, setWorksheetType }) => {
  const worksheetTypes = [
    { 
      id: 'spiral', 
      label: 'Spiral Review', 
      icon: 'sync',
      description: 'Mixed topics, one question per subtopic'
    },
    { 
      id: 'fluency', 
      label: 'Fluency Sheet', 
      icon: 'tachometer-alt',
      description: 'Single concept, timed, max 15 questions'
    }
  ];
  
  return (
    <div className="worksheet-type-selector-wrapper">
      <div className="worksheet-type-card-container">
        {worksheetTypes.map(option => (
          <div 
            key={option.id}
            className={`worksheet-type-card-option ${worksheetType === option.id ? 'selected' : ''}`}
            onClick={() => setWorksheetType(option.id)}
          >
            <Form.Check
              type="radio"
              name="worksheetType"
              id={option.id}
              value={option.id}
              checked={worksheetType === option.id}
              onChange={() => setWorksheetType(option.id)}
              className="visually-hidden"
            />
            <div className="option-header">
              <div className="option-icon">
                <i className={`fas fa-${option.icon}`}></i>
              </div>
              <h4 className="option-title">{option.label}</h4>
              {worksheetType === option.id && (
                <div className="selected-mark">
                  <i className="fas fa-check-circle"></i>
                </div>
              )}
            </div>
            <div className="option-description">
              {option.description}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default WorksheetTypeSelector;