import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogTagList } from "../components/BlogTagList";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import { PageArticle } from "../styles/styledComponents";
import { capitalizeCrumbs } from "../utils/capitalizeCrumbs";
import { translate } from "../utils/translations/translate";

const blogTagIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { tagName } = pageContext;

  return (
    <React.Fragment>
      <Seo
        description={translate.t("blog.description")}
        image={
          "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.webp"
        }
        keywords={translate.t("blog.keywords")}
        title={`Blogs about ${tagName} | A Pentesting Company | Fluid Attacks`}
        url={"https://fluidattacks.com/blog"}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <Breadcrumb
            crumbLabel={tagName}
            crumbSeparator={" / "}
            crumbs={capitalizeCrumbs(crumbs)}
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

            <BlogTagList tagName={tagName} />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogTagIndex;
