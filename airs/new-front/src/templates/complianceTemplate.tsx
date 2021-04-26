/*
 *There is no danger using dangerouslySetInnerHTML since everything is built in
 *compile time, also
 *Default exports are needed for pages used in nodes by default to create pages
 *like index.tsx or this one
 */
/* eslint react/no-danger:0 */
/* eslint import/no-default-export:0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import {
  MarkedPhrase,
  MarkedTitle,
  MarkedTitleContainer,
  RedMark,
} from "../styles/styledComponents";

const ComplianceIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { title } = data.asciidoc.document;
  const customCrumbLabel: string = `${title
    .charAt(0)
    .toUpperCase()}${title.slice(1).replace("-", "")}`;
  const ComplianceGrid: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      grid 
      compliance-content 
      compliance-grid 
      roboto 
      w-100
    `,
  })``;

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        keywords={data.asciidoc.pageAttributes.keywords}
        title={`${title} | Fluid Attacks`}
        url={data.asciidoc.pageAttributes.slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={customCrumbLabel}
            crumbSeparator={" / "}
            crumbs={crumbs}
          />
          <MarkedTitleContainer>
            <div className={"pl4"}>
              <RedMark>
                <MarkedTitle>{title}</MarkedTitle>
              </RedMark>
              <MarkedPhrase>{data.asciidoc.pageAttributes.phrase}</MarkedPhrase>
            </div>
            <ComplianceGrid
              dangerouslySetInnerHTML={{
                __html: data.asciidoc.html,
              }}
            />
          </MarkedTitleContainer>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default ComplianceIndex;

export const query: void = graphql`
  query ComplianceIndex($slug: String!) {
    asciidoc(fields: { slug: { eq: $slug } }) {
      document {
        title
      }
      html
      fields {
        slug
      }
      pageAttributes {
        banner
        definition
        description
        keywords
        phrase
        slug
      }
    }
  }
`;
