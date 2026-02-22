import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { CandidateFinderResults } from './CandidateFinderResults';
import type { CandidateFinderResponse } from '../../api/types';

const mockData: CandidateFinderResponse = {
  moves_table: {
    rows: [
      { pokemon_name: 'charizard', move_name: 'flamethrower', level_learned: 20, machine: null, egg_move: null },
    ],
  },
  stats_table: {
    rows: [
      { name: 'charizard', attack: 84, defense: 78, special_attack: 109, special_defense: 85, speed: 100 },
    ],
  },
  types_table: {
    rows: [{ name: 'charizard', type1: 'fire', type2: 'flying' }],
  },
};

describe('CandidateFinderResults', () => {
  it('renders moves tab with correct columns', () => {
    render(<CandidateFinderResults data={mockData} />);
    expect(screen.getByText('pokemon')).toBeInTheDocument();
    expect(screen.getByText('move')).toBeInTheDocument();
    expect(screen.getByText('level learned')).toBeInTheDocument();
  });

  it('renders moves table data', () => {
    render(<CandidateFinderResults data={mockData} />);
    expect(screen.getByText('charizard')).toBeInTheDocument();
    expect(screen.getByText('flamethrower')).toBeInTheDocument();
    expect(screen.getByText('20')).toBeInTheDocument();
  });

  it('renders with null data without crashing', () => {
    render(<CandidateFinderResults data={null} />);
    expect(screen.getByText('pokemon')).toBeInTheDocument();
  });
});
