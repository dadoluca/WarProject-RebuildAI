import { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar/SearchBar';
import CardList from './components/CardList/CardList';
import Header from './components/Header/Header';
import styles from './App.module.css';
import sampleData from './data/sampleCards.json';

// Types
export interface Benefit {
  context: string;
  description: string;
  source: string;
  title: string;
}

export interface RiskMitigation {
  mitigation_context: string;
  mitigation_description: string;
  mitigation_source: string;
  mitigation_title: string;
  risk_context: string;
  risk_description: string;
  risk_source: string;
  risk_title: string;
}

export interface Card {
  title: string;
  context: string;
  description: string;
  source: string | null; // Updated to allow null
  relevance_score: number;
  benefits: Benefit[];
  risks_mitigations: RiskMitigation[];
  steps_to_implementation: string[];
}

export interface QueryResponse {
  cards: Card[];
  query: string;
}

function App() {
  const [query, setQuery] = useState('');
  const [limitUseCase, setLimitUseCase] = useState(5);
  const [cards, setCards] = useState<Card[]>([]); // Explicitly typed state
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async () => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://127.0.0.1:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          query, 
          limit_use_cases: limitUseCase,
        }),
      });
      
      if (!response.ok) {
        throw new Error(`Server responded with status: ${response.status}`);
      }
      
      const data: QueryResponse = await response.json();
      setCards(data.cards);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
      console.error('Error fetching data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Load sample data in development mode
  useEffect(() => {
    if (import.meta.env.DEV && cards.length === 0 && !isLoading) {
      // Use the imported sample data
      if (sampleData && sampleData.cards && sampleData.cards.length > 0) {
        setCards(sampleData.cards as Card[]); // Type assertion to help TypeScript
      }
    }
  }, [cards.length, isLoading]);

  return (
    <div className={styles.app}>
      <Header />
      
      <main className={styles.main}>
        <div className={styles.searchContainer}>
          <SearchBar 
            query={query} 
            setQuery={setQuery} 
            limitUseCase={limitUseCase}
            setLimitUseCase={setLimitUseCase}
            onSearch={handleSearch}
            isLoading={isLoading}
          />
          
          {error && <div className={styles.error}>{error}</div>}
          
          {isLoading ? (
            <div className={styles.loading}>
              <div className={styles.spinner}></div>
              <p>Analyzing your query... can take a few minutes</p>
            </div>
          ) : (
            <CardList cards={cards} />
          )}
        </div>
      </main>
      
      <footer className={styles.footer}>
        <p>© {new Date().getFullYear()} RebuildAI - AI-powered solutions for humanitarian challenges</p>
      </footer>
    </div>
  );
}

export default App;