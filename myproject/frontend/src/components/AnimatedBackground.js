import React from 'react';

const AnimatedBackground = () => {
  return (
    <div className="animated-background">
      {/* Sun and rays */}
      <div className="sun">
        <div className="ray ray-1"></div>
        <div className="ray ray-2"></div>
        <div className="ray ray-3"></div>
        <div className="ray ray-4"></div>
        <div className="ray ray-5"></div>
        <div className="ray ray-6"></div>
        <div className="ray ray-7"></div>
        <div className="ray ray-8"></div>
      </div>

      {/* Paper Airplanes */}
      <div className="paper-plane plane-1">
        <div className="plane-body"></div>
      </div>
      <div className="paper-plane plane-2">
        <div className="plane-body"></div>
      </div>

      {/* Floating Math Symbols */}
      <div className="math-symbol symbol-plus">+</div>
      <div className="math-symbol symbol-minus">−</div>
      <div className="math-symbol symbol-multiply">×</div>
      <div className="math-symbol symbol-divide">÷</div>
      <div className="math-symbol symbol-equals">=</div>
      <div className="math-symbol symbol-percent">%</div>

      {/* Kid's Handwriting */}
      <div className="handwriting hw-1">2+2=4</div>
      <div className="handwriting hw-2">7-3=4</div>
      <div className="handwriting hw-3">5×2=10</div>

      {/* Simple Pencil */}
      <div className="pencil">
        <div className="pencil-body"></div>
        <div className="pencil-tip"></div>
        <div className="pencil-eraser"></div>
      </div>

      {/* Simple Calculator */}
      <div className="calculator">
        <div className="calc-screen"></div>
        <div className="calc-buttons"></div>
      </div>
    </div>
  );
};

export default AnimatedBackground;
