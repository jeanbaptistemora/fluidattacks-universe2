import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";

import { BlogAuthorList } from "../components/BlogAuthorList";
import { Layout } from "../components/Layout";
import { NavbarComponent } from "../components/Navbar";
import { PageHeader } from "../components/PageHeader";
import { Seo } from "../components/Seo";
import { PageArticle } from "../styles/styledComponents";
import { translate } from "../utils/translations/translate";

const blogAuthorIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { authorName } = pageContext;

  const capitalizeName: (words: string) => string = (words: string): string => {
    const separateWord = words.toLowerCase().split("-");

    const capitalizedName = separateWord.map(
      (word: string): string =>
        `${word.charAt(0).toUpperCase()}${word.substring(1)}`
    );

    return capitalizedName.join(" ");
  };

  return (
    <React.Fragment>
      <Seo
        description={translate.t("blog.description")}
        keywords={translate.t("blog.keywords")}
        title={"Blog | A Pentesting Company | Fluid Attacks"}
        url={"https://fluidattacks.com/blog"}
      />

      <Layout>
        <div>
          <NavbarComponent />

          <Breadcrumb
            crumbLabel={capitalizeName(authorName)}
            crumbSeparator={" / "}
            crumbs={crumbs}
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
