import { useState } from 'react';
import styles from './SearchBar.module.css';

interface SearchBarProps {
  query: string;
  setQuery: (query: string) => void;
  limitUseCase: number;
  setLimitUseCase: (limit: number) => void;
  onSearch: () => void;
  isLoading: boolean;
}

const SearchBar = ({ 
  query, 
  setQuery, 
  limitUseCase, 
  setLimitUseCase, 
  onSearch, 
  isLoading 
}: SearchBarProps) => {
  const [isAdvancedOpen, setIsAdvancedOpen] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch();
  };

  return (
    <div className={styles.searchBarContainer}>
      <h1 className={styles.title}>Find AI Solutions for Humanitarian Challenges</h1>
      <p className={styles.subtitle}>
        Enter a post-conlict humanitarian problem to discover technological or AI-based approaches with benefits, risks, and mitigations.      </p>
      
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.inputGroup}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., lack of clean water in Sudan after conflict"
            className={styles.input}
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className={styles.searchButton}
            disabled={isLoading || !query.trim()}
          >
            {isLoading ? 'Analyzing... ' : 'Analyze'}
          </button>
        </div>
        
        <div className={styles.advancedOptions}>
          <button 
            type="button" 
            className={styles.advancedToggle}
            onClick={() => setIsAdvancedOpen(!isAdvancedOpen)}
          >
            {isAdvancedOpen ? '− Hide' : '+ Show'} Advanced Options
          </button>
          
          {isAdvancedOpen && (
            <div className={styles.advancedControls}>
              <div className={styles.controlGroup}>
                <label htmlFor="limitUseCase">Maximum number of solutions:</label>
                <input
                  id="limitUseCase"
                  type="number"
                  min="1"
                  max="20"
                  value={limitUseCase}
                  onChange={(e) => setLimitUseCase(Number(e.target.value))}
                  className={styles.numberInput}
                />
              </div>
            </div>
          )}
        </div>
      </form>
    </div>
  );
};

export default SearchBar;