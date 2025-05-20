import { Card as CardType } from '../../App';
import styles from './ExpandedCard.module.css';

interface ExpandedCardProps {
  card: CardType;
}

const ExpandedCard = ({ card }: ExpandedCardProps) => {
  // Calculate badge color based on relevance score
  const getBadgeColor = () => {
    const score = card.relevance_score;
    if (score >= 0.8) return styles.highRelevance;
    if (score >= 0.5) return styles.mediumRelevance;
    return styles.lowRelevance;
  };

  return (
    <div className={styles.expandedCard}>
      <div className={styles.header}>
        <div className={styles.titleArea}>
          <h4 className={styles.title}>{card.title}</h4>
          <div className={`${styles.badge} ${getBadgeColor()}`}>
            {(card.relevance_score * 100).toFixed(0)}%
          </div>
        </div>
        <div className={styles.contextTag}>{card.context}</div>
      </div>

      <div className={styles.content}>
        <div className={styles.overview}>
          <h5 className={styles.sectionTitle}>Overview</h5>
          <p className={styles.description}>{card.description}</p>
          {card.source && <div className={styles.source}>Source: {card.source}</div>}
        </div>

        <div className={styles.benefitsSection}>
          <h5 className={styles.sectionTitle}>Benefits ({card.benefits.length})</h5>
          <div className={styles.benefitsList}>
            {card.benefits.map((benefit, index) => (
              <div key={index} className={styles.benefit}>
                <div className={styles.benefitHeader}>
                  <h4 className={styles.benefitTitle}>{benefit.title}</h4>
                  <div className={styles.benefitContext}>{benefit.context}</div>
                </div>
                <p className={styles.benefitDescription}>{benefit.description}</p>
                <div className={styles.source}>Source: {benefit.source}</div>
              </div>
            ))}
          </div>
        </div>

        <div className={styles.risksSection}>
          <h5 className={styles.sectionTitle}>Risks & Mitigations ({card.risks_mitigations.length})</h5>
          <div className={styles.risksList}>
            {card.risks_mitigations.map((risk, index) => (
              <div key={index} className={styles.riskWithMitigation}>
                <div className={styles.risk}>
                  <div className={styles.riskHeader}>
                    <h4 className={styles.riskTitle}>{risk.risk_title}</h4>
                  </div>
                  
                  <div className={styles.riskContent}>
                    <div className={styles.riskContext}>{risk.risk_context}</div>
                    <p className={styles.riskDescription}>{risk.risk_description}</p>
                    <div className={styles.source}>Source: {risk.risk_source}</div>
                  </div>
                </div>
                
                <div className={styles.mitigation}>
                  <div className={styles.mitigationHeader}>
                    <h5 className={styles.mitigationTitle}>
                      <span className={styles.mitigationIcon}>⚡</span>
                      {risk.mitigation_title}
                    </h5>
                    <div className={styles.mitigationContext}>{risk.mitigation_context}</div>
                  </div>
                  <p className={styles.mitigationDescription}>{risk.mitigation_description}</p>
                  <div className={styles.source}>Source: {risk.mitigation_source}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExpandedCard;