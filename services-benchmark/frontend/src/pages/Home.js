import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div className="home-container">
      <h2>Benvenuto</h2>
      <p>Seleziona la tua area di competenza:</p>
      <div className="button-group">
        <Link to="/student" className="btn btn-student">
          Area Studenti
        </Link>
        <Link to="/professor" className="btn btn-professor">
          Area Professore
        </Link>
      </div>
    </div>
  );
}

export default Home;