import { Card as CardType } from '../../App';
import Card from '../Card/Card';
import styles from './CardList.module.css';

interface CardListProps {
  cards: CardType[];
}

const CardList = ({ cards }: CardListProps) => {
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
      <h2 className={styles.resultsTitle}>
        {cards.length} {cards.length === 1 ? 'Solution' : 'Solutions'} Found
      </h2>
      <div className={styles.cardGrid}>
        {cards.map((card, index) => (
          <div className={styles.cardWrapper} key={`${card.title}-${index}`}>
            <Card card={card} />
          </div>
        ))}
      </div>
    </div>
  );
};

export default CardList;