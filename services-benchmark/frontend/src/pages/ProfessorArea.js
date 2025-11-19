import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:5001";

function ProfessorArea() {
  const [activeTab, setActiveTab] = useState('create'); // 'create' o 'view'

  // State per creazione Assignment
  const [newAssign, setNewAssign] = useState({ title: '', description: '', due_date: '' });
  const [msg, setMsg] = useState('');

  // State per lista Submissions
  const [submissions, setSubmissions] = useState([]);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      await axios.post(`${API_BASE}/assignments`, newAssign);
      setMsg('Compito creato con successo!');
      setNewAssign({ title: '', description: '', due_date: '' });
    } catch (error) {
      setMsg('Errore: ' + error.message);
    }
  };

  const fetchSubmissions = async () => {
    try {
      const res = await axios.get(`${API_BASE}/submissions`);
      setSubmissions(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  // Carica le submission quando si cambia tab in 'view'
  useEffect(() => {
    if (activeTab === 'view') {
      fetchSubmissions();
    }
  }, [activeTab]);

  return (
    <div className="page-container">
      <h2>Area Professore</h2>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'create' ? 'active' : ''}`}
          onClick={() => setActiveTab('create')}>
          Carica Nuovo Compito
        </button>
        <button
          className={`tab ${activeTab === 'view' ? 'active' : ''}`}
          onClick={() => setActiveTab('view')}>
          Vedi Consegne
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'create' && (
          <div className="create-section">
            <h3>Nuovo Assignment</h3>
            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label>Titolo:</label>
                <input
                  type="text" required
                  value={newAssign.title}
                  onChange={e => setNewAssign({...newAssign, title: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Descrizione:</label>
                <textarea
                  value={newAssign.description}
                  onChange={e => setNewAssign({...newAssign, description: e.target.value})}
                />
              </div>
              <div className="form-group">
                <label>Data Scadenza:</label>
                <input
                  type="date"
                  value={newAssign.due_date}
                  onChange={e => setNewAssign({...newAssign, due_date: e.target.value})}
                />
              </div>
              <button type="submit" className="btn btn-primary">Crea Compito</button>
            </form>
            {msg && <p className="msg">{msg}</p>}
          </div>
        )}

        {activeTab === 'view' && (
          <div className="view-section">
            <h3>Tutte le Consegne Ricevute</h3>
            {submissions.length === 0 ? <p>Nessuna consegna trovata.</p> : (
              <table className="sub-table">
                <thead>
                  <tr>
                    <th>Studente</th>
                    <th>Data Invio</th>
                    <th>ID Assignment</th>
                    <th>Risultato</th>
                  </tr>
                </thead>
                <tbody>
                  {submissions.map(sub => (
                    <tr key={sub._id}>
                      <td>{sub.student_name}</td>
                      <td>{new Date(sub.submitted_at).toLocaleString()}</td>
                      <td>{sub.idAssignment}</td>
                      <td>{sub.result}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default ProfessorArea;