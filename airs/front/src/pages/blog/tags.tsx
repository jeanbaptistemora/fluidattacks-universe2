/* eslint react/forbid-component-props:0 */
import React from "react";
import { useTranslation } from "react-i18next";

import { Breadcrumbs } from "../../components/Breadcrumbs";
import { Seo } from "../../components/Seo";
import { Layout } from "../../scenes/Footer/Layout";
import { NavbarComponent } from "../../scenes/Menu";
import { TagsPage } from "../../scenes/TagsPage";
import { PageArticle } from "../../styles/styledComponents";

const TagsIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const { location } = pageContext.breadcrumb;

  const home = ["/"];
  const path = home.concat(
    location.split("/").filter((name): boolean => name !== "")
  );

  const { t } = useTranslation();

  return (
    <React.Fragment>
      <Seo
        description={t("blog.listDescriptions.tags.description")}
        keywords={t("blog.keywords")}
        title={`Tags | Blog | Fluid Attacks`}
        url={"https://fluidattacks.com/blog/tags/"}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumbs currentPath={path} />

          <PageArticle bgColor={"#f9f9f9"}>
            <TagsPage />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default TagsIndex;
