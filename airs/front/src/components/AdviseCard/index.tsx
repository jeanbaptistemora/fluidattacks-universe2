/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Link, graphql, useStaticQuery } from "gatsby";
import React from "react";

import {
  AdvisoriesCardBack,
  AdvisoriesCardBackItem,
  AdvisoriesCardBackList,
  AdvisoriesCardFront,
  AdvisoriesCardFrontAuthorContainer,
  AdvisoriesCardFrontDesc,
  AdvisoriesCardFrontTitle,
  AdvisoriesShadowBoxContainer,
} from "./styles/styledComponents";

import { RegularRedButton } from "../../styles/styledComponents";
import { CloudImage } from "../CloudImage";

const AdviseCard: React.FC = (): JSX.Element => {
  const data: IData = useStaticQuery(graphql`
    query AdviseQuery {
      allMarkdownRemark(sort: { fields: [frontmatter___date], order: DESC }) {
        edges {
          node {
            fields {
              slug
            }
            frontmatter {
              advise
              authors
              codename
              cveid
              date
              description
              product
              slug
              title
              writer
            }
          }
        }
      }
    }
  `);

  const adviseInfo = data.allMarkdownRemark.edges.filter(
    (advisePages): boolean => advisePages.node.frontmatter.advise === "yes"
  );

  return (
    <React.StrictMode>
      {adviseInfo.map((advisePage): JSX.Element => {
        const {
          authors,
          codename,
          cveid,
          date,
          description,
          product,
          slug,
          writer,
        } = advisePage.node.frontmatter;

        return (
          <AdvisoriesShadowBoxContainer key={date}>
            <AdvisoriesCardFront>
              <AdvisoriesCardFrontTitle>
                {"VULNERABILITY"}
              </AdvisoriesCardFrontTitle>
              <AdvisoriesCardFrontDesc>{description}</AdvisoriesCardFrontDesc>
              <br />
              <AdvisoriesCardFrontAuthorContainer>
                <CloudImage
                  alt={"Author picture"}
                  src={`authors/${writer}`}
                  styles={"br-100 mr3 w-10"}
                />
                <p className={"roboto"}>{authors}</p>
                <br />
              </AdvisoriesCardFrontAuthorContainer>
            </AdvisoriesCardFront>
            <AdvisoriesCardBack>
              <AdvisoriesCardBackList>
                <AdvisoriesCardBackItem>
                  {`Code name: ${codename}`}
                </AdvisoriesCardBackItem>
                <AdvisoriesCardBackItem>
                  {`Product: ${product}`}
                </AdvisoriesCardBackItem>
                <AdvisoriesCardBackItem>
                  {`Release date: ${date}`}
                </AdvisoriesCardBackItem>
                <AdvisoriesCardBackItem>
                  {`CVE ID(s): ${cveid}`}
                </AdvisoriesCardBackItem>
              </AdvisoriesCardBackList>
              <Link to={`/${slug}`}>
                <RegularRedButton>{"Read More"}</RegularRedButton>
              </Link>
            </AdvisoriesCardBack>
          </AdvisoriesShadowBoxContainer>
        );
      })}
    </React.StrictMode>
  );
};

export { AdviseCard };
