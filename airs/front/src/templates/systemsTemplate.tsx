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
/* eslint import/no-namespace:0 */
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

const SystemsIndex: React.FC<IQueryData> = ({
  data,
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { description, keywords, slug, title } =
    data.markdownRemark.frontmatter;

  const systemData = [
    {
      image: "web-applications",
      link: "/systems/web-apps/",
      paragraph: translate.t("systems.webApps.paragraph"),
      title: translate.t("systems.webApps.title"),
    },
    {
      image: "mobile-apps",
      link: "/systems/mobile-apps/",
      paragraph: translate.t("systems.mobileApps.paragraph"),
      title: translate.t("systems.mobileApps.title"),
    },
    {
      image: "thick-clients",
      link: "/systems/thick-clients/",
      paragraph: translate.t("systems.thickClients.paragraph"),
      title: translate.t("systems.thickClients.title"),
    },
    {
      image: "apis",
      link: "/systems/apis/",
      paragraph: translate.t("systems.apis.paragraph"),
      title: translate.t("systems.apis.title"),
    },
    {
      image: "cloud",
      link: "/systems/cloud-infrastructure/",
      paragraph: translate.t("systems.cloud.paragraph"),
      title: translate.t("systems.cloud.title"),
    },
    {
      image: "networks",
      link: "/systems/networks-and-hosts/",
      paragraph: translate.t("systems.networks.paragraph"),
      title: translate.t("systems.networks.title"),
    },
    {
      image: "iot",
      link: "/systems/iot/",
      paragraph: translate.t("systems.iot.paragraph"),
      title: translate.t("systems.iot.title"),
    },
    {
      image: "scada",
      link: "/systems/ot/",
      paragraph: translate.t("systems.scada.paragraph"),
      title: translate.t("systems.scada.title"),
    },
    {
      image: "containers",
      link: "/systems/containers/",
      paragraph: translate.t("systems.containers.paragraph"),
      title: translate.t("systems.containers.title"),
    },
  ];

  return (
    <React.Fragment>
      <Seo
        description={description}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619630822/airs/solutions/bg-solutions_ylz99o.png"
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
              {systemData.map((systemCard): JSX.Element => {
                return (
                  <SystemsCardContainer key={systemCard.title}>
                    <CloudImage
                      alt={title}
                      src={`airs/systems/${systemCard.image}`}
                      styles={"w-100"}
                    />
                    <Title
                      fColor={"#2e2e38"}
                      fSize={"24"}
                      marginBottom={"1"}
                      marginTop={"1"}
                    >
                      {systemCard.title}
                    </Title>
                    <Paragraph
                      fColor={"#5c5c70"}
                      fSize={"16"}
                      marginBottom={"1"}
                    >
                      {systemCard.paragraph}
                    </Paragraph>
                    <Link to={systemCard.link}>
                      <PhantomRegularRedButton>
                        {"Go to system"}
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

export default SystemsIndex;

export const query: StaticQueryDocument = graphql`
  query SystemsIndex($slug: String!) {
    markdownRemark(fields: { slug: { eq: $slug } }) {
      html
      fields {
        slug
      }
      frontmatter {
        banner
        description
        keywords
        slug
        title
      }
    }
  }
`;
