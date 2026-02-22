import { useState } from 'react';
import { FilterBox } from '../shared/FilterBox';
import { TypeInput } from '../shared/TypeInput';
import '../shared/SearchForm.css';
import './CoverageAnalyzerSearch.css';

interface SlotState {
  enabled: boolean;
  type1: string;
  type2: string;
}

function emptySlot(): SlotState {
  return { enabled: false, type1: '', type2: '' };
}

interface CoverageAnalyzerSearchProps {
  onSearch: (slots: string[]) => void;
  onError: (msg: string) => void;
  lastSlots: string[] | null;
}

export function CoverageAnalyzerSearch({ onSearch, onError, lastSlots }: CoverageAnalyzerSearchProps) {
  const [slots, setSlots] = useState<SlotState[]>(Array.from({ length: 6 }, emptySlot));

  function updateSlot(index: number, patch: Partial<SlotState>) {
    setSlots(prev => prev.map((s, i) => (i === index ? { ...s, ...patch } : s)));
  }

  function handleSubmit() {
    const active = slots
      .filter(s => s.enabled && s.type1.trim())
      .map(s => {
        const t1 = s.type1.trim().toLowerCase();
        const t2 = s.type2.trim().toLowerCase();
        return t2 ? `${t1}-${t2}` : t1;
      });

    if (active.length === 0) {
      onError('Enable at least one slot and enter a type.');
      return;
    }

    const key = JSON.stringify(active);
    const lastKey = lastSlots ? JSON.stringify(lastSlots) : null;
    if (key === lastKey) {
      onError('Request not sent: Search parameters unchanged.');
      return;
    }

    onSearch(active);
  }

  return (
    <div className="ca-search">
      {slots.map((slot, i) => (
        <FilterBox key={i} title={`slot ${i + 1}`}>
          <label className="toggle-row">
            <input
              type="checkbox"
              checked={slot.enabled}
              onChange={e => updateSlot(i, { enabled: e.target.checked })}
            />
            enabled
          </label>
          <div className="input-row">
            <label htmlFor={`slot-${i}-type1`}>type 1</label>
            <TypeInput
              id={`slot-${i}-type1`}
              value={slot.type1}
              onChange={v => updateSlot(i, { type1: v })}
              disabled={!slot.enabled}
            />
          </div>
          <div className="input-row">
            <label htmlFor={`slot-${i}-type2`}>type 2</label>
            <TypeInput
              id={`slot-${i}-type2`}
              value={slot.type2}
              onChange={v => updateSlot(i, { type2: v })}
              disabled={!slot.enabled}
            />
          </div>
        </FilterBox>
      ))}

      <button className="go-button" onClick={handleSubmit}>
        Scan coverage
      </button>
    </div>
  );
}
