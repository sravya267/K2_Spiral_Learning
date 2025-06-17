import React from 'react';
import { Form } from 'react-bootstrap';
import './DifficultySelector.css';

const DifficultySelector = ({ difficulty, setDifficulty }) => {
  const difficulties = [
    { 
      id: 'beginner', 
      label: 'Beginner', 
      icon: 'star',
      description: 'Single-digit numbers, simple concepts'
    },
    { 
      id: 'intermediate', 
      label: 'Intermediate', 
      icon: 'star-half-alt',
      description: 'Double-digit numbers, moderate complexity'
    },
    { 
      id: 'advanced', 
      label: 'Advanced', 
      icon: 'star',
      description: 'Triple-digit numbers, challenging problems'
    }
  ];
  
  return (
    <div className="difficulty-selector-wrapper">
      <div className="difficulty-card-container">
        {difficulties.map(option => (
          <div 
            key={option.id}
            className={`difficulty-card-option ${difficulty === option.id ? 'selected' : ''}`}
            onClick={() => setDifficulty(option.id)}
          >
            <Form.Check
              type="radio"
              name="difficulty"
              id={option.id}
              value={option.id}
              checked={difficulty === option.id}
              onChange={() => setDifficulty(option.id)}
              className="visually-hidden"
            />
            <div className="option-header">
              <div className="option-icon">
                <i className={`fas fa-${option.icon}`}></i>
              </div>
              <h4 className="option-title">{option.label}</h4>
              {difficulty === option.id && (
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

export default DifficultySelector;