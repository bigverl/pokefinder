import './FilterBox.css';

interface FilterBoxProps {
  title: string;
  children: React.ReactNode;
}

export function FilterBox({ title, children }: FilterBoxProps) {
  return (
    <div className="filter-box">
      <span className="filter-box-title">{title}</span>
      {children}
    </div>
  );
}
