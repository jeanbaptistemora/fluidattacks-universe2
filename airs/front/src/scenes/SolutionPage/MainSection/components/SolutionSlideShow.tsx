/* eslint fp/no-mutating-methods:0 */
import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { CardSlideShow } from "../../../../components/CardSlideShow";

interface ISolutionSlideShowProps {
  description: string;
  solution: string;
  title: string;
}

const SolutionSlideShow: React.FC<ISolutionSlideShowProps> = ({
  description,
  solution,
  title,
}): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query SolutionBlogList {
      allMarkdownRemark(
        filter: {
          fields: { slug: { regex: "/blog/" } }
          frontmatter: { image: { regex: "" }, spanish: { eq: null } }
        }
        sort: { fields: frontmatter___date, order: DESC }
      ) {
        edges {
          node {
            fields {
              slug
            }
            frontmatter {
              alt
              slug
              tags
              description
              image
              title
              subtitle
            }
          }
        }
      }
    }
  `);

  const sortList: {
    [key: string]: string[];
    devsecops: string[];
    attackSimulation: string[];
  } = {
    attackSimulation: [
      "/blog/tribe-of-hackers-5/",
      "/blog/tribe-of-hackers-2/",
      "/blog/what-is-red-team-in-cyber-security/",
      "/blog/red-team-exercise/",
      "/blog/bas-vs-pentesting-vs-red-teaming/",
      "/blog/what-is-breach-attack-simulation/",
    ],
    devsecops: [
      "/blog/why-is-cloud-devsecops-important/",
      "/blog/what-does-a-devsecops-engineer-do/",
      "/blog/azure-devsecops-with-fluid-attacks/",
      "/blog/aws-devsecops-with-fluid-attacks/",
      "/blog/devsecops-best-practices/",
      "/blog/devsecops-tools/",
      "/blog/how-to-implement-devsecops/",
      "/blog/devsecops-concept/",
    ],
    ethicalHacking: [
      "/blog/tribe-of-hackers-5/",
      "/blog/tribe-of-hackers-4/",
      "/blog/tribe-of-hackers-3/",
      "/blog/tribe-of-hackers-2/",
      "/blog/tribe-of-hackers-1/",
      "/blog/delimit-ethical-hacking/",
      "/blog/thinking-like-hacker/",
      "/blog/what-is-ethical-hacking/",
    ],
    penetrationTesting: [
      "/blog/bas-vs-pentesting-vs-red-teaming/",
      "/blog/importance-pentesting/",
      "/blog/choosing-pentesting-team/",
      "/blog/what-is-ptaas/",
      "/blog/what-is-manual-penetration-testing/",
    ],
    redTeaming: [
      "/blog/bas-vs-pentesting-vs-red-teaming/",
      "/blog/tiber-eu-providers/",
      "/blog/tiber-eu-framework/",
      "/blog/attacking-without-announcing/",
      "/blog/red-team-exercise/",
      "/blog/what-is-red-team-in-cyber-security/",
    ],
    secureCodeReview: [
      "/blog/differences-between-sast-sca-dast/",
      "/blog/sastisfying-app-security/",
      "/blog/secure-coding-five-steps/",
      "/blog/secure-coding-practices/",
      "/blog/code-quality-and-security/",
      "/blog/manual-code-review/",
      "/blog/secure-code-review/",
    ],
    securityTesting: [
      "/blog/what-is-mast/",
      "/blog/what-is-ptaas/",
      "/blog/reverse-engineering/",
      "/blog/stand-shoulders-giants/",
      "/blog/sca-scans/",
      "/blog/sastisfying-app-security/",
      "/blog/casa-approved-static-scanning/",
      "/blog/differences-between-sast-sca-dast/",
    ],
    vulnerabilityManagement: [
      "/blog/aws-devsecops-with-fluid-attacks/",
      "/blog/devsecops-tools/",
      "/blog/cvssf-risk-exposure-metric/",
      "/blog/rules-new-standard/",
      "/blog/attack-resistance-management-psirts/",
      "/blog/from-asm-to-arm/",
    ],
  };

  const blogs: INodes[] = data.allMarkdownRemark.edges;

  const toFilter: string[] = sortList[solution];

  const filterBlogs: INodes[] = blogs.filter((post): boolean => {
    return toFilter.some((slug): boolean => {
      return slug === post.node.fields.slug;
    });
  });

  const sortedBlogs = [...filterBlogs].sort(
    (first, second): number =>
      toFilter.indexOf(second.node.fields.slug) -
      toFilter.indexOf(first.node.fields.slug)
  );

  return (
    <CardSlideShow
      btnText={"Read post"}
      containerDescription={description}
      containerTitle={title}
      data={sortedBlogs}
      variant={"dark"}
    />
  );
};

export { SolutionSlideShow };
