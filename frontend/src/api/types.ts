// Candidate Finder

export interface MovesTableRow {
  pokemon_name: string;
  move_name: string;
  level_learned: string | number | null;
  machine: string | null;
  egg_move: string | null;
}

export interface StatsTableRow {
  name: string;
  attack: number;
  defense: number;
  special_attack: number;
  special_defense: number;
  speed: number;
}

export interface TypesTableRow {
  name: string;
  type1: string;
  type2: string | null;
}

export interface CandidateFinderResponse {
  moves_table: { rows: MovesTableRow[] } | null;
  stats_table: { rows: StatsTableRow[] } | null;
  types_table: { rows: TypesTableRow[] } | null;
}

export interface CandidateFinderParams {
  move?: string;
  desired_type?: string;
  primary_stat?: string;
  secondary_stat?: string;
  min_primary?: number;
  min_secondary?: number;
  min_speed?: number;
  include_mythical?: boolean;
  include_legendary?: boolean;
  include_ultra_beasts?: boolean;
}

// Coverage Analyzer

export interface CoverageTableRow {
  effectiveness: string;
  enemy_type: string;
  friendly_type: string;
}

export interface CoverageAnalyzerResponse {
  team_strengths_table: { rows: CoverageTableRow[] } | null;
  team_weaknesses_table: { rows: CoverageTableRow[] } | null;
}
