/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Link, graphql, useStaticQuery } from "gatsby";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { RegularRedButton } from "../../styles/styledComponents";
import { CloudImage } from "../CloudImage";

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
          pageAttributes: {
            advise: string;
            authors: string;
            codename: string;
            cveid: string;
            date: string;
            description: string;
            product: string;
            slug: string;
            writer: string;
          };
        };
      }
    ];
  };
}

const AdviseCard: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query AdviseQuery {
      allAsciidoc(sort: { fields: [pageAttributes___date], order: DESC }) {
        edges {
          node {
            fields {
              slug
            }
            document {
              title
            }
            pageAttributes {
              advise
              authors
              codename
              cveid
              date
              description
              product
              slug
              writer
            }
          }
        }
      }
    }
  `);

  const adviseInfo = data.allAsciidoc.edges.filter(
    (advisePages): boolean => advisePages.node.pageAttributes.advise === "yes"
  );
  const AdvisoriesShadowBoxContainer: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
    br3
    dib
    f-1125
    lh-copy
    mb4
    mh4
    relative
    bs-btm-h-10
  `,
  })``;
  const AdvisoriesCardFront: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
    bg-white
    br3
    h-100
    pa4
    tl
  `,
  })``;
  const AdvisoriesCardFrontTitle: StyledComponent<
    "p",
    Record<string, unknown>
  > = styled.p.attrs({
    className: `
    f6
    shadow-gray
    tracked
    roboto
  `,
  })``;
  const AdvisoriesCardFrontDesc: StyledComponent<
    "h4",
    Record<string, unknown>
  > = styled.h4.attrs({
    className: `
    f3
    mv0
    neue
  `,
  })``;
  const AdvisoriesCardFrontAuthorContainer: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
    items-center
    flex
  `,
  })``;
  const AdvisoriesCardBack: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
    absolute 
    advisor-animation
    advisor-transition
    bg-white
    br3
    left-0
    pa4
    tc
    top-0
    h-100
  `,
  })``;
  const AdvisoriesCardBackList: StyledComponent<
    "ul",
    Record<string, unknown>
  > = styled.ul.attrs({
    className: `
    list
    ma0
    pa0
  `,
  })``;
  const AdvisoriesCardBackItem: StyledComponent<
    "li",
    Record<string, unknown>
  > = styled.li.attrs({
    className: `
    dib
    f-1125
    lh-2
    relative
    tl
    w-100
    roboto
  `,
  })``;

  return (
    <React.StrictMode>
      {adviseInfo.map(
        (advisePage): JSX.Element => (
          <AdvisoriesShadowBoxContainer
            key={advisePage.node.pageAttributes.date}
          >
            <AdvisoriesCardFront>
              <AdvisoriesCardFrontTitle>
                {"VULNERABILITY"}
              </AdvisoriesCardFrontTitle>
              <AdvisoriesCardFrontDesc>
                {advisePage.node.pageAttributes.description}
              </AdvisoriesCardFrontDesc>
              <br />
              <AdvisoriesCardFrontAuthorContainer>
                <CloudImage
                  alt={"Author picture"}
                  src={`authors/${advisePage.node.pageAttributes.writer}`}
                  styles={"br-100 mr3 w-10"}
                />
                <p className={"roboto"}>
                  {advisePage.node.pageAttributes.authors}
                </p>
                <br />
              </AdvisoriesCardFrontAuthorContainer>
            </AdvisoriesCardFront>
            <AdvisoriesCardBack>
              <AdvisoriesCardBackList>
                <AdvisoriesCardBackItem>
                  {`Code name: ${advisePage.node.pageAttributes.codename}`}
                </AdvisoriesCardBackItem>
                <AdvisoriesCardBackItem>
                  {`Product: ${advisePage.node.pageAttributes.product}`}
                </AdvisoriesCardBackItem>
                <AdvisoriesCardBackItem>
                  {`Release date: ${advisePage.node.pageAttributes.date}`}
                </AdvisoriesCardBackItem>
                <AdvisoriesCardBackItem>
                  {`CVE ID(s): ${advisePage.node.pageAttributes.cveid}`}
                </AdvisoriesCardBackItem>
              </AdvisoriesCardBackList>
              <Link to={`/${advisePage.node.pageAttributes.slug}`}>
                <RegularRedButton>{"Read More"}</RegularRedButton>
              </Link>
            </AdvisoriesCardBack>
          </AdvisoriesShadowBoxContainer>
        )
      )}
    </React.StrictMode>
  );
};

export { AdviseCard };
