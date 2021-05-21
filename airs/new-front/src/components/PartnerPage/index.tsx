/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Link, graphql, useStaticQuery } from "gatsby";
import React from "react";

import { CardsContainer } from "../../styles/styledComponents";
import { DropDownCard } from "../DropDownCard";

interface IData {
  allAsciidoc: {
    edges: [
      {
        node: {
          fields: {
            slug: string;
          };
          document: {
            title: string;
          };
          html: string;
          pageAttributes: {
            alt: string;
            description: string;
            keywords: string;
            partner: string;
            partnerlogo: string;
            slug: string;
          };
        };
      }
    ];
  };
}

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
          ({ node }): JSX.Element => (
            <DropDownCard
              haveTitle={false}
              key={node.pageAttributes.slug}
              node={node}
            />
          )
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
