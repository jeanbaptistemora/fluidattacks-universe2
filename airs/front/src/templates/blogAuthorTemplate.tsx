import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogAuthorList } from "../components/BlogAuthorList";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import { PageArticle } from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeDashedString, capitalizeObject } from "../utils/utilities";

const blogAuthorIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { authorName } = pageContext;

  return (
    <React.Fragment>
      <Seo
        description={translate.t("blog.description")}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.png"
        }
        keywords={translate.t("blog.keywords")}
        title={`Blogs by ${capitalizeDashedString(
          authorName
        )} | A Pentesting Company | Fluid Attacks`}
        url={"https://fluidattacks.com/blog"}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <Breadcrumb
            crumbLabel={capitalizeDashedString(authorName)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />
          <PageArticle>
            <PageHeader
              banner={"blog-bg"}
              pageWithBanner={true}
              slug={`blog/authors/${authorName}`}
              subtext={""}
              subtitle={""}
              title={"Blog"}
            />

            <BlogAuthorList authorName={authorName} />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogAuthorIndex;
