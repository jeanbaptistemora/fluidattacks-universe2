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
/* eslint react/forbid-component-props: 0 */
import { Link, graphql } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";
import type { StyledComponent } from "styled-components";
import styled from "styled-components";

import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import {
  BannerTitle,
  BlackH2,
  FullWidthContainer,
  LittleBannerContainer,
  PageArticle,
  RegularRedButton,
} from "../styles/styledComponents";
import { capitalizeObject } from "../utils/utilities";

const PlansIndex: React.FC<IQueryData> = ({
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
  const { banner } = data.asciidoc.pageAttributes;
  const PlansCards: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      flex
      flex-wrap
      justify-center
    `,
  })``;
  const PlansContainer: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      plans-feat
      roboto
      internal
      mw-1366
      ph-body
      ml-auto
      mr-auto
      roboto
      bg-white
      ph4-l
      ph3
      pt5-l
      pt4
      pb5
    `,
  })``;

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619635918/airs/about-us/clients/cover-clients_llnlaw.png"
        }
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
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle>
            <LittleBannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </LittleBannerContainer>

            <PlansContainer>
              <BlackH2 className={"pv5"}>
                {data.asciidoc.pageAttributes.phrase}
              </BlackH2>
              <PlansCards
                dangerouslySetInnerHTML={{
                  __html: data.asciidoc.html,
                }}
              />
              <div className={"tc pv3"}>
                <Link to={"/contact-us/"}>
                  <RegularRedButton>{"Inquire now"}</RegularRedButton>
                </Link>
              </div>
            </PlansContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default PlansIndex;

export const query: void = graphql`
  query PlansIndex($slug: String!) {
    asciidoc(fields: { slug: { eq: $slug } }) {
      document {
        title
      }
      html
      fields {
        slug
      }
      pageAttributes {
        description
        banner
        keywords
        phrase
        slug
      }
    }
  }
`;
