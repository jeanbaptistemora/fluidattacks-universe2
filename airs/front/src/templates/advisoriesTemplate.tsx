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

import { AdviseCard } from "../components/AdviseCard";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import {
  BannerTitle,
  FullWidthContainer,
  LittleBannerContainer,
  PageArticle,
  RegularRedButton,
} from "../styles/styledComponents";
import { capitalizeCrumbs } from "../utils/capitalizeCrumbs";
import { translate } from "../utils/translations/translate";

const AdvisoriesIndex: React.FC<IQueryData> = ({
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
  const AdvisoriesGrid: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
    advisories-grid
    center
    grid
    mt4
  `,
  })``;
  const AdvisoriesContainer: StyledComponent<
    "div",
    Record<string, unknown>
  > = styled.div.attrs({
    className: `
      w-100
      tc
      mb4
    `,
  })``;

  return (
    <React.Fragment>
      <Seo
        description={data.asciidoc.pageAttributes.description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619634447/airs/bg-advisories_htsqyd.png"
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
            crumbs={capitalizeCrumbs(crumbs)}
          />

          <PageArticle>
            <LittleBannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </LittleBannerContainer>
            <div className={"flex"}>
              <AdvisoriesGrid>
                <AdviseCard />
              </AdvisoriesGrid>
            </div>
            <AdvisoriesContainer>
              <h4 className={"f3 roboto"}>{`${translate.t(
                "advisories.disclosurePhrase"
              )} `}</h4>
              <Link to={"/advisories/policy"}>
                <RegularRedButton>{`${translate.t(
                  "advisories.buttonPhrase"
                )} `}</RegularRedButton>
              </Link>
            </AdvisoriesContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default AdvisoriesIndex;

export const query: void = graphql`
  query AdvisoriesIndex($slug: String!) {
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
        slug
      }
    }
  }
`;
