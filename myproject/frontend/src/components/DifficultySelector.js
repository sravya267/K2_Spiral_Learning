import React from 'react';
import { Row, Col, Form, Card } from 'react-bootstrap';

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
    <Row className="g-3">
      {difficulties.map(option => (
        <Col md={4} key={option.id}>
          <Card 
            className={`difficulty-card ${difficulty === option.id ? 'selected' : ''}`}
            onClick={() => setDifficulty(option.id)}
          >
            <Card.Body>
              <Form.Check
                type="radio"
                name="difficulty"
                id={option.id}
                value={option.id}
                checked={difficulty === option.id}
                onChange={() => setDifficulty(option.id)}
                className="visually-hidden"
              />
              <div className="card-icon">
                <i className={`fas fa-${option.icon}`}></i>
              </div>
              <Card.Title>{option.label}</Card.Title>
              <Card.Text>
                {option.description}
              </Card.Text>
              {difficulty === option.id && (
                <div className="selected-checkmark">
                  <i className="fas fa-check-circle"></i>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      ))}
    </Row>
  );
};

export default DifficultySelector;
