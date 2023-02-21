/* eslint react/forbid-component-props:0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";
import { useTranslation } from "react-i18next";

import { Seo } from "../../components/Seo";
import { Layout } from "../../scenes/Footer/Layout";
import { NavbarComponent } from "../../scenes/Menu";
import { TagsPage } from "../../scenes/TagsPage";
import { PageArticle } from "../../styles/styledComponents";
import { capitalizeObject } from "../../utils/utilities";

const TagsIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

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
          <Breadcrumb
            crumbLabel={"Tags"}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

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
