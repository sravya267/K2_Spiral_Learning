import React from 'react';
import { Container } from 'react-bootstrap';
import WorksheetForm from './components/WorksheetForm';
import Header from './components/Header';
import Footer from './components/Footer';
import AnimatedBackground from './components/AnimatedBackground';
import './App.css';

function App() {
  return (
    <div className="worksheet-generator">
      <AnimatedBackground />
      <Container>
        <Header />
        <WorksheetForm />
        <Footer />
      </Container>
    </div>
  );
}

export default App;
