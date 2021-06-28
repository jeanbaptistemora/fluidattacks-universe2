/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Link, graphql, useStaticQuery } from "gatsby";
import React from "react";

import { CardsContainer } from "../../styles/styledComponents";
import { DropDownCard } from "../DropDownCard";

const PartnerPage: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query PartnerQuery {
      allAsciidoc(sort: { fields: [pageAttributes___slug], order: ASC }) {
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
              partner
              partnerlogo
              slug
            }
          }
        }
      }
    }
  `);

  const partnerInfo = data.allAsciidoc.edges.filter(
    (partnerCard): boolean => partnerCard.node.pageAttributes.partner === "yes"
  );

  return (
    <React.Fragment>
      <CardsContainer>
        {partnerInfo.map(
          ({ node }): JSX.Element => {
            const { alt, partnerlogo, slug } = node.pageAttributes;

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
                title={node.document.title}
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
