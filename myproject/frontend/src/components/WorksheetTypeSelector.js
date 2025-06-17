import React from 'react';
import { Row, Col, Form, Card } from 'react-bootstrap';

const WorksheetTypeSelector = ({ worksheetType, setWorksheetType }) => {
  return (
    <Row className="g-3">
      <Col md={6}>
        <Card 
          className={`worksheet-type-card ${worksheetType === 'spiral' ? 'selected' : ''}`}
          onClick={() => setWorksheetType('spiral')}
        >
          <Card.Body>
            <Form.Check
              type="radio"
              name="worksheet_type"
              id="spiral"
              value="spiral"
              checked={worksheetType === 'spiral'}
              onChange={() => setWorksheetType('spiral')}
              className="visually-hidden"
            />
            <div className="card-icon">
              <i className="fas fa-sync-alt"></i>
            </div>
            <Card.Title>Spiral Review</Card.Title>
            <Card.Text>
              Mix of different concepts for comprehensive learning
            </Card.Text>
            {worksheetType === 'spiral' && (
              <div className="selected-checkmark">
                <i className="fas fa-check-circle"></i>
              </div>
            )}
            <div className="worksheet-visual spiral-visual">
              <div className="visual-item">+</div>
              <div className="visual-item">−</div>
              <div className="visual-item">🕒</div>
              <div className="visual-item">💰</div>
              <div className="visual-item">#</div>
            </div>
          </Card.Body>
        </Card>
      </Col>
      
      <Col md={6}>
        <Card 
          className={`worksheet-type-card ${worksheetType === 'fluency' ? 'selected' : ''}`}
          onClick={() => setWorksheetType('fluency')}
        >
          <Card.Body>
            <Form.Check
              type="radio"
              name="worksheet_type"
              id="fluency"
              value="fluency"
              checked={worksheetType === 'fluency'}
              onChange={() => setWorksheetType('fluency')}
              className="visually-hidden"
            />
            <div className="card-icon">
              <i className="fas fa-bolt"></i>
            </div>
            <Card.Title>Fluency Practice</Card.Title>
            <Card.Text>
              Focus on a single concept for rapid skill development
            </Card.Text>
            {worksheetType === 'fluency' && (
              <div className="selected-checkmark">
                <i className="fas fa-check-circle"></i>
              </div>
            )}
            <div className="worksheet-visual fluency-visual">
              <div className="visual-item">5+3=?</div>
              <div className="visual-item">7+4=?</div>
              <div className="visual-item">9+2=?</div>
            </div>
          </Card.Body>
        </Card>
      </Col>
      
      <Col xs={12}>
        <div className="info-box">
          <div className="info-icon">
            <i className="fas fa-info-circle"></i>
          </div>
          <div className="info-text">
            {worksheetType === 'spiral' 
              ? "Spiral Review includes one problem from each selected concept" 
              : "Fluency Practice allows only one concept selection"}
          </div>
        </div>
      </Col>
    </Row>
  );
};

export default WorksheetTypeSelector;
