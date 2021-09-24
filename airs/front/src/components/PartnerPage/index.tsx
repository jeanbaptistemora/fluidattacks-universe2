/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Link, graphql, useStaticQuery } from "gatsby";
import React from "react";

import { CardsContainer } from "../../styles/styledComponents";
import { DropDownCard } from "../DropDownCard";

const PartnerPage: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query PartnerQuery {
      allMarkdownRemark(sort: { fields: [frontmatter___alt], order: ASC }) {
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
              partner
              partnerlogo
              slug
              title
            }
          }
        }
      }
    }
  `);

  const partnerInfo = data.allMarkdownRemark.edges.filter(
    (partnerCard): boolean => partnerCard.node.frontmatter.partner === "yes"
  );

  return (
    <React.Fragment>
      <CardsContainer>
        {partnerInfo.map(
          ({ node }): JSX.Element => {
            const { alt, partnerlogo, slug, title } = node.frontmatter;

            return (
              <DropDownCard
                alt={alt}
                cardType={"partners-cards"}
                haveTitle={false}
                htmlData={node.html}
                key={slug}
                logo={partnerlogo}
                logoPaths={"/airs/partners"}
                slug={slug}
                title={title}
              />
            );
          }
        )}
      </CardsContainer>
      <div>
        <p>
          {"If you are interested in partnering with"}
          <code>{"Fluid Attacks"}</code>
          {", please submit the following "}
          <Link to={"/contact-us/"}>{"Contact Form."}</Link>
        </p>
      </div>
    </React.Fragment>
  );
};

export { PartnerPage };
