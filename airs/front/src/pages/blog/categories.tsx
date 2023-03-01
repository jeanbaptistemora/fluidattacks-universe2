/* eslint react/forbid-component-props:0 */
import React from "react";
import { useTranslation } from "react-i18next";

import { Breadcrumbs } from "../../components/Breadcrumbs";
import { Seo } from "../../components/Seo";
import { CategoriesPage } from "../../scenes/CategoriesPage";
import { Layout } from "../../scenes/Footer/Layout";
import { NavbarComponent } from "../../scenes/Menu";
import { PageArticle } from "../../styles/styledComponents";

const CategoriesIndex: React.FC<IQueryData> = ({
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
        description={t("blog.listDescriptions.categories.description")}
        keywords={t("blog.keywords")}
        title={`Categories | Blog | Fluid Attacks`}
        url={"https://fluidattacks.com/blog/authors/"}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumbs currentPath={path} />

          <PageArticle bgColor={"#f9f9f9"}>
            <CategoriesPage />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default CategoriesIndex;
