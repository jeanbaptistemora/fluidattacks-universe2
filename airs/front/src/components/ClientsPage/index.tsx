/* eslint @typescript-eslint/no-confusing-void-expression:0 */
/* eslint react/forbid-component-props: 0 */
import {
  faChevronLeft,
  faChevronRight,
} from "@fortawesome/pro-regular-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { graphql, useStaticQuery } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { ClientsMenuButtons } from "./ClientsMenuButtons";

import { CardsContainer } from "../../styles/styledComponents";
import { DropDownCard } from "../DropDownCard";

const MenuList: StyledComponent<
  "ul",
  Record<string, unknown>
> = styled.ul.attrs({
  className: `
      list
      ph0-ns
      ph3
      ma0
      tc
      pv3
      overflow-x-auto
      nowrap
      slide-show
    `,
})``;

const ClientsPage: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query ClientQuery {
      allAsciidoc(sort: { fields: [document___title], order: ASC }) {
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
              client
              clientlogo
              description
              filter
              keywords
              slug
            }
          }
        }
      }
    }
  `);

  const partnerInfo = data.allAsciidoc.edges.filter(
    (partnerCard): boolean => partnerCard.node.pageAttributes.client === "yes"
  );

  return (
    <React.Fragment>
      <div className={"flex flex-nowrap"}>
        <FontAwesomeIcon
          className={"arrow w1 pv3 mv1 mh2"}
          icon={faChevronLeft}
        />
        <MenuList>
          <ClientsMenuButtons />
        </MenuList>
        <FontAwesomeIcon
          className={"arrow w1 pv3 mv1 mh2"}
          icon={faChevronRight}
        />
      </div>
      <CardsContainer>
        {partnerInfo.map(
          ({ node }): JSX.Element => {
            const { alt, clientlogo, filter, slug } = node.pageAttributes;

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
                title={node.document.title}
              />
            );
          }
        )}
      </CardsContainer>
    </React.Fragment>
  );
};

export { ClientsPage };
