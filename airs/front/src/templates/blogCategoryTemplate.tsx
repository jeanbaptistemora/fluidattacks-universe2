/* eslint react/forbid-component-props: 0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogSeo } from "../components/BlogSeo";
import { Seo } from "../components/Seo";
import { BlogsToFilterPage } from "../scenes/BlogsToFilterPage";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import { PageArticle } from "../styles/styledComponents";
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
        title={`Blog posts about ${capitalizePlainString(
          categoryName
        )} | Application security testing solutions | Fluid Attacks`}
        url={`https://fluidattacks.com/blog/categories/${categoryName}`}
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
            crumbLabel={capitalizePlainString(categoryName)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />
          <PageArticle bgColor={"transparent"}>
            <BlogsToFilterPage
              description={categoryDescription}
              filterBy={"category"}
              value={categoryName}
            />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogCategoryTemplate;
