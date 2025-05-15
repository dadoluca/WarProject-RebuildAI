import styles from './Header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
      <div className={styles.logoContainer}>
        <div className={styles.logo}>
          <span className={styles.rebuild}>Rebuild</span>
          <span className={styles.ai}>AI</span>
        </div>
        <div className={styles.tagline}>AI-powered humanitarian solutions</div>
      </div>
    </header>
  );
};

export default Header;