import { useState } from 'react';
import { FilterBox } from '../shared/FilterBox';
import { TypeInput } from '../shared/TypeInput';
import type { CandidateFinderParams } from '../../api/types';
import '../shared/SearchForm.css';
import './CandidateFinderSearch.css';

const STAT_OPTIONS = [
  { label: 'attack', value: 'attack' },
  { label: 'defense', value: 'defense' },
  { label: 'special attack', value: 'special_attack' },
  { label: 'special defense', value: 'special_defense' },
  { label: 'speed', value: 'speed' },
];

function parseStatInt(raw: string): number | null {
  if (!raw) return null;
  if (raw.includes('.')) throw new Error(`Expected integer, got float: ${raw}`);
  const n = parseInt(raw, 10);
  if (isNaN(n)) throw new Error('Stat field must be a number between 1 and 255');
  if (n < 1 || n > 255) throw new Error('Stat field must be a number between 1 and 255');
  return n;
}

interface CandidateFinderSearchProps {
  onSearch: (params: CandidateFinderParams) => void;
  onError: (msg: string) => void;
  lastParams: CandidateFinderParams | null;
}

export function CandidateFinderSearch({ onSearch, onError, lastParams }: CandidateFinderSearchProps) {
  const [legendary, setLegendary] = useState(false);
  const [mythical, setMythical] = useState(false);
  const [ultraBeast, setUltraBeast] = useState(false);

  const [moveEnabled, setMoveEnabled] = useState(false);
  const [moveName, setMoveName] = useState('');

  const [statsEnabled, setStatsEnabled] = useState(false);
  const [primaryStat, setPrimaryStat] = useState('');
  const [minPrimary, setMinPrimary] = useState('');
  const [secondaryStat, setSecondaryStat] = useState('');
  const [minSecondary, setMinSecondary] = useState('');
  const [minSpeed, setMinSpeed] = useState('');

  const [typeEnabled, setTypeEnabled] = useState(false);
  const [type1, setType1] = useState('');
  const [type2, setType2] = useState('');

  function handleSubmit() {
    try {
      const params: CandidateFinderParams = {
        include_legendary: legendary,
        include_mythical: mythical,
        include_ultra_beasts: ultraBeast,
      };

      if (moveEnabled && moveName) {
        params.move = moveName.toLowerCase().replace(/ /g, '_');
      }

      if (statsEnabled) {
        if (primaryStat && !secondaryStat) {
          onError('Select a secondary stat.');
          return;
        }
        if (secondaryStat && !primaryStat) {
          onError('Select a primary stat.');
          return;
        }
        if (primaryStat) params.primary_stat = primaryStat;
        if (secondaryStat) params.secondary_stat = secondaryStat;
        const mp = parseStatInt(minPrimary);
        const ms = parseStatInt(minSecondary);
        const msp = parseStatInt(minSpeed);
        if (mp != null) params.min_primary = mp;
        if (ms != null) params.min_secondary = ms;
        if (msp != null) params.min_speed = msp;
      }

      if (typeEnabled && type1) {
        params.desired_type = type2 ? `${type1}-${type2}` : type1;
      }

      const key = JSON.stringify(params);
      const lastKey = lastParams ? JSON.stringify(lastParams) : null;
      if (key === lastKey) {
        onError('Request not sent: Search parameters unchanged.');
        return;
      }

      onSearch(params);
    } catch (e) {
      onError((e as Error).message);
    }
  }

  return (
    <div className="cf-search">
      <FilterBox title="special pokemon">
        <label className="toggle-row">
          <input type="checkbox" checked={legendary} onChange={e => setLegendary(e.target.checked)} />
          legendary
        </label>
        <label className="toggle-row">
          <input type="checkbox" checked={mythical} onChange={e => setMythical(e.target.checked)} />
          mythical
        </label>
        <label className="toggle-row">
          <input type="checkbox" checked={ultraBeast} onChange={e => setUltraBeast(e.target.checked)} />
          ultra beast
        </label>
      </FilterBox>

      <FilterBox title="move">
        <label className="toggle-row">
          <input type="checkbox" checked={moveEnabled} onChange={e => setMoveEnabled(e.target.checked)} />
          enabled
        </label>
        <div className="input-row">
          <label htmlFor="move-input">move name</label>
          <input
            id="move-input"
            className="text-input"
            value={moveName}
            onChange={e => setMoveName(e.target.value)}
            disabled={!moveEnabled}
          />
        </div>
      </FilterBox>

      <FilterBox title="stats">
        <label className="toggle-row">
          <input type="checkbox" checked={statsEnabled} onChange={e => setStatsEnabled(e.target.checked)} />
          enabled
        </label>
        <FilterBox title="primary stat">
          <div className="input-row">
            <label htmlFor="primary-stat">stat name</label>
            <select
              id="primary-stat"
              className="stat-select"
              value={primaryStat}
              onChange={e => setPrimaryStat(e.target.value)}
              disabled={!statsEnabled}
            >
              <option value="">select stat</option>
              {STAT_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>
          <div className="input-row">
            <label htmlFor="min-primary">minimum value</label>
            <input
              id="min-primary"
              className="text-input narrow"
              value={minPrimary}
              onChange={e => setMinPrimary(e.target.value)}
              disabled={!statsEnabled}
            />
          </div>
        </FilterBox>
        <FilterBox title="secondary stat">
          <div className="input-row">
            <label htmlFor="secondary-stat">stat name</label>
            <select
              id="secondary-stat"
              className="stat-select"
              value={secondaryStat}
              onChange={e => setSecondaryStat(e.target.value)}
              disabled={!statsEnabled}
            >
              <option value="">select stat</option>
              {STAT_OPTIONS.map(o => <option key={o.value} value={o.value}>{o.label}</option>)}
            </select>
          </div>
          <div className="input-row">
            <label htmlFor="min-secondary">minimum value</label>
            <input
              id="min-secondary"
              className="text-input narrow"
              value={minSecondary}
              onChange={e => setMinSecondary(e.target.value)}
              disabled={!statsEnabled}
            />
          </div>
        </FilterBox>
        <FilterBox title="desired speed (optional)">
          <div className="input-row">
            <label htmlFor="min-speed">minimum value</label>
            <input
              id="min-speed"
              className="text-input narrow"
              value={minSpeed}
              onChange={e => setMinSpeed(e.target.value)}
              disabled={!statsEnabled}
            />
          </div>
        </FilterBox>
      </FilterBox>

      <FilterBox title="desired type">
        <label className="toggle-row">
          <input type="checkbox" checked={typeEnabled} onChange={e => setTypeEnabled(e.target.checked)} />
          enabled
        </label>
        <div className="input-row">
          <label htmlFor="type1">type 1</label>
          <TypeInput id="type1" value={type1} onChange={setType1} disabled={!typeEnabled} />
        </div>
        <div className="input-row">
          <label htmlFor="type2">type 2</label>
          <TypeInput id="type2" value={type2} onChange={setType2} disabled={!typeEnabled} />
        </div>
      </FilterBox>

      <button className="go-button" onClick={handleSubmit}>
        Catch 'em all!
      </button>
    </div>
  );
}
