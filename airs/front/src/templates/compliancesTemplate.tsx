/*
 *There is no danger using dangerouslySetInnerHTML since everything is built in
 *compile time, also
 *Default exports are needed for pages used in nodes by default to create pages
 *like index.tsx or this one
 */
/* eslint react/no-danger:0 */
/* eslint import/no-default-export:0 */
/* eslint react/forbid-component-props: 0 */
/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Link, graphql } from "gatsby";
import type { StaticQueryDocument } from "gatsby";
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { CloudImage } from "../components/CloudImage";
import { Seo } from "../components/Seo";
import { Paragraph, Title } from "../components/Texts";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import {
  FlexCenterItemsContainer,
  PageArticle,
  PageContainer,
  PhantomRegularRedButton,
  SystemsCardContainer,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const CompliancesIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  const complianceData = [
    {
      image: "owasp",
      link: "/compliance/owasp/",
      paragraph: translate.t("compliances.owasp.paragraph"),
      title: translate.t("compliances.owasp.subtitle"),
    },
    {
      image: "pci",
      link: "/compliance/pci/",
      paragraph: translate.t("compliances.pci.paragraph"),
      title: translate.t("compliances.pci.subtitle"),
    },
    {
      image: "hipaa",
      link: "/compliance/hipaa/",
      paragraph: translate.t("compliances.hipaa.paragraph"),
      title: translate.t("compliances.hipaa.subtitle"),
    },
    {
      image: "nist",
      link: "/compliance/nist/",
      paragraph: translate.t("compliances.nist.paragraph"),
      title: translate.t("compliances.nist.subtitle"),
    },
    {
      image: "gdpr",
      link: "/compliance/gdpr/",
      paragraph: translate.t("compliances.gdpr.paragraph"),
      title: translate.t("compliances.gdpr.subtitle"),
    },
    {
      image: "cve",
      link: "/compliance/cve/",
      paragraph: translate.t("compliances.cve.paragraph"),
      title: translate.t("compliances.cve.subtitle"),
    },
    {
      image: "cwe",
      link: "/compliance/cwe/",
      paragraph: translate.t("compliances.cwe.paragraph"),
      title: translate.t("compliances.cwe.subtitle"),
    },
  ];

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619637251/airs/compliance/cover-compliance_vnojb7.png"
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

          <PageArticle bgColor={"#f4f4f6"}>
            <FlexCenterItemsContainer>
              <Title fColor={"#2e2e38"} fSize={"48"} marginTop={"4"}>
                {title}
              </Title>
            </FlexCenterItemsContainer>
            <PageContainer className={"flex flex-wrap"}>
              {complianceData.map((complianceCard): JSX.Element => {
                return (
                  <SystemsCardContainer key={complianceCard.title}>
                    <CloudImage
                      alt={title}
                      src={`airs/compliance/${complianceCard.image}`}
                      styles={"w-100"}
                    />
                    <Title
                      fColor={"#2e2e38"}
                      fSize={"24"}
                      marginBottom={"1"}
                      marginTop={"1"}
                    >
                      {complianceCard.title}
                    </Title>
                    <Paragraph
                      fColor={"#5c5c70"}
                      fSize={"16"}
                      marginBottom={"1"}
                    >
                      {complianceCard.paragraph}
                    </Paragraph>
                    <Link to={complianceCard.link}>
                      <PhantomRegularRedButton>
                        {"Read more"}
                      </PhantomRegularRedButton>
                    </Link>
                  </SystemsCardContainer>
                );
              })}
            </PageContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

export default CompliancesIndex;

export const query: StaticQueryDocument = graphql`
  query CompliancesIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        description
        banner
        keywords
        phrase
        slug
        title
      }
    }
  }
`;
