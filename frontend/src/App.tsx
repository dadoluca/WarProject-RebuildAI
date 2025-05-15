import { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar/SearchBar';
import CardList from './components/CardList/CardList';
import Header from './components/Header/Header';
import styles from './App.module.css';

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
  source: string;
  relevance_score: number;
  benefits: Benefit[];
  risks_mitigations: RiskMitigation[];
}

export interface QueryResponse {
  cards: Card[];
  query: string;
}

function App() {
  const [query, setQuery] = useState('');
  const [limitUseCase, setLimitUseCase] = useState(5);
  const [cards, setCards] = useState<Card[]>([]);
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
          limit_use_case: limitUseCase 
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

  // For demo purposes, populate with sample data from the provided content
  useEffect(() => {
    // This is just for demonstration - you'd normally not have this
    if (import.meta.env.DEV && cards.length === 0 && !isLoading) {
      const sampleCard = {
        title: "Mobile Water Quality Testing and Monitoring",
        context: "Post-conflict, humanitarian (addressing water quality issues in Sudan after conflict)",
        description: "Deploying mobile water quality testing units equipped with sensors and data analytics to assess the safety of water sources in conflict-affected regions of Sudan. These units can provide real-time data on contaminants, enabling humanitarian organizations to prioritize interventions and ensure access to clean water for affected populations.",
        source: "Inspired by AI for WASH in Fragile States, 2017.",
        relevance_score: 0.95,
        benefits: [
          {
            context: "Post-conflict, humanitarian (water safety in conflict zones)",
            description: "The deployment of mobile water quality testing units allows for continuous monitoring of water sources, providing real-time data on contaminants such as bacteria, heavy metals, and chemical pollutants. This proactive approach enables humanitarian organizations to identify and address potential health risks before they escalate into widespread outbreaks of waterborne diseases, ultimately protecting the health of vulnerable populations in conflict-affected regions of Sudan.",
            source: "Adapted from mobile water quality testing initiatives in humanitarian contexts.",
            title: "Enhanced Public Health Monitoring"
          }
        ],
        risks_mitigations: [
          {
            mitigation_context: "Mobile Water Quality Testing and Monitoring in post-conflict Sudan",
            mitigation_description: "Establish a comprehensive training program for local technicians to ensure they are equipped with the necessary skills for sensor calibration and maintenance of mobile water quality testing units. This program should include hands-on training, remote support options, and the creation of easy-to-follow maintenance manuals tailored to the local context. By empowering local personnel, the reliance on external technical support can be reduced, ensuring the sustainability of the water quality monitoring efforts even in challenging environments.",
            mitigation_source: "Inspired by capacity building strategies in humanitarian contexts.",
            mitigation_title: "Local Technician Training Program",
            risk_context: "Mobile water quality testing in post-conflict regions",
            risk_description: "The mobile water quality testing units may face challenges in sensor calibration and maintenance due to the harsh environmental conditions and limited access to technical support in conflict-affected areas. This could lead to inaccurate readings of water quality, compromising the safety assessments and potentially endangering public health.",
            risk_source: "Expert analysis based on field conditions in Sudan",
            risk_title: "Sensor Calibration and Maintenance Challenges"
          },
          {
            mitigation_context: "Mobile Water Quality Testing in Conflict Zones",
            mitigation_description: "Develop and implement comprehensive security protocols specifically for mobile water quality testing units. This includes training personnel on situational awareness, establishing safe routes for travel, and creating emergency response plans. Collaborate with local authorities and community leaders to ensure the safety of the teams and the equipment during deployment. Regularly assess the security situation and adapt protocols as necessary to mitigate risks of theft, vandalism, or targeted attacks.",
            mitigation_source: "Adapted from general security measures for humanitarian operations.",
            mitigation_title: "Mobile Unit Security Protocols",
            risk_context: "Mobile water quality testing in conflict-affected areas",
            risk_description: "Deploying mobile water quality testing units in conflict zones poses security risks, including theft, vandalism, or targeted attacks against humanitarian workers. Such incidents could disrupt operations, limit access to critical data, and deter organizations from deploying necessary interventions to ensure clean water access.",
            risk_source: "Field reports on humanitarian operations in conflict zones",
            risk_title: "Security Risks to Mobile Units"
          }
        ]
      };
      setCards([sampleCard]);
    }
  }, [cards.length, isLoading]);

  return (
    <div className={styles.app}>
      <Header />
      <main className={styles.main}>
        <div className={styles.container}>
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
              <p>Analyzing your query...</p>
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