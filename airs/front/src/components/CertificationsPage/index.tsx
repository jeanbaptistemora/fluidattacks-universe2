/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { CardsContainer } from "../../styles/styledComponents";
import { DropDownCard } from "../DropDownCard";

const CertificationsPage: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query CertificationQuery {
      allAsciidoc(
        sort: { fields: [pageAttributes___certificationid], order: ASC }
      ) {
        edges {
          node {
            fields {
              slug
            }
            document {
              title
            }
            html
            pageAttributes {
              alt
              description
              keywords
              certification
              certificationid
              certificationlogo
              slug
            }
          }
        }
      }
    }
  `);

  const certificationInfo = data.allAsciidoc.edges.filter(
    (certificationCard): boolean =>
      certificationCard.node.pageAttributes.certification === "yes"
  );

  return (
    <CardsContainer>
      {certificationInfo.map(
        ({ node }): JSX.Element => {
          const { alt, certificationlogo, slug } = node.pageAttributes;

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
              title={node.document.title}
            />
          );
        }
      )}
    </CardsContainer>
  );
};

export { CertificationsPage };
