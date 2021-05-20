import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';

const features = [
  {
    title: 'About',
    description: (
      <>
        Here you can find some useful information about us
      </>
    ),
    link: 'about'
  },
  {
    title: 'Machine',
    description: (
      <>
        Guides and information about our Machine plan
      </>
    ),
    link: 'machine/app'
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
        List of security requirements considered by our organization
      </>
    ),
    link: 'criteria'
  },
  {
    title: 'Types',
    description: (
      <>
        List of vulnerability types related to security requirements
      </>
    ),
    link: 'types'
  },
  {
    title: 'Security',
    description: (
      <>
        Take a look at the principles that matter most to us as a security company
      </>
    ),
    link: 'security'
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

function Feature({imageUrl, title, description, link}) {
  const imgUrl = useBaseUrl(imageUrl);
  return (
    <div className={clsx('col col--4', styles.feature)}>
      {imgUrl && (
        <div className="text--center">
          <img className={styles.featureImage} src={imgUrl} alt={title} />
        </div>
      )}
      <a className={styles.button} href={link}>
      <h3>{title}</h3>
      <p>{description}</p>
      </a>
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
