import { useState } from 'react';
import { Card as CardType } from '../../App';
import Card from '../Card/Card';
import ExpandedCard from '../ExpandedCard/ExpandedCard';
import styles from './CardList.module.css';

interface CardListProps {
  cards: CardType[];
}

const CardList = ({ cards }: CardListProps) => {
  const [viewMode, setViewMode] = useState<'compact' | 'expanded'>('compact');

  if (cards.length === 0) {
    return (
      <div className={styles.emptyState}>
        <h2>No solutions found yet</h2>
        <p>Enter a humanitarian challenge in the search bar above to find AI-powered solutions.</p>
      </div>
    );
  }

  return (
    <div className={styles.cardList}>
      <div className={styles.listHeader}>
        <h2 className={styles.resultsTitle}>
          {cards.length} {cards.length === 1 ? 'Solution' : 'Solutions'} Found
        </h2>
        <div className={styles.viewToggle}>
          <button 
            className={`${styles.viewButton} ${viewMode === 'compact' ? styles.activeView : ''}`}
            onClick={() => setViewMode('compact')}
          >
            Compact View
          </button>
          <button 
            className={`${styles.viewButton} ${viewMode === 'expanded' ? styles.activeView : ''}`}
            onClick={() => setViewMode('expanded')}
          >
            Expanded View
          </button>
        </div>
      </div>
      <div className={viewMode === 'expanded' ? styles.expandedCardGrid : styles.cardGrid}>
        {cards.map((card, index) => (
          <div className={styles.cardWrapper} key={`${card.title}-${index}`}>
            {viewMode === 'compact' ? (
              <Card card={card} />
            ) : (
              <ExpandedCard card={card} />
            )}
          </div>
        ))}
      </div>
    </div>
  );
};

export default CardList;