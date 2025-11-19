import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:5001";

function StudentArea() {
  const [assignments, setAssignments] = useState([]);
  const [selectedAssignment, setSelectedAssignment] = useState(null);
  const [formData, setFormData] = useState({ student_name: '', result: '' });
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchAssignments();
  }, []);

  const fetchAssignments = async () => {
    try {
      const res = await axios.get(`${API_BASE}/assignments`);
      setAssignments(res.data);
    } catch (error) {
      console.error("Errore fetch assignments", error);
    }
  };

  const handleOpenSubmit = (assignment) => {
    setSelectedAssignment(assignment);
    setMessage('');
    setFormData({ student_name: '', result: '' });
  };

  const handleSubmit = async (e) => {
  e.preventDefault();
  if (!selectedAssignment) return;

  // --- FIX INIZIO ---
  // MongoDB a volte restituisce _id come stringa "123..."
  // e a volte come oggetto { "$oid": "123..." } a seconda del serializer usato.
  // Questo controllo gestisce entrambi i casi.
  let assignmentId = selectedAssignment._id;

  if (typeof assignmentId === 'object' && assignmentId !== null && assignmentId.$oid) {
      assignmentId = assignmentId.$oid;
  }

  console.log("Invio submit per ID:", assignmentId); // Debug in console del browser
  // --- FIX FINE ---

  try {
    // Usiamo la variabile assignmentId pulita invece di selectedAssignment._id direttamente
    await axios.post(`${API_BASE}/assignments/${assignmentId}/submit`, formData);

    setMessage('Compito inviato con successo!');
    setTimeout(() => {
      setSelectedAssignment(null);
      setMessage('');
    }, 2000);
  } catch (error) {
    console.error("Errore invio:", error);
    setMessage('Errore durante l\'invio: ' + (error.response?.data?.error || error.message));
  }
};

  return (
    <div className="page-container">
      <h2>Area Studente</h2>
      <p>Ecco i compiti disponibili:</p>

      <div className="assignments-list">
        {assignments.map(ass => (
          <div key={ass._id} className="card">
            <h3>{ass.title}</h3>
            <p>{ass.description}</p>
            <small>Scadenza: {ass.due_date || 'N/A'}</small>
            <button onClick={() => handleOpenSubmit(ass)} className="btn btn-primary">
              Consegna
            </button>
          </div>
        ))}
      </div>

      {/* Modale o Form di Consegna */}
      {selectedAssignment && (
        <div className="modal-overlay">
          <div className="modal">
            <h3>Consegna per: {selectedAssignment.title}</h3>
            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label>Nome e Cognome:</label>
                <input
                  type="text"
                  required
                  value={formData.student_name}
                  onChange={e => setFormData({...formData, student_name: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Risultato / Testo Compito:</label>
                <textarea
                  required
                  value={formData.result}
                  onChange={e => setFormData({...formData, result: e.target.value})}
                />
              </div>
              <button type="submit" className="btn btn-success">Invia</button>
              <button type="button" className="btn btn-secondary" onClick={() => setSelectedAssignment(null)}>Annulla</button>
            </form>
            {message && <p className="msg">{message}</p>}
          </div>
        </div>
      )}
    </div>
  );
}

export default StudentArea;