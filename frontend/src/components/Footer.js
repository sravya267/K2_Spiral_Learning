import React from 'react';
import { Row, Col } from 'react-bootstrap';

const Footer = () => {
  return (
    <footer className="footer">
      <Row className="align-items-center">
        <Col md={6}>
          <p className="mb-0">© {new Date().getFullYear()} Math Worksheet Generator</p>
        </Col>
        <Col md={6} className="text-md-end">
          <p className="mb-0">
            <small>Made with <span className="text-warning">☀️</span> for passionate educators</small>
          </p>
        </Col>
      </Row>
    </footer>
  );
};

export default Footer;
