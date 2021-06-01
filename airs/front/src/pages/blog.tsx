/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogsList } from "../components/BlogsList";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import { PageArticle } from "../styles/styledComponents";
import { capitalizeCrumbs } from "../utils/capitalizeCrumbs";
import { translate } from "../utils/translations/translate";

const BlogIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const blogImage: string =
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.webp";

  return (
    <React.Fragment>
      <Seo
        description={translate.t("blog.description")}
        image={blogImage}
        keywords={translate.t("blog.keywords")}
        title={"Blog | A Pentesting Company | Fluid Attacks"}
        url={"https://fluidattacks.com/blog"}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <Breadcrumb
            crumbLabel={"Blog"}
            crumbSeparator={" / "}
            crumbs={capitalizeCrumbs(crumbs)}
          />
          <PageArticle>
            <PageHeader
              banner={"blog-bg"}
              pageWithBanner={true}
              slug={"blog/"}
              subtext={""}
              subtitle={""}
              title={"Blog"}
            />

            <BlogsList />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default BlogIndex;
