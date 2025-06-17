import React from 'react';
import { Row, Col } from 'react-bootstrap';
import './Header.css'; // Add this import

const Header = () => {
  return (
    <div className="header-container">
      <Row className="align-items-center">
        <Col md={7}>
          <h1 className="main-title" style={{ fontSize: "1.5rem" }}>
            Math Worksheet Generator
            <span className="k2-badge">K-2</span>
          </h1>
          <p className="subtitle" style={{ fontSize: "0.75rem" }}>
            Customize your worksheets to fit your needs. Because the best kind of learning happens when <strong><em style={{ color: "#ff9500" }}>YOU</em></strong> make it your own.
          </p>
        </Col>
        <Col md={5} className="text-center d-none d-md-block">
          <div className="header-image" style={{ height: "80px", overflow: "hidden" }}>
            {/* Animation elements with reduced size */}
            <div className="stick-figure-container" style={{ transform: "scale(0.7)" }}>
              <div className="stick-figure sf-1">
                <div className="head"></div>
                <div className="body"></div>
                <div className="arm left"></div>
                <div className="arm right up"></div>
                <div className="leg left"></div>
                <div className="leg right"></div>
              </div>
              <div className="stick-figure sf-2">
                <div className="head"></div>
                <div className="body"></div>
                <div className="arm left up"></div>
                <div className="arm right up"></div>
                <div className="leg left"></div>
                <div className="leg right jump"></div>
              </div>
              <div className="banner-objects">
                <div className="banner-object symbol-plus">+</div>
                <div className="banner-object symbol-minus">−</div>
                <div className="banner-object symbol-multiply">×</div>
                <div className="banner-object symbol-divide">÷</div>
                <div className="banner-object symbol-equals">=</div>
                <div className="banner-object symbol-percent">%</div>
              </div>
              <div className="math-symbol ms-1">+</div>
              <div className="math-symbol ms-2">−</div>
              <div className="math-symbol ms-3">×</div>
              <div className="math-symbol ms-4">=</div>
            </div>
          </div>
        </Col>
      </Row>
    </div>
  );
};

export default Header;