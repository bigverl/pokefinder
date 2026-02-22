import './TypeInput.css';

const TYPES = [
  'normal', 'fire', 'water', 'electric', 'grass', 'ice',
  'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug',
  'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy',
];

function getMatch(value: string): string | null {
  if (!value) return null;
  const lower = value.toLowerCase();
  return TYPES.find(t => t.startsWith(lower) && t !== lower) ?? null;
}

interface TypeInputProps {
  id: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function TypeInput({ id, value, onChange, disabled }: TypeInputProps) {
  const match = getMatch(value);
  const suffix = match ? match.slice(value.length) : '';

  return (
    <div className="type-input-wrap">
      {match && (
        <div className="type-ghost" aria-hidden="true">
          <span className="type-ghost-typed">{value}</span>
          <span className="type-ghost-suffix">{suffix}</span>
        </div>
      )}
      <input
        id={id}
        className="type-input"
        value={value}
        onChange={e => onChange(e.target.value)}
        onKeyDown={e => {
          if (e.key === 'Tab' && match) {
            e.preventDefault();
            onChange(match);
          }
        }}
        disabled={disabled}
        autoComplete="off"
      />
    </div>
  );
}
