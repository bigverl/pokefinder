import { useState } from 'react';
import './Tabs.css';

interface Tab {
  label: string;
  content: React.ReactNode;
}

interface TabsProps {
  tabs: Tab[];
}

export function Tabs({ tabs }: TabsProps) {
  const [activeIndex, setActiveIndex] = useState(0);

  return (
    <div className="tabs">
      <div className="tabs-bar">
        {tabs.map((tab, i) => (
          <button
            key={tab.label}
            className={`tab-btn${i === activeIndex ? ' active' : ''}`}
            onClick={() => setActiveIndex(i)}
          >
            {tab.label}
          </button>
        ))}
      </div>
      <div className="tab-content">
        {tabs[activeIndex].content}
      </div>
    </div>
  );
}
