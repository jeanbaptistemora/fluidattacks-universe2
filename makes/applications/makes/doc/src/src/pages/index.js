import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './styles.module.css';

const features = [
  {
    title: 'Web',
    description: (
      <>
        Here are our UI guides for the Attack Surface Manager
      </>
    ),
    link: 'web'
  },
  {
    title: 'API',
    description: (
      <>
        Utilize our API for sending and getting data quickly and efficiently
      </>
    ),
    link: 'api'
  },
  {
    title: 'Agent',
    description: (
      <>
        The DevSecOps Agent you can use for breaking your build in case your system is vulnerable
      </>
    ),
    link: 'agent'
  },
  {
    title: 'Rules',
    description: (
      <>
        List of security requirements considered by our organization
      </>
    ),
    link: 'rules'
  },
  {
    title: 'Dev',
    description: (
      <>
        Information, guides and tips useful to our production team in the development of products
      </>
    ),
    link: 'dev'
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
