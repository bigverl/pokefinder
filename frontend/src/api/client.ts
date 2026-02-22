import type {
  CandidateFinderParams,
  CandidateFinderResponse,
  CoverageAnalyzerResponse,
} from './types';

const BASE_URL = import.meta.env.VITE_BACKEND_URL ?? 'http://localhost:8000';

async function get<T>(path: string, params: Record<string, string>): Promise<T> {
  const url = new URL(path, BASE_URL);
  for (const [key, value] of Object.entries(params)) {
    url.searchParams.set(key, value);
  }

  const res = await fetch(url.toString());
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text);
  }
  return res.json() as Promise<T>;
}

export async function searchPokemon(params: CandidateFinderParams): Promise<CandidateFinderResponse> {
  const query: Record<string, string> = {};

  if (params.move) query.move = params.move;
  if (params.desired_type) query.desired_type = params.desired_type;
  if (params.primary_stat) query.primary_stat = params.primary_stat;
  if (params.secondary_stat) query.secondary_stat = params.secondary_stat;
  if (params.min_primary != null) query.min_primary = String(params.min_primary);
  if (params.min_secondary != null) query.min_secondary = String(params.min_secondary);
  if (params.min_speed != null) query.min_speed = String(params.min_speed);
  if (params.include_mythical) query.include_mythical = 'true';
  if (params.include_legendary) query.include_legendary = 'true';
  if (params.include_ultra_beasts) query.include_ultra_beasts = 'true';

  return get<CandidateFinderResponse>('/search_pokemon', query);
}

export async function searchTeamCoverage(slots: string[]): Promise<CoverageAnalyzerResponse> {
  const query: Record<string, string> = {};
  slots.forEach((slot, i) => {
    query[`slot_${i + 1}`] = slot;
  });
  return get<CoverageAnalyzerResponse>('/team_coverage', query);
}
