import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <Heading as="h1" className={clsx('hero__title', styles.gradientTitle)}>
          {siteConfig.title}
        </Heading>
        <p className="hero__subtitle">Bridging the gap between the digital brain and the physical body.</p>
        <div className={styles.buttons}>
          <Link
            className={clsx('button button--lg', styles.primaryButton)}
            to="/docs/module-01-ros2/week-01-intro">
            Start Learning
          </Link>
          <Link
            className={clsx('button button--lg', styles.secondaryButton)}
            to="https://github.com/facebook/docusaurus">
            GitHub Repo
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <HomepageHeader />
      <main className={styles.mainContent}>
        <div className="container padding-vert--xl">
          <div className="row">
            <div className="col col--4">
              <div className={styles.featureCard}>
                <div className={styles.featureIcon}>🧠</div>
                <Heading as="h3" className={styles.featureTitle}>Embodied Intelligence</Heading>
                <p className={styles.featureDescription}>Learn how AI transitions from digital bits to physical atoms.</p>
              </div>
            </div>
            <div className="col col--4">
              <div className={styles.featureCard}>
                <div className={styles.featureIcon}>🤖</div>
                <Heading as="h3" className={styles.featureTitle}>Humanoid Control</Heading>
                <p className={styles.featureDescription}>Master kinematics, dynamics, and zero-moment point balancing.</p>
              </div>
            </div>
            <div className="col col--4">
              <div className={styles.featureCard}>
                <div className={styles.featureIcon}>💬</div>
                <Heading as="h3" className={styles.featureTitle}>RAG Integrated</Heading>
                <p className={styles.featureDescription}>Chat with the book using our embedded AI assistant.</p>
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}