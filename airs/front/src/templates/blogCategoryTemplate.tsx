import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogCategoryList } from "../components/BlogCategoryList";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import { PageArticle } from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject, capitalizePlainString } from "../utils/utilities";

const blogCategoryIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { categoryName } = pageContext;

  return (
    <React.Fragment>
      <Seo
        description={translate.t("blog.description")}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.png"
        }
        keywords={translate.t("blog.keywords")}
        title={`Blogs about ${capitalizePlainString(
          categoryName
        )} | A Pentesting Company | Fluid Attacks`}
        url={"https://fluidattacks.com/blog"}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <Breadcrumb
            crumbLabel={`${categoryName
              .charAt(0)
              .toUpperCase()}${categoryName.slice(1).replace("-", " ")}`}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />
          <PageArticle>
            <PageHeader
              banner={"blog-bg"}
              pageWithBanner={true}
              slug={"blog/tags/"}
              subtext={""}
              subtitle={""}
              title={"Blog"}
            />
            <BlogCategoryList categoryName={categoryName} />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogCategoryIndex;
