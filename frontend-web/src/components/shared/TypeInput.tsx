import './TypeInput.css';

const TYPES = [
  'normal', 'fire', 'water', 'electric', 'grass', 'ice',
  'fighting', 'poison', 'ground', 'flying', 'psychic', 'bug',
  'rock', 'ghost', 'dragon', 'dark', 'steel', 'fairy',
];

interface TypeInputProps {
  id: string;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

export function TypeInput({ id, value, onChange, disabled }: TypeInputProps) {
  const listId = `${id}-list`;
  return (
    <>
      <input
        id={id}
        className="type-input"
        list={listId}
        value={value}
        onChange={e => onChange(e.target.value)}
        disabled={disabled}
        autoComplete="off"
      />
      <datalist id={listId}>
        {TYPES.map(t => <option key={t} value={t} />)}
      </datalist>
    </>
  );
}
