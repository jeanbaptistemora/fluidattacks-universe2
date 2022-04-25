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

import { AdviseCard } from "../components/AdviseCard";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import {
  AdvisoriesContainer,
  AdvisoriesGrid,
  BannerContainer,
  BannerTitle,
  FullWidthContainer,
  PageArticle,
  RegularRedButton,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const AdvisoriesIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { banner, description, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619634447/airs/bg-advisories_htsqyd.png"
        }
        keywords={keywords}
        title={`${title} | Fluid Attacks`}
        url={slug}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={capitalizePlainString(title)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle bgColor={"#dddde3"}>
            <BannerContainer className={banner}>
              <FullWidthContainer>
                <BannerTitle>{title}</BannerTitle>
              </FullWidthContainer>
            </BannerContainer>
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
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        description
        banner
        keywords
        slug
        title
      }
    }
  }
`;
