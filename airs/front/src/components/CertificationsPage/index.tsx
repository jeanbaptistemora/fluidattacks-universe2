/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { CardsContainer } from "../../styles/styledComponents";
import { DropDownCard } from "../DropDownCard";

const CertificationsPage: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query CertificationQuery {
      allMarkdownRemark(
        sort: { fields: [frontmatter___certificationid], order: ASC }
      ) {
        edges {
          node {
            fields {
              slug
            }
            html
            frontmatter {
              alt
              description
              keywords
              certification
              certificationid
              certificationlogo
              slug
              title
            }
          }
        }
      }
    }
  `);

  const certificationInfo = data.allMarkdownRemark.edges.filter(
    (certificationCard): boolean =>
      certificationCard.node.frontmatter.certification === "yes"
  );

  return (
    <CardsContainer>
      {certificationInfo.map(
        ({ node }): JSX.Element => {
          const { alt, certificationlogo, slug, title } = node.frontmatter;

          return (
            <DropDownCard
              alt={alt}
              cardType={"certifications-cards"}
              haveTitle={true}
              htmlData={node.html}
              key={slug}
              logo={certificationlogo}
              logoPaths={"/airs/about-us/certifications"}
              slug={slug}
              title={title}
            />
          );
        }
      )}
    </CardsContainer>
  );
};

export { CertificationsPage };
