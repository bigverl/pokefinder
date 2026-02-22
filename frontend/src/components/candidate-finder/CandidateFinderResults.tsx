import { DataTable } from '../shared/DataTable';
import { Tabs } from '../shared/Tabs';
import type { CandidateFinderResponse } from '../../api/types';

interface CandidateFinderResultsProps {
  data: CandidateFinderResponse | null;
}

export function CandidateFinderResults({ data }: CandidateFinderResultsProps) {
  const movesRows = data?.moves_table?.rows.map(r => [
    r.pokemon_name,
    r.move_name,
    r.level_learned,
    r.machine ?? '',
    r.egg_move ?? '',
  ]) ?? [];

  const statsRows = data?.stats_table?.rows.map(r => [
    r.name,
    r.attack,
    r.defense,
    r.special_attack,
    r.special_defense,
    r.speed,
  ]) ?? [];

  const typesRows = data?.types_table?.rows.map(r => [
    r.name,
    r.type1,
    r.type2 ?? '',
  ]) ?? [];

  return (
    <Tabs tabs={[
      {
        label: 'moves',
        content: (
          <DataTable
            columns={['pokemon', 'move', 'level learned', 'machine', 'egg move']}
            rows={movesRows}
          />
        ),
      },
      {
        label: 'stats',
        content: (
          <DataTable
            columns={['name', 'attack', 'defense', 'special attack', 'special defense', 'speed']}
            rows={statsRows}
          />
        ),
      },
      {
        label: 'types',
        content: (
          <DataTable
            columns={['name', 'type 1', 'type 2']}
            rows={typesRows}
          />
        ),
      },
    ]} />
  );
}
