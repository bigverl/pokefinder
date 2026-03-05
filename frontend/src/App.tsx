import { useState } from 'react';
import { CandidateFinderSearch } from './components/candidate-finder/CandidateFinderSearch';
import { CandidateFinderResults } from './components/candidate-finder/CandidateFinderResults';
import { CoverageAnalyzerSearch } from './components/coverage-analyzer/CoverageAnalyzerSearch';
import { CoverageAnalyzerResults } from './components/coverage-analyzer/CoverageAnalyzerResults';
import { HelpModal } from './components/shared/HelpModal';
import { searchPokemon, searchTeamCoverage } from './api/client';
import type { CandidateFinderParams, CandidateFinderResponse, CoverageAnalyzerResponse } from './api/types';
import './App.css';

type Feature = 'candidate-finder' | 'coverage-analyzer';

export default function App() {
  const [activeFeature, setActiveFeature] = useState<Feature>('candidate-finder');
  const [helpOpen, setHelpOpen] = useState(false);

  const [cfData, setCfData] = useState<CandidateFinderResponse | null>(null);
  const [cfLastParams, setCfLastParams] = useState<CandidateFinderParams | null>(null);
  const [cfError, setCfError] = useState<string | null>(null);

  const [caData, setCaData] = useState<CoverageAnalyzerResponse | null>(null);
  const [caLastSlots, setCaLastSlots] = useState<string[] | null>(null);
  const [caError, setCaError] = useState<string | null>(null);

  async function handleCandidateSearch(params: CandidateFinderParams) {
    setCfError(null);
    try {
      const data = await searchPokemon(params);
      setCfData(data);
      setCfLastParams(params);
    } catch (e) {
      setCfError((e as Error).message || 'Generic Error: Something very strange happened.');
    }
  }

  async function handleCoverageSearch(slots: string[]) {
    setCaError(null);
    try {
      const data = await searchTeamCoverage(slots);
      setCaData(data);
      setCaLastSlots(slots);
    } catch (e) {
      setCaError((e as Error).message || 'Generic Error: Something very strange happened.');
    }
  }

  return (
    <div className="app">
      {helpOpen && <HelpModal onClose={() => setHelpOpen(false)} />}
      <div className="left-pane">
        <span className="pane-border-title right">poke-finder</span>
        <div className="pane-header">
          <div className="feature-tabs">
            <button
              className={`feature-tab${activeFeature === 'candidate-finder' ? ' active' : ''}`}
              onClick={() => setActiveFeature('candidate-finder')}
            >
              candidate finder
            </button>
            <button
              className={`feature-tab${activeFeature === 'coverage-analyzer' ? ' active' : ''}`}
              onClick={() => setActiveFeature('coverage-analyzer')}
            >
              type coverage
            </button>
          </div>
        </div>

        <div className="pane-body">
          {activeFeature === 'candidate-finder' && (
            <>
              <CandidateFinderSearch
                onSearch={handleCandidateSearch}
                onError={msg => setCfError(msg)}
                lastParams={cfLastParams}
              />
              {cfError && <p className="error-msg">{cfError}</p>}
            </>
          )}
          {activeFeature === 'coverage-analyzer' && (
            <>
              <CoverageAnalyzerSearch
                onSearch={handleCoverageSearch}
                onError={msg => setCaError(msg)}
                lastSlots={caLastSlots}
              />
              {caError && <p className="error-msg">{caError}</p>}
            </>
          )}
        </div>
      </div>

      <div className="right-pane">
        <span className="pane-border-title left">results</span>
        <button className="help-btn" onClick={() => setHelpOpen(true)}>CLICK HERE FOR HELP!</button>
        <div className="pane-body">
          {activeFeature === 'candidate-finder' && <CandidateFinderResults data={cfData} />}
          {activeFeature === 'coverage-analyzer' && <CoverageAnalyzerResults data={caData} />}
        </div>
      </div>
    </div>
  );
}
