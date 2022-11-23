/* eslint react/forbid-component-props:0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";
import { useTranslation } from "react-i18next";

import { Layout } from "../../components/Layout";
import { NavbarComponent } from "../../components/Navbar";
import { Seo } from "../../components/Seo";
import { TagsList } from "../../components/TagsList";
import { InternalContainer, PageArticle } from "../../styles/styledComponents";
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
            <InternalContainer>
              <TagsList />
            </InternalContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default TagsIndex;
