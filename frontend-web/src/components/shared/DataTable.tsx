import { useState } from 'react';
import './DataTable.css';

type CellValue = string | number | null | undefined;

interface DataTableProps {
  columns: string[];
  rows: CellValue[][];
}

type SortDir = 'asc' | 'desc';

function sortKey(value: CellValue): [number, string | number] {
  if (typeof value === 'number') return [0, value];
  return [1, String(value ?? '').toLowerCase()];
}

function compareRows(a: CellValue[], b: CellValue[], colIndex: number, dir: SortDir): number {
  const [aTier, aVal] = sortKey(a[colIndex]);
  const [bTier, bVal] = sortKey(b[colIndex]);
  if (aTier !== bTier) return aTier - bTier;
  if (aVal < bVal) return dir === 'asc' ? -1 : 1;
  if (aVal > bVal) return dir === 'asc' ? 1 : -1;
  return 0;
}

export function DataTable({ columns, rows }: DataTableProps) {
  const [sortCol, setSortCol] = useState<number | null>(null);
  const [sortDir, setSortDir] = useState<SortDir>('asc');

  function handleHeaderClick(colIndex: number) {
    if (sortCol === colIndex) {
      setSortDir(d => (d === 'asc' ? 'desc' : 'asc'));
    } else {
      setSortCol(colIndex);
      setSortDir('asc');
    }
  }

  const sorted =
    sortCol !== null
      ? [...rows].sort((a, b) => compareRows(a, b, sortCol, sortDir))
      : rows;

  return (
    <div className="data-table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((col, i) => (
              <th key={col} onClick={() => handleHeaderClick(i)} className="sortable-header">
                {col}
                {sortCol === i && (
                  <span className="sort-indicator">{sortDir === 'asc' ? ' ^' : ' v'}</span>
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sorted.map((row, ri) => (
            <tr key={ri}>
              {row.map((cell, ci) => (
                <td key={ci}>{cell ?? ''}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
