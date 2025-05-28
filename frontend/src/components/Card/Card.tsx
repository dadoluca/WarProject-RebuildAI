import { useState } from 'react';
import { Card as CardType } from '../../App';
import styles from './Card.module.css';

interface CardProps {
  card: CardType;
}

const Card = ({ card }: CardProps) => {
  const [activeTab, setActiveTab] = useState<'overview' | 'benefits' | 'steps' | 'risks'>('overview');
  const [expandedRiskIndex, setExpandedRiskIndex] = useState<number | null>(null);

  const handleToggleRisk = (index: number) => {
    setExpandedRiskIndex(expandedRiskIndex === index ? null : index);
  };

  // Calculate badge color based on relevance score
  const getBadgeColor = () => {
    const score = card.relevance_score;
    if (score >= 0.8) return styles.highRelevance;
    if (score >= 0.5) return styles.mediumRelevance;
    return styles.lowRelevance;
  };

  return (
    <div className={styles.card}>
      <div className={styles.header}>
        <div className={styles.titleArea}>
          <h4 className={styles.title}>{card.title}</h4>
          <div className={`${styles.badge} ${getBadgeColor()}`}>
            {(card.relevance_score * 100).toFixed(0)}%
          </div>
        </div>
        <div className={styles.contextTag}>{card.context}</div>
      </div>

      <div className={styles.tabs}>
        <button
          className={`${styles.tab} ${activeTab === 'overview' ? styles.activeTab : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'steps' ? styles.activeTab : ''}`}
          onClick={() => setActiveTab('steps')}
        >
          Steps
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'benefits' ? styles.activeTab : ''}`}
          onClick={() => setActiveTab('benefits')}
        >
          Benefits ({card.benefits.length})
        </button>
        <button
          className={`${styles.tab} ${activeTab === 'risks' ? styles.activeTab : ''}`}
          onClick={() => setActiveTab('risks')}
        >
          Risks ({card.risks_mitigations.length})
        </button>
      </div>

      <div className={styles.content}>
        {activeTab === 'overview' && (
          <div className={styles.overview}>
            <p className={styles.description}>{card.description}</p>
            <div className={styles.source}>Source: {card.source}</div>
          </div>
        )}

        {activeTab === 'steps' && card.steps_to_implementation &&(
          <div className={styles.stepsList}>
            {card.steps_to_implementation.map((step, index) => (
              <div key={index} className={styles.step}>
                <div className={styles.stepNumber}>Step {index + 1}</div>
                <p className={styles.stepText}>{step}</p>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'benefits' && (
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
        )}

        {activeTab === 'risks' && (
          <div className={styles.risksList}>
            {card.risks_mitigations.map((risk, index) => (
              <div key={index} className={styles.risk}>
                <div
                  className={styles.riskHeader}
                  onClick={() => handleToggleRisk(index)}
                >
                  <h4 className={styles.riskTitle}>{risk.risk_title}</h4>
                  <span className={styles.expandIcon}>
                    {expandedRiskIndex === index ? '−' : '+'}
                  </span>
                </div>

                <div className={styles.riskContent}>
                  <div className={styles.riskContext}>{risk.risk_context}</div>
                  <p className={styles.riskDescription}>{risk.risk_description}</p>
                  <div className={styles.source}>Source: {risk.risk_source}</div>
                </div>

                {expandedRiskIndex === index && (
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
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Card;