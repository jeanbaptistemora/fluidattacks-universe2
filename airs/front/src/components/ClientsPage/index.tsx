/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import { graphql, useStaticQuery } from "gatsby";
import React from "react";

import { ClientsMenuButtons } from "./ClientsMenuButtons";

import { CardsContainer, MenuList } from "../../styles/styledComponents";
import { DropDownCard } from "../DropDownCard";

const ClientsPage: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query ClientQuery {
      allMarkdownRemark(sort: { fields: [frontmatter___title], order: ASC }) {
        edges {
          node {
            fields {
              slug
            }
            html
            frontmatter {
              alt
              client
              clientlogo
              description
              filter
              keywords
              slug
              title
            }
          }
        }
      }
    }
  `);

  const partnerInfo = data.allMarkdownRemark.edges.filter(
    (partnerCard): boolean => partnerCard.node.frontmatter.client === "yes"
  );

  return (
    <React.Fragment>
      <div className={"flex flex-nowrap"}>
        <MenuList>
          <ClientsMenuButtons />
        </MenuList>
      </div>
      <CardsContainer>
        {partnerInfo.map(
          ({ node }): JSX.Element => {
            const { alt, clientlogo, filter, slug, title } = node.frontmatter;

            return (
              <DropDownCard
                alt={alt}
                cardType={`all-clients-cards ${filter}-cards`}
                haveTitle={true}
                htmlData={node.html}
                key={slug}
                logo={clientlogo}
                logoPaths={"/airs/about-us/clients"}
                slug={slug}
                title={title}
              />
            );
          }
        )}
      </CardsContainer>
    </React.Fragment>
  );
};

export { ClientsPage };
