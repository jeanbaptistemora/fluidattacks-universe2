import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogSeo } from "../components/BlogSeo";
import { BlogTagList } from "../components/BlogTagList";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { Seo } from "../components/Seo";
import { Title } from "../components/Texts";
import {
  BlogPageArticle,
  FlexCenterItemsContainer,
} from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";
import { capitalizeObject } from "../utils/utilities";

const blogTagTemplate: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { tagName } = pageContext;
  const blogImage: string =
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.png";

  return (
    <React.Fragment>
      <Seo
        description={translate.t("blog.description")}
        image={blogImage}
        keywords={translate.t("blog.keywords")}
        title={`Blogs about ${tagName} | A Pentesting Company | Fluid Attacks`}
        url={"https://fluidattacks.com/blog"}
      />
      <BlogSeo
        description={translate.t("blog.description")}
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
            <FlexCenterItemsContainer>
              <Title fColor={"#2e2e38"} fSize={"48"} marginBottom={"2"}>
                {tagName.charAt(0).toUpperCase() + tagName.slice(1)}
              </Title>
            </FlexCenterItemsContainer>
            <BlogTagList tagName={tagName} />
          </BlogPageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogTagTemplate;
