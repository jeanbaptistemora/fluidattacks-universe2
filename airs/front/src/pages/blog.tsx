/* eslint @typescript-eslint/no-invalid-void-type:0 */
/* eslint @typescript-eslint/no-confusing-void-expression:0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { Seo } from "../components/Seo";
import { BlogsPage } from "../scenes/BlogsPage";
import { Layout } from "../scenes/Footer/Layout";
import { NavbarComponent } from "../scenes/Menu";
import { PageArticle } from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject } from "../utils/utilities";

const BlogIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const blogImage: string =
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.png";

  return (
    <React.Fragment>
      <Seo
        description={translate.t("blog.description")}
        image={blogImage}
        keywords={translate.t("blog.keywords")}
        title={"Blog | Application security testing solutions | Fluid Attacks"}
        url={"https://fluidattacks.com/blog"}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={"Blog"}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />
          <PageArticle bgColor={"#dddde3"}>
            <BlogsPage />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default BlogIndex;
