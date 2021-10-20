import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import useThemeContext from '@theme/hooks/useThemeContext';
import styles from './styles.module.css';
import BrowserOnly from '@docusaurus/BrowserOnly';

const features = [
  {
    title: 'About',
    description: (
      <>
        Here you can find some useful information about us
      </>
    ),
    link: 'about/faq'
  },
  {
    title: 'Machine',
    description: (
      <>
        Guides and information about our Machine plan
      </>
    ),
    link: 'machine/web'
  },
  {
    title: 'Squad',
    description: (
      <>
        Guides and information about our Squad plan
      </>
    ),
    link: 'squad'
  },
  {
    title: 'Criteria',
    description: (
      <>
        List of security requirements, compliances and vulnerabilities considered by our organization
      </>
    ),
    link: 'criteria/'
  },
  {
    title: 'Development',
    description: (
      <>
        Information, guides and tips useful to our production team in the development of products
      </>
    ),
    link: 'development'
  },
];

function Card({cardLink, children}) {
  const { isDarkTheme } = useThemeContext();
  return (
    <a className={isDarkTheme ? styles.darkCard : styles.card} href={cardLink}>
      {children}
    </a>
  );
}

function Feature({imageUrl, title, description, link}) {
  const imgUrl = useBaseUrl(imageUrl);
  return (
    <div className={clsx('col col--4', styles.feature)}>
      {imgUrl && (
        <div className="text--center">
          <img className={styles.featureImage} src={imgUrl} alt={title} />
        </div>
      )}
      <BrowserOnly>
        {() => {
          return (
            <Card cardLink={link}>
              <h3>{title}</h3>
              <p>{description}</p>
            </Card>
          )
        }}
      </BrowserOnly>
    </div>
  );
}

function Home() {
  const context = useDocusaurusContext();
  const {siteConfig = {}} = context;
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Description will go into a meta tag in <head />">
      <main>
        {features && features.length > 0 && (
          <section className={styles.features}>
            <div className="container">
              <div className="row">
                {features.map((props, idx) => (
                  <Feature key={idx} {...props} />
                ))}
              </div>
            </div>
          </section>
        )}
      </main>
    </Layout>
  );
}

export default Home;
