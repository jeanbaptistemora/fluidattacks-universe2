/* eslint react/forbid-component-props: 0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogSeo } from "../components/BlogSeo";
import { BlogTagList } from "../components/BlogTagList";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { Paragraph, Title } from "../components/Texts";
import {
  BlogPageArticle,
  CenteredMaxWidthContainer,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

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
      description: translate.t("blogListTags.company.description"),
      metaDescription: translate.t("blogListTags.company.metaDescription"),
      title: translate.t("blogListTags.company.title"),
    },
    {
      description: translate.t("blogListTags.cybersecurity.description"),
      metaDescription: translate.t(
        "blogListTags.cybersecurity.metaDescription"
      ),
      title: translate.t("blogListTags.cybersecurity.title"),
    },
    {
      description: translate.t("blogListTags.risk.description"),
      metaDescription: translate.t("blogListTags.risk.metaDescription"),
      title: translate.t("blogListTags.risk.title"),
    },
    {
      description: translate.t("blogListTags.software.description"),
      metaDescription: translate.t("blogListTags.software.metaDescription"),
      title: translate.t("blogListTags.software.title"),
    },
    {
      description: translate.t("blogListTags.vulnerability.description"),
      metaDescription: translate.t(
        "blogListTags.vulnerability.metaDescription"
      ),
      title: translate.t("blogListTags.vulnerability.title"),
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
        description={translate.t("blog.description")}
        image={blogImage}
        keywords={translate.t("blog.keywords")}
        title={`Blogs about ${capitalizePlainString(
          tagName
        )} | A Pentesting Company | Fluid Attacks`}
        url={"https://fluidattacks.com/blog"}
      />
      <BlogSeo
        description={
          metaDescription === undefined
            ? translate.t("blog.description")
            : metaDescription
        }
        image={blogImage}
        title={"Blog | A Pentesting Company | Fluid Attacks"}
        url={"https://fluidattacks.com/blog"}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <Breadcrumb
            crumbLabel={tagName}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />
          <BlogPageArticle>
            <CenteredMaxWidthContainer className={"tc"}>
              <Title fColor={"#2e2e38"} fSize={"48"} marginBottom={"2"}>
                {tagName.charAt(0).toUpperCase() + tagName.slice(1)}
              </Title>
              {tagDescription === undefined ? undefined : (
                <Paragraph fColor={"#2e2e38"} fSize={"24"}>
                  {tagDescription}
                </Paragraph>
              )}
            </CenteredMaxWidthContainer>
            <BlogTagList tagName={tagName} />
          </BlogPageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogTagTemplate;
