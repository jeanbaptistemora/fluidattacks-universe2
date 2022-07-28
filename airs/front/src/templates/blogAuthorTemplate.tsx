/* eslint react/forbid-component-props: 0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogAuthorList } from "../components/BlogAuthorList";
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
import { capitalizeDashedString, capitalizeObject } from "../utils/utilities";

const blogAuthorTemplate: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { authorName } = pageContext;
  const blogImage: string =
    "https://res.cloudinary.com/fluid-attacks/image/upload/v1619632208/airs/bg-blog_bj0szx.png";

  const data = [
    {
      description: translate.t("blogListAuthors.andresRoldan.description"),
      metaDescription: translate.t(
        "blogListAuthors.andresRoldan.metaDescription"
      ),
      title: translate.t("blogListAuthors.andresRoldan.title"),
    },
    {
      description: translate.t("blogListAuthors.felipeRuiz.description"),
      metaDescription: translate.t(
        "blogListAuthors.felipeRuiz.metaDescription"
      ),
      title: translate.t("blogListAuthors.felipeRuiz.title"),
    },
    {
      description: translate.t("blogListAuthors.felipeZarate.description"),
      metaDescription: translate.t(
        "blogListAuthors.felipeZarate.metaDescription"
      ),
      title: translate.t("blogListAuthors.felipeZarate.title"),
    },
    {
      description: translate.t("blogListAuthors.jasonChavarria.description"),
      metaDescription: translate.t(
        "blogListAuthors.jasonChavarria.metaDescription"
      ),
      title: translate.t("blogListAuthors.jasonChavarria.title"),
    },
    {
      description: translate.t("blogListAuthors.jonathanArmas.description"),
      metaDescription: translate.t(
        "blogListAuthors.jonathanArmas.metaDescription"
      ),
      title: translate.t("blogListAuthors.jonathanArmas.title"),
    },
    {
      description: translate.t("blogListAuthors.julianArango.description"),
      metaDescription: translate.t(
        "blogListAuthors.julianArango.metaDescription"
      ),
      title: translate.t("blogListAuthors.julianArango.title"),
    },
    {
      description: translate.t("blogListAuthors.oscarPrado.description"),
      metaDescription: translate.t(
        "blogListAuthors.oscarPrado.metaDescription"
      ),
      title: translate.t("blogListAuthors.oscarPrado.title"),
    },
    {
      description: translate.t("blogListAuthors.rafaelBallestas.description"),
      metaDescription: translate.t(
        "blogListAuthors.rafaelBallestas.metaDescription"
      ),
      title: translate.t("blogListAuthors.rafaelBallestas.title"),
    },
    {
      description: translate.t("blogListAuthors.rafaelAlvarez.description"),
      metaDescription: translate.t(
        "blogListAuthors.rafaelAlvarez.metaDescription"
      ),
      title: translate.t("blogListAuthors.rafaelAlvarez.title"),
    },
  ];

  const authorDescription = data.find(
    (tag): boolean => tag.title === authorName
  )?.description;

  const metaDescription = data.find(
    (tag): boolean => tag.title === authorName
  )?.metaDescription;

  return (
    <React.Fragment>
      <Seo
        description={translate.t("blog.description")}
        image={blogImage}
        keywords={translate.t("blog.keywords")}
        title={`Blogs by ${capitalizeDashedString(
          authorName
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
            crumbLabel={capitalizeDashedString(authorName)}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />
          <BlogPageArticle>
            <CenteredMaxWidthContainer className={"tc"}>
              <Title fColor={"#2e2e38"} fSize={"48"} marginBottom={"2"}>
                {capitalizeDashedString(authorName)}
              </Title>
              {authorDescription === undefined ? undefined : (
                <Paragraph fColor={"#2e2e38"} fSize={"24"}>
                  {authorDescription}
                </Paragraph>
              )}
            </CenteredMaxWidthContainer>
            <BlogAuthorList authorName={authorName} />
          </BlogPageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default blogAuthorTemplate;
