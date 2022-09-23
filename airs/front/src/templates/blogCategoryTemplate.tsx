/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props: 0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogCategoryList } from "../components/BlogCategoryList";
import { BlogSeo } from "../components/BlogSeo";
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

const blogCategoryTemplate: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { categoryName } = pageContext;
  const blogImage: string =
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.png";

  const data = [
    {
      description: translate.t("blogListCategories.attacks.description"),
      metaDescription: translate.t(
        "blogListCategories.attacks.metaDescription"
      ),
      title: translate.t("blogListCategories.attacks.title"),
    },
    {
      description: translate.t("blogListCategories.development.description"),
      metaDescription: translate.t(
        "blogListCategories.development.metaDescription"
      ),
      title: translate.t("blogListCategories.development.title"),
    },
    {
      description: translate.t("blogListCategories.interview.description"),
      metaDescription: translate.t(
        "blogListCategories.interview.metaDescription"
      ),
      title: translate.t("blogListCategories.interview.title"),
    },
    {
      description: translate.t("blogListCategories.opinions.description"),
      metaDescription: translate.t(
        "blogListCategories.opinions.metaDescription"
      ),
      title: translate.t("blogListCategories.opinions.title"),
    },
    {
      description: translate.t("blogListCategories.philosophy.description"),
      metaDescription: translate.t(
        "blogListCategories.philosophy.metaDescription"
      ),
      title: translate.t("blogListCategories.philosophy.title"),
    },
    {
      description: translate.t("blogListCategories.politics.description"),
      metaDescription: translate.t(
        "blogListCategories.politics.metaDescription"
      ),
      title: translate.t("blogListCategories.politics.title"),
    },
  ];

  const categoryDescription = data.find(
    (category): boolean => category.title === categoryName
  )?.description;

  const metaDescription = data.find(
    (category): boolean => category.title === categoryName
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
        title={`Blogs about ${capitalizePlainString(
          categoryName
        )} | A Pentesting Company | Fluid Attacks`}
        url={`https://fluidattacks.com/blog/categories/${categoryName}`}
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
            crumbLabel={`${categoryName.charAt(0).toUpperCase()}${categoryName
              .slice(1)
              .replace("-", " ")}`}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />
          <BlogPageArticle>
            <CenteredMaxWidthContainer className={"tc"}>
              <Title fColor={"#2e2e38"} fSize={"48"} marginBottom={"2"}>
                {categoryName.charAt(0).toUpperCase() + categoryName.slice(1)}
              </Title>
              {categoryDescription === undefined ? undefined : (
                <Paragraph fColor={"#2e2e38"} fSize={"24"}>
                  {categoryDescription}
                </Paragraph>
              )}
            </CenteredMaxWidthContainer>
            <BlogCategoryList categoryName={categoryName} />
          </BlogPageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogCategoryTemplate;
