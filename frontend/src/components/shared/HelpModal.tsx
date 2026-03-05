import { useEffect } from 'react';

interface HelpModalProps {
  onClose: () => void;
}

export function HelpModal({ onClose }: HelpModalProps) {
  useEffect(() => {
    function handleKey(e: KeyboardEvent) {
      if (e.key === 'Escape') onClose();
    }
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, [onClose]);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={e => e.stopPropagation()}>
        <button className="modal-close" onClick={onClose}>x</button>

        <section className="modal-section">
          <h2>Candidate Finder</h2>
          <p><em>Search for Pokemon matching one or more filters!</em></p>
          <ul>
            <li><span className="modal-label">Move</span>: returns Pokemon that can learn this move</li>
            <li><span className="modal-label">Type</span>: returns Pokemon with that type combination</li>
            <li><span className="modal-label">Stats</span>: returns Pokemon meeting minimum stat thresholds. Both primary and secondary stat are required. Speed is optional.</li>
          </ul>
          <p className="modal-note">(All active filters are applied together!)</p>
          
        </section>

        <section className="modal-section">
          <h2>Type Coverage</h2>
          <p><em>See which types your team is strong and weak against!</em></p>
          <p>Enter types for up to six pokemon:</p>
          <ul>
            <li><span className="modal-label">Strengths</span>: types your team hits super-effectively</li>
            <li><span className="modal-label">Weaknesses</span>: types that are super-effective against your team</li>
          </ul>
        </section>
        <p className="modal-label">Have fun!</p>
      </div>
    </div>
  );
}
