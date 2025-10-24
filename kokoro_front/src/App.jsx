import { useState } from 'react';
import axios from 'axios';
import './App.css';

export default function App() {
  const [text, setText] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!text.trim()) return alert('Veuillez entrer du texte.');
    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8000/tts', 
        { text }
      );
      const filename = response.data.audio_file; 
      setAudioUrl(`http://127.0.0.1:8000/${filename}`);
    }
    catch (error) {
      console.error('Erreur lors de la génération de la synthèse vocale:', error);
      alert('Une erreur est survenue lors de la génération de la synthèse vocale.');
    }
    finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1> TTS </h1>
      <textarea
        row="5"
        placeholder="Entrez le texte à synthétiser ici..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <br />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? 'Génération en cours...' : 'Générer la synthèse vocale'}
      </button>

      {audioUrl && (
        <div>
          <audio controls src={audioUrl}> </audio>
          <p>
            <a href={audioUrl} download="audio.wav">
              Télécharger le fichier audio
            </a>
          </p>
        </div>
      )} 
    </div>
  );
}

