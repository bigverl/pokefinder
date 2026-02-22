import { DataTable } from '../shared/DataTable';
import { Tabs } from '../shared/Tabs';
import type { CoverageAnalyzerResponse } from '../../api/types';

interface CoverageAnalyzerResultsProps {
  data: CoverageAnalyzerResponse | null;
}

export function CoverageAnalyzerResults({ data }: CoverageAnalyzerResultsProps) {
  const columns = ['effectiveness', 'enemy type', 'your type'];

  const strengthsRows = data?.team_strengths_table?.rows.map(r => [
    r.effectiveness,
    r.enemy_type,
    r.friendly_type,
  ]) ?? [];

  const weaknessesRows = data?.team_weaknesses_table?.rows.map(r => [
    r.effectiveness,
    r.enemy_type,
    r.friendly_type,
  ]) ?? [];

  return (
    <Tabs tabs={[
      {
        label: 'strengths',
        content: <DataTable columns={columns} rows={strengthsRows} />,
      },
      {
        label: 'weaknesses',
        content: <DataTable columns={columns} rows={weaknessesRows} />,
      },
    ]} />
  );
}
