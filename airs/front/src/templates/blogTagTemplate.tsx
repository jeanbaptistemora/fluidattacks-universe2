/* eslint react/forbid-component-props: 0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogSeo } from "../components/BlogSeo";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { BlogsToFilterPage } from "../scenes/BlogsToFilterPage";
import { PageArticle } from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeDashedString, capitalizeObject } from "../utils/utilities";

const blogTagTemplate: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { tagName } = pageContext;
  const blogImage: string =
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.png";

  const data = [
    {
      description: translate.t("blogListTags.blueTeam.description"),
      metaDescription: translate.t("blogListTags.blueTeam.metaDescription"),
      title: translate.t("blogListTags.blueTeam.title"),
    },
    {
      description: translate.t("blogListTags.cloud.description"),
      metaDescription: translate.t("blogListTags.cloud.metaDescription"),
      title: translate.t("blogListTags.cloud.title"),
    },
    {
      description: translate.t("blogListTags.code.description"),
      metaDescription: translate.t("blogListTags.code.metaDescription"),
      title: translate.t("blogListTags.code.title"),
    },
    {
      description: translate.t("blogListTags.company.description"),
      metaDescription: translate.t("blogListTags.company.metaDescription"),
      title: translate.t("blogListTags.company.title"),
    },
    {
      description: translate.t("blogListTags.compliance.description"),
      metaDescription: translate.t("blogListTags.compliance.metaDescription"),
      title: translate.t("blogListTags.compliance.title"),
    },
    {
      description: translate.t("blogListTags.credential.description"),
      metaDescription: translate.t("blogListTags.credential.metaDescription"),
      title: translate.t("blogListTags.credential.title"),
    },
    {
      description: translate.t("blogListTags.cryptography.description"),
      metaDescription: translate.t("blogListTags.cryptography.metaDescription"),
      title: translate.t("blogListTags.cryptography.title"),
    },
    {
      description: translate.t("blogListTags.cybersecurity.description"),
      metaDescription: translate.t(
        "blogListTags.cybersecurity.metaDescription"
      ),
      title: translate.t("blogListTags.cybersecurity.title"),
    },
    {
      description: translate.t("blogListTags.devsecops.description"),
      metaDescription: translate.t("blogListTags.devsecops.metaDescription"),
      title: translate.t("blogListTags.devsecops.title"),
    },
    {
      description: translate.t("blogListTags.exploit.description"),
      metaDescription: translate.t("blogListTags.exploit.metaDescription"),
      title: translate.t("blogListTags.exploit.title"),
    },
    {
      description: translate.t("blogListTags.hacking.description"),
      metaDescription: translate.t("blogListTags.hacking.metaDescription"),
      title: translate.t("blogListTags.hacking.title"),
    },
    {
      description: translate.t("blogListTags.machineLearning.description"),
      metaDescription: translate.t(
        "blogListTags.machineLearning.metaDescription"
      ),
      title: translate.t("blogListTags.machineLearning.title"),
    },
    {
      description: translate.t("blogListTags.malware.description"),
      metaDescription: translate.t("blogListTags.malware.metaDescription"),
      title: translate.t("blogListTags.malware.title"),
    },
    {
      description: translate.t("blogListTags.pentesting.description"),
      metaDescription: translate.t("blogListTags.pentesting.metaDescription"),
      title: translate.t("blogListTags.pentesting.title"),
    },
    {
      description: translate.t("blogListTags.redTeam.description"),
      metaDescription: translate.t("blogListTags.redTeam.metaDescription"),
      title: translate.t("blogListTags.redTeam.title"),
    },
    {
      description: translate.t("blogListTags.risk.description"),
      metaDescription: translate.t("blogListTags.risk.metaDescription"),
      title: translate.t("blogListTags.risk.title"),
    },
    {
      description: translate.t("blogListTags.securityTesting.description"),
      metaDescription: translate.t(
        "blogListTags.securityTesting.metaDescription"
      ),
      title: translate.t("blogListTags.securityTesting.title"),
    },
    {
      description: translate.t("blogListTags.socialEngineering.description"),
      metaDescription: translate.t(
        "blogListTags.socialEngineering.metaDescription"
      ),
      title: translate.t("blogListTags.socialEngineering.title"),
    },
    {
      description: translate.t("blogListTags.software.description"),
      metaDescription: translate.t("blogListTags.software.metaDescription"),
      title: translate.t("blogListTags.software.title"),
    },
    {
      description: translate.t("blogListTags.standard.description"),
      metaDescription: translate.t("blogListTags.standard.metaDescription"),
      title: translate.t("blogListTags.standard.title"),
    },
    {
      description: translate.t("blogListTags.training.description"),
      metaDescription: translate.t("blogListTags.training.metaDescription"),
      title: translate.t("blogListTags.training.title"),
    },
    {
      description: translate.t("blogListTags.trend.description"),
      metaDescription: translate.t("blogListTags.trend.metaDescription"),
      title: translate.t("blogListTags.trend.title"),
    },
    {
      description: translate.t("blogListTags.vulnerability.description"),
      metaDescription: translate.t(
        "blogListTags.vulnerability.metaDescription"
      ),
      title: translate.t("blogListTags.vulnerability.title"),
    },
    {
      description: translate.t("blogListTags.vulnserver.description"),
      metaDescription: translate.t("blogListTags.vulnserver.metaDescription"),
      title: translate.t("blogListTags.vulnserver.title"),
    },
    {
      description: translate.t("blogListTags.web.description"),
      metaDescription: translate.t("blogListTags.web.metaDescription"),
      title: translate.t("blogListTags.web.title"),
    },
    {
      description: translate.t("blogListTags.windows.description"),
      metaDescription: translate.t("blogListTags.windows.metaDescription"),
      title: translate.t("blogListTags.windows.title"),
    },
  ];

  const tagDescription = data.find(
    (tag): boolean => tag.title === tagName
  )?.description;

  const metaDescription = data.find(
    (tag): boolean => tag.title === tagName
  )?.metaDescription;

  return (
    <React.Fragment>
      <Seo
        description={
          metaDescription === undefined
            ? translate.t("blog.description")
            : metaDescription
        }
        image={blogImage}
        keywords={translate.t("blog.keywords")}
        title={`Blogs about ${capitalizeDashedString(
          tagName
        )} | Application security testing solutions | Fluid Attacks`}
        url={`https://fluidattacks.com/blog/tags/${tagName}`}
      />
      <BlogSeo
        description={
          metaDescription === undefined
            ? translate.t("blog.description")
            : metaDescription
        }
        image={blogImage}
        title={"Blog | Application security testing solutions | Fluid Attacks"}
        url={"https://fluidattacks.com/blog"}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <Breadcrumb
            crumbLabel={capitalizeDashedString(tagName)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />
          <PageArticle bgColor={"transparent"}>
            <BlogsToFilterPage
              description={tagDescription}
              filterBy={"tag"}
              value={tagName}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogTagTemplate;
