/*
 * SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
 *
 * SPDX-License-Identifier: MPL-2.0
 */

/* eslint react/forbid-component-props:0 */
import { Breadcrumb } from "gatsby-plugin-breadcrumb";
import React from "react";
import { useTranslation } from "react-i18next";

import { CategoriesList } from "../../components/CategoriesList";
import { Layout } from "../../components/Layout";
import { NavbarComponent } from "../../components/Navbar";
import { Seo } from "../../components/Seo";
import { InternalContainer, PageArticle } from "../../styles/styledComponents";
import { capitalizeObject } from "../../utils/utilities";

const CategoriesIndex: React.FC<IQueryData> = ({
  pageContext,
}: IQueryData): JSX.Element => {
  const {
    breadcrumb: { crumbs },
  } = pageContext;

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
          <Breadcrumb
            crumbLabel={"Categories"}
            crumbSeparator={" / "}
            crumbs={capitalizeObject(crumbs)}
          />

          <PageArticle bgColor={"#f9f9f9"}>
            <InternalContainer>
              <CategoriesList />
            </InternalContainer>
          </PageArticle>
        </div>
      </Layout>
    </React.Fragment>
  );
};

// eslint-disable-next-line import/no-default-export
export default CategoriesIndex;
