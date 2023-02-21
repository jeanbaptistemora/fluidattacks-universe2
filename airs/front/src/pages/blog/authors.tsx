/* eslint react/forbid-component-props:0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";
import { useTranslation } from "react-i18next";

import { Seo } from "../../components/Seo";
import { AuthorsPage } from "../../scenes/AuthorsPage";
import { Layout } from "../../scenes/Footer/Layout";
import { NavbarComponent } from "../../scenes/Menu";
import { PageArticle } from "../../styles/styledComponents";
import { capitalizeObject } from "../../utils/utilities";

const AuthorsIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

  const { t } = useTranslation();

  return (
    <React.Fragment>
      <Seo
        description={t("blog.listDescriptions.authors.description")}
        keywords={t("blog.keywords")}
        title={`Authors | Blog | Fluid Attacks`}
        url={"https://fluidattacks.com/blog/authors/"}
      />

      <Layout>
        <div>
          <NavbarComponent />
          <Breadcrumb
            crumbLabel={"Authors"}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle bgColor={"#f9f9f9"}>
            <AuthorsPage />
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default AuthorsIndex;
